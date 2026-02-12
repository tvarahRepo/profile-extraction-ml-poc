from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from src.config import get_extraction_llm
from src.validation_models.jd import JobDescription


system_prompt = SystemMessagePromptTemplate.from_template(
    """
### ROLE
You are a Technical Recruiter AI. Your job is to extract structured matching criteria from a messy Job Description.

### INSTRUCTIONS
1. **Ignore the Fluff:** Do not extract text from the "About Us" or "Culture" sections unless it specifies a hard requirement (e.g., "Must work EST timezone").
2. **Distinguish Requirements:**
   - If a skill says "Required", "Must have", or "Proficient in", put it in `mandatory_skills`.
   - If a skill says "Bonus", "Plus", "Good to have", or "Familiarity with", put it in `optional_skills`.
3. **Formatting:**
   - Skills should be single keywords (e.g., "Python", "AWS", "React"). Do not write sentences.
"""
)

human_prompt = HumanMessagePromptTemplate.from_template(
    """
    Here is the JobDescription Markdown:
    <job_description>
    {job_description_markdown}
    </job_description>
"""
)

prompt_template = ChatPromptTemplate.from_messages([system_prompt, human_prompt])


def get_jd_chain():
    llm = get_extraction_llm()
    return prompt_template | llm.with_structured_output(JobDescription)
