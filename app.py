import streamlit as st
import tempfile
import os

from src.graph.workflow import build_graph


st.set_page_config(page_title="Document Extraction Pipeline", layout="wide")
st.title("Document Extraction Pipeline")

# --- Mode Selection ---
mode = st.radio("Select mode:", ["Resume Only", "JD Only", "Both"], horizontal=True)

# --- File Uploaders ---
resume_file = None
jd_file = None

col1, col2 = st.columns(2)

if mode in ("Resume Only", "Both"):
    with col1:
        resume_file = st.file_uploader(
            "Upload Resume (PDF/DOCX)", type=["pdf", "docx"], key="resume"
        )

if mode in ("JD Only", "Both"):
    with col2:
        jd_file = st.file_uploader(
            "Upload Job Description (PDF/DOCX)", type=["pdf", "docx"], key="jd"
        )

# --- Extract Button ---
if st.button("Extract", type="primary"):
    # Validate inputs
    if mode in ("Resume Only", "Both") and resume_file is None:
        st.error("Please upload a resume file.")
        st.stop()
    if mode in ("JD Only", "Both") and jd_file is None:
        st.error("Please upload a job description file.")
        st.stop()

    # Save uploaded files to temp paths
    resume_path = None
    jd_path = None

    if resume_file:
        suffix = os.path.splitext(resume_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(resume_file.read())
            resume_path = tmp.name

    if jd_file:
        suffix = os.path.splitext(jd_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(jd_file.read())
            jd_path = tmp.name

    mode_map = {"Resume Only": "resume_only", "JD Only": "jd_only", "Both": "both"}

    graph = build_graph()

    with st.spinner("Processing..."):
        result = graph.invoke({
            "mode": mode_map[mode],
            "resume_file_path": resume_path,
            "jd_file_path": jd_path,
            "resume_markdown": None,
            "jd_markdown": None,
            "resume_data": None,
            "jd_data": None,
            "judge_results": [],
        })

    # --- Display Results ---
    st.divider()

    if result.get("resume_data"):
        st.subheader("Resume Extraction")
        st.json(result["resume_data"].model_dump())

    if result.get("jd_data"):
        st.subheader("JD Extraction")
        st.json(result["jd_data"].model_dump())

    st.subheader("Judge Results")
    for jr in result.get("judge_results", []):
        icon = "✅" if jr["grade"].lower() == "pass" else "❌"
        st.write(f"{icon} **{jr['source'].upper()}**: {jr['grade']} — {jr['summary']}")

    # Cleanup temp files
    if resume_path and os.path.exists(resume_path):
        os.unlink(resume_path)
    if jd_path and os.path.exists(jd_path):
        os.unlink(jd_path)
