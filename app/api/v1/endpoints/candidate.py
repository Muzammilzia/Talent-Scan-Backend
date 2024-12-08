from fastapi import APIRouter, HTTPException
from app.db.schemas.candidate import CandidateCreate, CandidateSignInRequest
from app.services.candidate import create_candidate, sign_in_candidate
from enum import Enum

router = APIRouter()

class Candidate_Routes(str, Enum):
    SIGN_IN = '/sign-in'
    SIGN_UP = '/sign-up'
    GET_CANDIDATE_BY_ID = '/{id}'

@router.post(Candidate_Routes.SIGN_IN.value)
async def sign_in(candidate: CandidateSignInRequest):
    try:
        result = await sign_in_candidate(candidate)
        return {"message": "Candidate signed in successfully", "data": result}
    except Exception as e:
        print('error',e)
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.post(Candidate_Routes.SIGN_UP.value)
async def sign_up(candidate: CandidateCreate):
    try:
        result = await create_candidate(candidate)
        return {"message": "Candidate created successfully", "candidate": result}
    except Exception as e:
        print('error',e)
        raise HTTPException(status_code=e.status_code, detail=str(e))