from fastapi import APIRouter, HTTPException
from app.models.request import CodeInput
from app.models.response import ReviewOutput
from app.services.review_engine import generate_code_review, generate_suggested_fix

router = APIRouter(tags=["Code Review"])

@router.post("/review", response_model=ReviewOutput, summary="Review source code")
async def review_code(data: CodeInput):
    try:
        if not data.code.strip():
            raise HTTPException(status_code=400, detail="Code input cannot be empty.")

        review_text = generate_code_review(data.code)
        suggested_code = generate_suggested_fix(data.code)

        # Optional: You can parse and compute a score based on review_text or keep None for now
        score = None

        return {
            "review": review_text,
            "suggested_fix": suggested_code,
            "score": score
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Review failed: {str(e)}")
