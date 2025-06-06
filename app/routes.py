# app/routes.py

import os
import tempfile
import shutil

from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.response import ReviewOutput
from app.services.review_engine import (
    generate_code_review_with_standards,
    generate_suggested_fix_with_standards,
)
from app.services.standards_parser import extract_standards_from_docx

router = APIRouter(tags=["Code Review"])


@router.post(
    "/review",
    response_model=ReviewOutput,
    summary="Review source code with custom coding standards (file uploads)",
)
async def review_code_with_files(
    code_file: UploadFile = File(
        ..., description="The code file to review."
    ),
    standards_file: UploadFile = File(
        ..., description="Coding standards file (.docx or .txt)."
    ),
):
    """
    1. Read & decode `code_file` (UTF-8). Reject if empty.
    2. Read `standards_file`:
       - If '.docx': save to a temp file, parse via extract_standards_from_docx, then delete temp.
       - Else (e.g. '.txt'): read as UTF-8. Reject if empty.
    3. Call the Gemini/FAISS pipeline to get (review_md, score_value) and fix_md.
    4. Wrap them into a ReviewOutput and return JSON.
    """

    # 1. Read & decode the code file
    try:
        code_bytes = await code_file.read()                     # read raw bytes
        code_str = code_bytes.decode("utf-8", errors="replace")  # decode → Python string
        if not code_str.strip():
            # If file is all whitespace or empty, reject
            raise HTTPException(status_code=400, detail="Uploaded code file is empty.")
    except HTTPException:
        raise   # re‐raise if it was our 400
    except Exception as e:
        # A different error (e.g. decode failure)
        raise HTTPException(status_code=400, detail=f"Failed to read code file: {e}")

    # 2. Read & decode the standards file
    suffix = os.path.splitext(standards_file.filename)[1].lower()
    try:
        if suffix == ".docx":
            # ──> For .docx, we need to write it to disk (temp), parse, then delete:
            tmp_dir = tempfile.mkdtemp()
            tmp_path = os.path.join(tmp_dir, standards_file.filename)

            # Write uploaded bytes to that temp .docx file
            with open(tmp_path, "wb") as f:
                f.write(await standards_file.read())

            # Extract the plain‐text rules from the .docx
            standards_text = extract_standards_from_docx(tmp_path)

            # Clean up the temp folder
            shutil.rmtree(tmp_dir, ignore_errors=True)

        else:
            # ──> Any other extension (e.g. .txt), treat as plain‐text
            standards_bytes = await standards_file.read()
            standards_text = standards_bytes.decode("utf-8", errors="replace")
            if not standards_text.strip():
                raise HTTPException(status_code=400, detail="Standards file is empty.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read standards file: {e}")

    # 3. Invoke the LLM/FAISS pipeline
    try:
        # generate_code_review_with_standards returns a tuple: (review_markdown, score_float_or_None)
        review_md, score_value = generate_code_review_with_standards(code_str, standards_text)
        fix_md = generate_suggested_fix_with_standards(code_str, standards_text)
    except Exception as e:
        # If something goes wrong inside your LLM/FAISS calls
        raise HTTPException(status_code=500, detail=f"Review failed: {e}")

    # 4. Return JSON that matches ReviewOutput Pydantic model
    return ReviewOutput(
        review=review_md,
        suggested_fix=fix_md,
        score=score_value,
    )
