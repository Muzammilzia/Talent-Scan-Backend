from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Request, status
from app.db.schemas.candidate import CandidateCreate, CandidateSignInRequest, Socials, Qualification, Experience
from app.services.candidate import create_candidate, sign_in_candidate, get_candidate_by_id, update_candidate, get_all_candidates
from enum import Enum
from app.utils.upload_file import upload_file
from typing import Literal, List, Optional
import json
import time
import os

router = APIRouter()

class Candidate_Routes(str, Enum):
    SIGN_IN = '/sign-in'
    SIGN_UP = '/sign-up'
    GET_CANDIDATE_BY_ID = '/{id}'
    CANDIDATE_ME = '/me'
    PROFILE_EDIT = '/edit'
    LIST_CANDIDATES = '/list'


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

@router.post(Candidate_Routes.PROFILE_EDIT.value)
async def edit_profile(
    request: Request,
    fullName: Optional[str] = Form(None),
    bio: Optional[str] = Form(None),
    about: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    age: Optional[str] = Form(None),
    gender: Optional[Literal["male", "female", ""]] = Form(None),
    phone: Optional[str] = Form(None),
    skills: Optional[str] = Form(None),
    qualification: Optional[List[Qualification]] = Form(None),
    experience: Optional[List[Experience]] = Form(None),
    socials: Optional[str] = Form(None),
    resume: Optional[UploadFile] = File(None),
):
    try:
        # Convert `skills` JSON string back to a Python list
        skills_list: List[str] = json.loads(skills) if skills else []

        # Convert `socials` JSON string back to a Python dictionary
        socials_dict = json.loads(socials) if socials else {}

        candidate_id = request.state.user["id"]  # Extract candidate ID from request state

        update_data = {
            "fullName": fullName,
            "bio": bio,
            "about": about,
            "address": address,
            "age": age,
            "gender": gender,
            "phone": phone,
            "skills": skills_list,
            "qualification": qualification,
            "experience": experience,
            "socials": socials_dict,
        }


        # Remove None values to only update provided fields
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        print(update_data)

        if resume:
            print("inside")
            file_location = await upload_file(resume)
            update_data["resume"] = file_location

        print("herere")

        updated_candidate = await update_candidate(candidate_id, update_data)

        return {"message": "Profile updated successfully", "candidate": updated_candidate}

    except Exception as e:
        print("error", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get(Candidate_Routes.LIST_CANDIDATES.value)
async def candidate_list():
    try:
        candidates = await get_all_candidates()
        return {"message": "success", "candidates": candidates}
    except Exception as e:
        print('error',e)
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.get(Candidate_Routes.GET_CANDIDATE_BY_ID.value)
async def candidate_get_by_id(id: str):
    try:
        candidate = await get_candidate_by_id(id)
        return {"message": "success", "candidate": candidate}
    except Exception as e:
        print('error',e)
        raise HTTPException(status_code=e.status_code, detail=str(e))

