from fastapi import APIRouter, HTTPException
from app.db.schemas.job_application import JobApplicationBase
from app.db.session import get_job_Application_collection
from enum import Enum
import random

router = APIRouter()

class Job_Application_Routes(str, Enum):
    APPLY = '/apply'
    GET_BY_COMPANY = '/get-by-company'
    GET_BY_CANDIDATE = '/get-by-candidate/{id}'
    GET_BY_JOB = '/get-by-job'

@router.post(Job_Application_Routes.APPLY.value)
async def create(job_application: JobApplicationBase):
    try:
        collection = get_job_Application_collection()
        job_application = job_application.dict()
        
        job_application["AIScore"] = round(random.uniform(50, 90), 2)
        
        result = collection.insert_one(job_application)
        return {"message": "Job application created successfully", "data": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get(Job_Application_Routes.GET_BY_CANDIDATE.value)
async def get_by_candidate(id: str):
    try:
        collection = get_job_Application_collection()

        job_applications = list(collection.find({"candidate": id}))

        for application in job_applications:
            application["_id"] = str(application["_id"])
        
        return {"data": job_applications}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
