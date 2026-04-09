from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.resume import (
    InterviewStartRequest,
    InterviewStartResponse,
    InterviewAnswerRequest,
    InterviewAnswerResponse,
    InterviewSession,
)
from app.services.qwen import qwen_service
import uuid

router = APIRouter(prefix="/interview", tags=["Interview (v2)"])

# In-memory interview session storage (use Redis for production)
_interview_sessions: dict[str, InterviewSession] = {}


@router.post("/start", response_model=InterviewStartResponse)
async def start_interview(request: InterviewStartRequest):
    """
    Start a mock interview session.
    Returns the first interview question.
    """
    session_id = str(uuid.uuid4())

    # Generate first question
    result = await qwen_service.interview_question(
        role=request.role,
        experience_level=request.experience_level,
        question_number=1,
        focus_areas=request.focus_areas,
    )

    # Store session
    _interview_sessions[session_id] = InterviewSession(
        session_id=session_id,
        user_id=request.user_id,
        role=request.role,
        question_number=1,
        total_questions=10,
        is_complete=False,
    )

    return InterviewStartResponse(
        session_id=session_id,
        first_question=result.get("next_question", "Tell me about yourself."),
    )


@router.post("/answer", response_model=InterviewAnswerResponse)
async def submit_answer(request: InterviewAnswerRequest):
    """
    Submit an answer to an interview question.
    Returns feedback, score, and the next question.
    """
    # Validate session
    session = _interview_sessions.get(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")

    if session.is_complete:
        raise HTTPException(status_code=400, detail="Interview session is already complete")

    # Get feedback and next question
    result = await qwen_service.interview_question(
        role=session.role,
        experience_level="Senior",  # Could be stored in session
        question_number=session.question_number + 1,
        previous_answer=request.answer,
    )

    # Update session
    session.question_number += 1

    # Check if interview is complete
    if session.question_number > session.total_questions or result.get("is_complete", False):
        session.is_complete = True
        result["next_question"] = None
        result["is_complete"] = True

    return InterviewAnswerResponse(
        feedback=result.get("feedback", ""),
        score=result.get("score", 0),
        next_question=result.get("next_question"),
        is_complete=session.is_complete,
    )


@router.get("/session/{session_id}")
async def get_interview_session(session_id: str):
    """Get current interview session status."""
    session = _interview_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session.session_id,
        "role": session.role,
        "question_number": session.question_number,
        "total_questions": session.total_questions,
        "is_complete": session.is_complete,
    }
