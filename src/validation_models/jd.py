from pydantic import BaseModel, Field


class skillsInfo(BaseModel):
    programming_languages: list[str] = Field(default=[], description="Programming languages as required, \
        Ex: Python,C,C++ etc if not present then return None")
    frameworks_and_libraries: list[str] = Field(default=[], description="Frameworks and libraries as required, \
        Ex: React,Angular,Django,Flask,Pandas,Pytorch etc if not present then return None")
    tools: list[str] = Field(default=[], description="Tools as required, \
        Ex: Git,Docker,Kubernetes,Jenkins,Jira,etc. if not present then return None")
    databases: list[str] = Field(default=[], description="Databases as required, \
        Ex: MySQL,PostgreSQL,MongoDB,Oracle,etc. if not present then return None")
    cloud_and_infra: list[str] = Field(default=[], description="Cloud and infra as required, \
        Ex: AWS,Azure,GCP,etc. if not present then return None")


class JobDescription(BaseModel):
    role_title: str = Field(..., description="The standard job title, e.g., 'Senior Backend Engineer'")
    company_name: str | None = Field(default=None, description="Name of the company")
    salary_range: str | None = Field(default=None, description="e.g. '$120k - $160k'")

    mandatory_skills: skillsInfo = Field(..., description="Technical skills explicitly marked as required")

    optional_skills: list[str] = Field(default=[], description="Skills listed as 'preferred', 'bonus', or 'plus'")

    min_years_experience: int | None = Field(default=None, description="Integer value of required years. e.g. '5+ years' -> 5")

    degree_required: str | None = Field(default=None, description="e.g. 'Bachelor in CS', 'PhD'")

    summary_responsibilities: list[str] = Field(..., description="Top 3-5 core responsibilities summarized")
