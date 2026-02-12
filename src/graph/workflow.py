from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from PIL import Image
from langchain_core.runnables.graph import MermaidDrawMethod
import io

from src.graph.state import GraphState


# --- Routing ---

def route_inputs(state: GraphState) -> list[Send]:
    """Fan out to resume branch, JD branch, or both based on mode.
    Using Sends -> as this is a fan out from node 
    """
    sends = []
    mode = state["mode"]
    if mode in ("resume_only", "both"):
        sends.append(Send("ocr_resume", state))
    if mode in ("jd_only", "both"):
        sends.append(Send("ocr_jd", state))
    return sends


################# Adding a Start Node #####################
def router_node(state:GraphState) -> dict:

    return {}

########## Resume Branch Nodes #########

def ocr_resume(state: GraphState) -> dict:
    from src.ocr import upload_file, get_ocr_response

    url = upload_file(state["resume_file_path"])
    ocr_response = get_ocr_response(url)
    markdown = " ".join(page.markdown for page in ocr_response.pages)
    return {"resume_markdown": markdown}


def parse_resume(state: GraphState) -> dict:
    from src.chains.resume_chain import get_resume_chain

    chain = get_resume_chain()
    result = chain.invoke({"resume_markdown": state["resume_markdown"]})
    return {"resume_data": result}

#####################################################

# def judge_resume(state: GraphState) -> dict:
#     from src.chains.judge_chain import get_judge_chain

#     chain = get_judge_chain()
#     result = chain.invoke({
#         "markdown": state["resume_markdown"],
#         "jsondata": state["resume_data"].model_dump_json(indent=4),
#     })
#     return {
#         "judge_results": [
#             {"source": "resume", "grade": result.grade, "summary": result.grade_summary}
#         ]
#     }


############## JD Branch Nodes #####################

def ocr_jd(state: GraphState) -> dict:
    from src.ocr import upload_file, get_ocr_response

    url = upload_file(state["jd_file_path"])
    ocr_response = get_ocr_response(url)
    markdown = " ".join(page.markdown for page in ocr_response.pages)
    return {"jd_markdown": markdown}


def parse_jd(state: GraphState) -> dict:
    from src.chains.jd_chain import get_jd_chain

    chain = get_jd_chain()
    result = chain.invoke({"job_description_markdown": state["jd_markdown"]})
    return {"jd_data": result}
#################################################################

def llm_as_judge(state: GraphState) -> dict:
    from src.chains.judge_chain import get_judge_chain

    chain = get_judge_chain()

    new_loop = state["reflection_loop"] + 1

    if state['mode'] == 'resume_only':
        result = chain.invoke({
            "markdown": state["resume_markdown"],
            "jsondata": state["resume_data"].model_dump_json(indent=4),
        })
        return {
            "reflection_loop": new_loop,
            "judge_results": [
                {"source": "resume", "grade": result.grade, "summary": result.grade_summary}
            ]
        }
    elif state['mode'] == 'jd_only':
        result = chain.invoke({
            "markdown": state["jd_markdown"],
            "jsondata": state["jd_data"].model_dump_json(indent=4),
        })
        return {
            "reflection_loop": new_loop,
            "judge_results": [
                {"source": "jd", "grade": result.grade, "summary": result.grade_summary}
            ]
        }
    else:
        result_resume = chain.invoke({
            "markdown": state["resume_markdown"],
            "jsondata": state["resume_data"].model_dump_json(indent=4),
        })


        result_jd = chain.invoke({
            "markdown": state["jd_markdown"],
            "jsondata": state["jd_data"].model_dump_json(indent=4),
        })
        return {
            "reflection_loop": new_loop,
            "judge_results": [
                {"source": "jd", "grade": result_jd.grade, "summary": result_jd.grade_summary},
                {"source": "resume", "grade": result_resume.grade, "summary": result_resume.grade_summary}
            ]
        }



# --- Convergence ---

# def aggregate_results(state: GraphState) -> dict:
#     """Convergence node. State already contains all results via reducers."""
#     return {}

def reflection_path(state: GraphState) -> str:
    """Route based on judge verdict. Retry once on FAIL, then always end."""

    if state['reflection_loop'] > 1:
        return "end"

    judge_results = state['judge_results']
    print(judge_results)

    # Get only the latest judge results (from the most recent pass)
    if len(judge_results) == 1:
        if judge_results[0]['grade'] == 'FAIL':
            return judge_results[0]['source']
        return "end"

    elif len(judge_results) > 1:
        # Check the last two entries (the most recent judge pass)
        recent = judge_results[-2:]
        if "FAIL" in [r['grade'] for r in recent]:
            return "both"
        return "end"

    return "end"
    

        





# --- Graph Builder ---

def build_graph():
    graph = StateGraph(GraphState)

    # Add nodes
    graph.add_node("router_node",router_node)
    graph.add_node("ocr_resume", ocr_resume)
    graph.add_node("ocr_jd", ocr_jd)
    graph.add_node("parse_resume", parse_resume)
    graph.add_node("parse_jd", parse_jd)
    graph.add_node("llm_as_judge", llm_as_judge)
    #graph.add_node("judge_jd", judge_jd)
    #graph.add_node("aggregate_results", aggregate_results)

    # Routing from START
    graph.add_conditional_edges("router_node", route_inputs)

    # Resume branch: ocr -> parse -> judge -> aggregate
    graph.add_edge("ocr_resume", "parse_resume")
    graph.add_edge("parse_resume", "llm_as_judge")
    #graph.add_edge("judge_resume", "aggregate_results")

    # JD branch: ocr -> parse -> judge -> aggregate
    graph.add_edge("ocr_jd", "parse_jd")
    graph.add_edge("parse_jd", "llm_as_judge")
    #graph.add_edge("judge_jd", "aggregate_results")

    # End
    #graph.add_edge("llm_as_judge", END)
    graph.add_conditional_edges("llm_as_judge",reflection_path,
                                {
                                    "resume":"ocr_resume",
                                    "jd":"ocr_jd",
                                    "both":"router_node",
                                    "end":END

                                })
    
    graph.set_entry_point("router_node")
    app = graph.compile()
    img = app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)
    img = Image.open(io.BytesIO(img))
    print(img.size)
    img.save('D:\\Tvarah\\resume_extraction\\src\\graph.png')
    return graph.compile()


if __name__ == "__main__":
    build_graph()