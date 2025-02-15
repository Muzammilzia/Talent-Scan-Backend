from fastapi import HTTPException
from pymongo import MongoClient
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from bson import ObjectId
from app.db.schemas.job_post import JobPostCreate
from app.db.session import get_job_post_collection

async def create_job(job: JobPostCreate):
    try:
        collection = get_job_post_collection()
        job_dict = job.dict()
        print(job_dict)
        job_dict["jobType"] = [job_type.value for job_type in job_dict["jobType"]]
        result = collection.insert_one(job_dict)
        return {"id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def edit_job(id: str, job: JobPostCreate):
    try:
        collection = get_job_post_collection()
        update_data = job.dict(exclude_unset=True)  # Ignore None values
        if "jobType" in update_data:
            update_data["jobType"] = [job_type.value for job_type in update_data["jobType"]]
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"message": "Job updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def list_jobs():
    try:
        collection = get_job_post_collection()
        jobs = list(collection.find())
        print(jobs, 'in list jobs')
        for job in jobs:
            job["_id"] = str(job["_id"])
        return { "jobs": jobs }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def list_jobs_by_company(companyId: str):
    try:
        collection = get_job_post_collection()
        jobs = list(collection.find({"company": companyId}))
        for job in jobs:
            job["_id"] = str(job["_id"])
        return { "jobs": jobs }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_job_by_id(id: str):
    try:
        collection = get_job_post_collection()
        job = collection.find_one({"_id": ObjectId(id)})
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        job["_id"] = str(job["_id"])
        return { "job": job }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
