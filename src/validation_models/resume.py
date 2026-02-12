from pydantic import BaseModel, Field


class personalInfo(BaseModel):
    full_name: str = Field(..., description="Full name of the candidate")
    first_name: str = Field(..., description="First name of the candidate")
    middle_name: str | None = Field(default=None, description="Middle name of the candidate, if not present then return None")
    last_name: str | None = Field(default=None, description="Last name of the candidate, if not present then return None")
    date_of_birth: str | None = Field(default=None, description="Date of birth of the candidate, if not present then return None")
    gender: str | None = Field(default=None, description="Gender of the candidate, if not present then return None")
    nationality: str | None = Field(default=None, description="Nationality of the candidate, if not present then return None")
    work_authorization: str | None = Field(default=None, description="Work authorization of the candidate, if not present then return None")


class contactInfo(BaseModel):
    primary_email: str | None = Field(default=None, description="Primary email address of the candidate, if not present then return None")
    secondary_email: str | None = Field(default=None, description="Secondary email address of the candidate, if not present then return None")
    primary_phone_number: str | None = Field(default=None, description="Primary phone number of the candidate, if not present then return None")
    secondary_phone_number: str | None = Field(default=None, description="Secondary phone number of the candidate, if not present then return None")
    country_code: str | None = Field(default=None, description="Country code of the candidate, if not present then return None")
    current_city: str | None = Field(default=None, description="Current city of the candidate, if not present then return None")
    current_state: str | None = Field(default=None, description="Current state of the candidate, if not present then return None")
    current_country: str | None = Field(default=None, description="Current country of the candidate, if not present then return None")
    postal_address: str | None = Field(default=None, description="Address of the candidate, if not present then return None")


class educationInfo(BaseModel):
    institution_name: str | None = Field(default=None, description="Institution name of the candidate, if not present then return None")
    institution_type: str | None = Field(default=None, description="Institution type (University,College,School,Bootcamp,etc), if not present then return None")
    institution_country: str | None = Field(default=None, description="Country of the institution, if not present then return None")
    degree: str | None = Field(default=None, description="Degree of the candidate with respect to the institution, \
        example: B.E, B.Tech, M.E, M.Tech, Ph.D, etc. if not present then return None")
    field_of_study: str | None = Field(default=None, description="Field of study of the candidate with respect to the institution, \
        example: Computer Science, Information Technology, etc. if not present then return None")
    specialisation: str | None = Field(default=None, description="Specialisation of the candidate with respect to the institution, \
        example: Artificial Intelligence, Marketing, Finance etc. if not present then return None")
    education_level: str | None = Field(default=None, description="Education level of the candidate with respect to the institution, \
        example: high_school / bachelors / masters / phd / diploma/bootcamp/certificate, if not present then return None")
    start_date: str | None = Field(default=None, description="Start date at the institution, if not present then return None")
    end_date: str | None = Field(default=None, description="End date of the institution, \
        If mentioned - Present or Ongoing, return None")
    is_current: str | None = Field(default=None, description="Yes, if the candidate is currently pursuing the degree, \
        No, if the candidate has completed the degree, if not present then return None")
    grade_or_gpa: str | None = Field(default=None, description="Grade or GPA of the candidate with respect to the institution, \
        if not present then return None")
    mode: str | None = Field(default=None, description="Mode of the institution, \
        example: full_time, part_time, online, etc. if not present then return None")


class workExperienceInfo(BaseModel):
    company_name: str | None= Field(default=None, description="Company name of the candidate")
    company_location: str | None = Field(default=None, description="Location of the company, if not present then return None")
    job_title: str | None = Field(default=None, description="Job title of the candidate, if not present then return None")
    employment_type: str | None = Field(default=None, description="Employment type of the candidate with respect to the company, \
        example: full_time, part_time, contract, temporary,internship etc. if not present then return None")
    start_date: str | None = Field(default=None, description="Start date of the role, if not present then return None")
    end_date: str | None = Field(default=None, description="End date of the role, if not present then return None")
    is_current_role: str | None = Field(default=None, description="Yes, if the candidate is currently working in the role, if not present then return None")
    role_description: str | None = Field(default=None, description="Role description of the role, \
        This should be a brief summary of the role and responsibilities,not more than 200words.")


class skillsInfo(BaseModel):
    programming_languages: list[str] = Field(default=[], description="Programming languages the candidate has worked on, \
        Ex: Python,C,C++ etc if not present then return None")
    frameworks_and_libraries: list[str] = Field(default=[], description="Frameworks and libraries the candidate has worked on, \
        Ex: React,Angular,Django,Flask,Pandas,Pytorch etc if not present then return None")
    tools_and_platforms: list[str] = Field(default=[], description="Tools and platforms the candidate has worked on, \
        Ex: Git,Docker,Kubernetes,Jenkins,Jira,etc. if not present then return None")
    databases: list[str] = Field(default=[], description="Databases the candidate has worked on, \
        Ex: MySQL,PostgreSQL,MongoDB,Oracle,etc. if not present then return None")
    cloud_and_infra: list[str] = Field(default=[], description="Cloud and infra the candidate has worked on, \
        Ex: AWS,Azure,GCP,etc. if not present then return None")
    soft_skills: list[str] = Field(default=[], description="Soft skills of the candidate, \
        Ex: Communication,Teamwork,Leadership,Problem-solving,etc. if not present then return None")
    domain_skills: list[str] = Field(default=[], description="Domain skills of the candidate, \
        Ex: Finance,Healthcare,Education,etc. if not present then return None")
    certified_skills: list[str] = Field(default=[], description="Certified skills of the candidate, if not present then return None")


class ResumeData(BaseModel):
    personal_info: personalInfo = Field(..., description="Personal information of the candidate")
    contact_info: contactInfo = Field(..., description="Contact information of the candidate")
    education_info: list[educationInfo] = Field(..., description="Education information of the candidate")
    work_experience_info: list[workExperienceInfo] = Field(..., description="Work experience information of the candidate")
    skills_info: skillsInfo = Field(..., description="Skills information of the candidate")
