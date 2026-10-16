from pydantic import Field, BaseModel
from typing import List

class PersonalInfo(BaseModel):
    name: str = Field(..., description='The full name of the certificate owner')
    
class CertificateInfo(BaseModel):
    company_name: str = Field(..., description="The certification course provider.")
    course_name: str = Field(..., description="A concise description of the type of certification.")
    certification_date: str = Field(..., description="The date of the certificate (in format: 3-Sep-2026) or NA if unavailable.")
    expiry_date: str = Field(..., description="The date for when the certification expires (in format: 3-Sep-2026) or NA if unavailable.")

class DataReport(BaseModel):
    certificate_text: str = Field(..., description="The original parsed certificate text.")
    personal_info: PersonalInfo = Field(..., description="parsed personal details within the certificate text.")
    certificate_info: CertificateInfo = Field(..., description="parsed certificate details within the certificate text.")

class EmailDraft(BaseModel):
    subject_line: str = Field(..., description="The subject line of the email.")
    content: str = Field(..., description="The main content of the email.")