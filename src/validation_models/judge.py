from pydantic import BaseModel, Field


class judgeJson(BaseModel):
    grade: str = Field(..., description="Pass or Fail")
    grade_summary: str = Field(..., description="Summary of what things are right or what is wrong with the extraction")
