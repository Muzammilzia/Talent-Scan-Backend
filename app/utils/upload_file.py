from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Request, status
import time
import os

async def upload_file(resume: UploadFile):
    try:
        print(resume)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        PARENT_OF_PARENT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
        file_location = os.path.join(PARENT_OF_PARENT_DIR, "uploads", f"{time.time()}-{resume.filename}")
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb") as f:
            f.write(await resume.read())

        return file_location
    
    except Exception as e:
        print('error',e)
        raise HTTPException(status_code=500, detail=str(e))