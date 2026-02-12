# Document Extraction ML POC

Extract structured data from **resumes** and **job descriptions** using OCR + LLM parsing, orchestrated by a LangGraph state graph with built-in QA validation.

```
PDF/DOCX  →  Mistral OCR  →  LLM Parser  →  LLM Judge  →  Structured JSON
```

## How It Works

Upload a resume, a job description, or both. The pipeline:

1. **OCR** — Mistral OCR converts the document to markdown
2. **Parse** — Ministral 14B extracts structured fields into Pydantic models
3. **Judge** — Microsoft Phi-4 validates the extraction against the source (catches hallucinations, date errors, missing data)

When processing both documents, the resume and JD branches run **in parallel** and converge at the end.

```
                    START
                      |
                [route_inputs]
                 /    │    \
          resume    both    jd
            │       / \      │
            ▼      ▼   ▼     ▼
      [ocr_resume]   [ocr_jd]
            │            │
      [parse_resume] [parse_jd]
            │            │
      [judge_resume] [judge_jd]
            \      │     /
         [aggregate_results]
                  │
                 END
```

## Quick Start

### Prerequisites

- Python 3.13+
- [UV](https://github.com/astral-sh/uv) package manager
- API keys for [Mistral](https://console.mistral.ai/) and [OpenRouter](https://openrouter.ai/)

### Setup

```bash
# Clone and enter the project
git clone <repo-url>
cd resume_extraction

# Create venv and install dependencies
uv venv
uv sync

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### Configure API Keys

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=sk-or-v1-...
MISTRAL_API_KEY=...
```

### Run

```bash
streamlit run app.py
```

Select a mode (Resume Only / JD Only / Both), upload your file(s), and hit **Extract**.

## Project Structure

```
resume_extraction/
├── app.py                          # Streamlit web UI
├── src/
│   ├── config.py                   # API keys + LLM client factories
│   ├── ocr.py                      # Mistral OCR (upload + extract)
│   ├── validation_models/
│   │   ├── resume.py               # ResumeData, personalInfo, contactInfo, ...
│   │   ├── jd.py                   # JobDescription, skillsInfo (JD version)
│   │   └── judge.py                # judgeJson (Pass/Fail verdict)
│   ├── chains/
│   │   ├── resume_chain.py         # Resume prompt + LangChain chain
│   │   ├── jd_chain.py             # JD prompt + LangChain chain
│   │   └── judge_chain.py          # Judge prompt + LangChain chain
│   └── graph/
│       ├── state.py                # GraphState TypedDict
│       └── workflow.py             # LangGraph StateGraph + build_graph()
├── experiment_1.ipynb              # Original resume parsing notebook
├── experiment_2.ipynb              # Original JD parsing notebook
├── pyproject.toml
└── data/                           # Sample documents (gitignored)
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| OCR | Mistral OCR API |
| LLM (parsing) | Ministral 14B via OpenRouter |
| LLM (judge) | Microsoft Phi-4 via OpenRouter |
| Orchestration | LangGraph (state graph, routing, parallel execution) |
| Chains | LangChain (prompts, structured output) |
| Validation | Pydantic v2 |
| UI | Streamlit |
| Package Manager | UV |

## Architecture Details

The pipeline is a **LangGraph StateGraph** defined in `src/graph/workflow.py`:

- **Routing** — `route_inputs()` inspects the `mode` field and returns `Send` objects to fan out to the appropriate branch(es)
- **Parallel execution** — In "Both" mode, resume and JD branches run concurrently in the same superstep
- **Reducer** — `judge_results` uses `operator.add` so parallel branches append results without overwriting
- **Reflection** — `reflection_path` Retries the node which caused the failure


## License

Private — internal use only.
