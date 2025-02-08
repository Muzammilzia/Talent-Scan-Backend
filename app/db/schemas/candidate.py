from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import Literal, List, Optional
from datetime import date

class Qualification(BaseModel):
    institute: str
    program: str
    startDate: date
    endDate: date
    description: Optional[str]

class Experience(BaseModel):
    company_or_organization: str = Field(..., alias="company/organization")
    role: str
    startDate: date
    endDate: date
    description: Optional[str]

class Socials(BaseModel):
    name: str  # Platform name (e.g., 'LinkedIn', 'GitHub', 'Website')
    url: HttpUrl  # URL to the social profile

class CandidateSignInRequest(BaseModel):
    email: EmailStr  # Ensures the email is a valid email format
    password: str 

class CandidateBase(BaseModel):
    fullName: Optional[str] = ''
    resume: Optional[str] = ''
    bio: Optional[str] = ''
    about: Optional[str] = ''
    address: Optional[str] = ''
    age: Optional[str] = ''
    gender: Literal["male", "female", ""] = ""
    phone: Optional[str] = ''
    email: EmailStr
    password: str  = Field(..., min_length=7)
    skills: Optional[List[str]] = []
    resume: Optional[str] = ''

class CandidateCreate(CandidateBase):
    qualification: Optional[List[Qualification]] = []
    experience: Optional[List[Experience]] = []
    socials: Optional[List[Socials]] = []

class CandidateInDB(CandidateCreate):
    id: str = Field(..., alias="_id")

class CandidateOut(CandidateInDB):
    pass
