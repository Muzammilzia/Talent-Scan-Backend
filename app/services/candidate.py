# app/services/candidate.py
from fastapi import HTTPException, status
from app.db.session import get_candidates_collection
from app.db.schemas.candidate import CandidateCreate, CandidateSignInRequest
from bson import ObjectId  # For MongoDB ObjectId handling
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_jwt_token

async def create_candidate(candidate_data: CandidateCreate) -> dict:
    collection = get_candidates_collection()
    candidate = collection.find_one({ "email": candidate_data.email })

    if candidate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already in use"
        )

    # Hash the password before storing it in the database
    hashed_password = hash_password(candidate_data.password)

    # Candidate data to insert into MongoDB
    candidate_document = {
        "fullName": candidate_data.fullName,
        "bio": candidate_data.bio,
        "address": candidate_data.address,
        "age": candidate_data.age,
        "gender": candidate_data.gender,
        "phone": candidate_data.phone,
        "email": candidate_data.email,
        "skills": candidate_data.skills,
        "qualification": candidate_data.qualification,
        "experience": candidate_data.experience,
        "socials": candidate_data.socials,
        "password": hashed_password
    }

    # Insert the candidate document into MongoDB
    result = collection.insert_one(candidate_document)

    # Return the created candidate with MongoDB _id as string
    candidate_document["_id"] = str(result.inserted_id)
    candidate_document.pop("password")
    return candidate_document

async def sign_in_candidate(payload_candidate: CandidateSignInRequest) -> dict:
    # Fetch the collection
    collection = get_candidates_collection()

    # Search for the candidate by email
    candidate = collection.find_one({"email": payload_candidate.email})
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found."
        )

    # Verify the password
    if not verify_password(payload_candidate.password, candidate["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password."
        )

    # Generate JWT token
    token = create_jwt_token({"id": str(candidate["_id"]), "email": candidate["email"]})

    # Return the token and candidate information
    return {"token": token, "candidate": {"id": str(candidate["_id"]), "email": candidate["email"]}}

async def get_candidate_by_id(id: str) -> dict:
    collection = get_candidates_collection()
    try:
        object_id = ObjectId(id)  # Convert string to ObjectId
    except Exception as e:
        print(f"Invalid ObjectId: {e}")
        return None  # Handle invalid ObjectId cases

    candidate = collection.find_one({"_id": object_id}, {"password": 0})
    candidate["_id"] = str(candidate["_id"])
    return candidate