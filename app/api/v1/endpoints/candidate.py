from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Request, status
from app.db.schemas.candidate import CandidateCreate, CandidateSignInRequest
from app.services.candidate import create_candidate, sign_in_candidate, get_candidate_by_id
from enum import Enum
from app.utils.upload_file import upload_file
import time
import os

router = APIRouter()

class Candidate_Routes(str, Enum):
    SIGN_IN = '/sign-in'
    SIGN_UP = '/sign-up'
    GET_CANDIDATE_BY_ID = '/{id}'
    CANDIDATE_ME = '/me'


@router.post(Candidate_Routes.SIGN_IN.value)
async def sign_in(candidate: CandidateSignInRequest):
    try:
        result = await sign_in_candidate(candidate)
        return {"message": "Candidate signed in successfully", "data": result}
    except Exception as e:
        print('error',e)
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))

@router.post(Candidate_Routes.SIGN_UP.value)
async def sign_up(
    fullName: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    resume: UploadFile = File(...)
):
    try:
        print(resume.filename)
        file_location = await upload_file(resume)

        candidate = CandidateCreate(
            fullName=fullName, 
            email=email, 
            password=password, 
            resume=file_location
        )
        result = await create_candidate(candidate)
        return {"message": "Candidate created successfully", "candidate": result}
    except Exception as e:
        print('error',e)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get(Candidate_Routes.CANDIDATE_ME.value)
async def candidate_me(request: Request):
    try:
        candidate = await get_candidate_by_id(request.state.user["id"])
        return {"message": "success", "candidate": candidate}
    except Exception as e:
        print('error',e)
        raise HTTPException(status_code=e.status_code, detail=str(e))