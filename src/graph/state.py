import operator
from typing import Annotated, TypedDict, Optional

from src.validation_models.resume import ResumeData
from src.validation_models.jd import JobDescription


class GraphState(TypedDict):
    # --- Inputs (set at invocation) ---
    mode: str  # "resume_only" | "jd_only" | "both"
    resume_file_path: Optional[str]
    jd_file_path: Optional[str]
    # --- Intermediate: OCR markdown ---
    resume_markdown: Optional[str]
    jd_markdown: Optional[str]
    # --- Extraction results ---
    resume_data: ResumeData | None
    jd_data: JobDescription | None
    # --- Judge results (reducer for parallel merge) ---
    # Each entry: {"source": "resume"|"jd", "grade": "Pass"|"Fail", "summary": "..."}
    judge_results: Annotated[list[dict], operator.add]
