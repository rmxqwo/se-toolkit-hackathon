from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import os

from app.db import get_db
from app.models import UserProfile, ResumeHistory
from app.schemas.resume import (
    ResumeGenerateRequest,
    ResumeGenerateResponse,
    ResumeHistoryResponse,
    OptimizeRequest,
    OptimizeResponse,
    SkillItem,
    ExperienceItem,
    EducationItem,
    ProjectItem,
)
from app.services.qwen import qwen_service
from app.services.pdf_generator import pdf_generator

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/generate", response_model=ResumeGenerateResponse)
async def generate_resume(
    request: ResumeGenerateRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Generate a polished resume PDF.
    1. Calls Qwen API to polish the content
    2. Generates a professional PDF
    3. Saves to history
    """
    try:
        # Verify user exists
        result = await db.execute(select(UserProfile).where(UserProfile.id == request.user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Polish content with AI
        polished = await qwen_service.polish_resume(
            summary=request.summary or user.summary or "",
            skills=[s.model_dump() for s in request.skills],
            experience=[e.model_dump() for e in request.experience],
            education=[e.model_dump() for e in request.education],
            projects=[p.model_dump() for p in request.projects] if request.projects else [],
        )

        # Generate PDF
        pdf_filename = pdf_generator.generate(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
            location=user.location,
            linkedin=user.linkedin,
            github=user.github,
            portfolio=user.portfolio,
            professional_title=request.title or user.professional_title,
            summary=polished.get("summary", ""),
            skills=polished.get("skills", []),
            experience=polished.get("experience", []),
            education=polished.get("education", []),
            projects=polished.get("projects", []),
        )

        # Save to history
        resume_record = ResumeHistory(
            user_id=request.user_id,
            title=request.title,
            summary=polished.get("summary"),
            skills_json=polished.get("skills"),
            experience_json=polished.get("experience"),
            education_json=polished.get("education"),
            projects_json=polished.get("projects"),
            pdf_filename=pdf_filename,
            pdf_url=f"/resumes/download/{pdf_filename}",
            job_description=request.job_description,
        )
        db.add(resume_record)
        await db.flush()
        await db.refresh(resume_record)

        return ResumeGenerateResponse(
            resume_id=resume_record.id,
            pdf_url=f"/resumes/download/{pdf_filename}",
            message="Resume generated successfully!",
        )
    except HTTPException:
        raise
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error generating resume: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate resume: {str(e)}"
        )


@router.post("/optimize", response_model=OptimizeResponse)
async def optimize_resume(
    request: OptimizeRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Optimize resume for a specific job description.
    1. Analyzes job description for keywords
    2. Rewrites resume to match requirements
    3. Generates optimized PDF
    """
    # Verify user exists
    result = await db.execute(select(UserProfile).where(UserProfile.id == request.user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get current resume content or use defaults
    current_summary = request.current_resume or user.summary or ""
    current_skills = []
    current_experience = []
    current_education = []

    # Try to get latest resume from history
    history_result = await db.execute(
        select(ResumeHistory)
        .where(ResumeHistory.user_id == request.user_id)
        .order_by(ResumeHistory.created_at.desc())
        .limit(1)
    )
    latest_resume = history_result.scalar_one_or_none()

    if latest_resume:
        current_summary = latest_resume.summary or current_summary
        current_skills = latest_resume.skills_json or []
        current_experience = latest_resume.experience_json or []
        current_education = latest_resume.education_json or []

    # Optimize with AI
    optimized = await qwen_service.optimize_for_job(
        current_summary=current_summary,
        current_skills=current_skills,
        current_experience=current_experience,
        current_education=current_education,
        job_description=request.job_description,
    )

    # Convert skills to proper format
    optimized_skills = [
        SkillItem(**s) if isinstance(s, dict) else SkillItem(name=str(s))
        for s in optimized.get("skills", [])
    ]
    optimized_experience = [
        ExperienceItem(**e) if isinstance(e, dict) else ExperienceItem(
            company=str(e), position="Role"
        )
        for e in optimized.get("experience", [])
    ]
    optimized_education = [
        EducationItem(**edu) if isinstance(edu, dict) else EducationItem(
            institution=str(edu), degree="Degree"
        )
        for edu in optimized.get("education", [])
    ]

    # Generate optimized PDF
    pdf_filename = pdf_generator.generate(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        location=user.location,
        linkedin=user.linkedin,
        github=user.github,
        portfolio=user.portfolio,
        professional_title=user.professional_title,
        summary=optimized.get("summary", ""),
        skills=[s.model_dump() for s in optimized_skills],
        experience=[e.model_dump() for e in optimized_experience],
        education=[e.model_dump() for e in optimized_education],
    )

    # Save to history
    resume_record = ResumeHistory(
        user_id=request.user_id,
        title=f"Optimized - {user.professional_title or 'Resume'}",
        summary=optimized.get("summary"),
        skills_json=[s.model_dump() for s in optimized_skills],
        experience_json=[e.model_dump() for e in optimized_experience],
        education_json=[e.model_dump() for e in optimized_education],
        pdf_filename=pdf_filename,
        pdf_url=f"/resumes/download/{pdf_filename}",
        job_description=request.job_description,
    )
    db.add(resume_record)
    await db.flush()
    await db.refresh(resume_record)

    return OptimizeResponse(
        resume_id=resume_record.id,
        optimized_summary=optimized.get("summary", ""),
        optimized_skills=optimized_skills,
        optimized_experience=optimized_experience,
        optimized_education=optimized_education,
        pdf_url=f"/resumes/download/{pdf_filename}",
        keyword_match_score=optimized.get("keyword_match_score", 50.0),
    )


@router.get("/history/{user_id}", response_model=List[ResumeHistoryResponse])
async def get_resume_history(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get all generated resumes for a user."""
    result = await db.execute(
        select(ResumeHistory)
        .where(ResumeHistory.user_id == user_id)
        .order_by(ResumeHistory.created_at.desc())
    )
    resumes = result.scalars().all()
    return resumes


@router.get("/download/{filename}")
async def download_resume(filename: str):
    """Download a generated resume PDF."""
    filepath = os.path.join(pdf_generator.output_dir, filename)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="PDF file not found")

    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="application/pdf",
    )


@router.delete("/history/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume_history(resume_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a resume from history."""
    result = await db.execute(select(ResumeHistory).where(ResumeHistory.id == resume_id))
    resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Delete PDF file if exists
    if resume.pdf_filename:
        filepath = os.path.join(pdf_generator.output_dir, resume.pdf_filename)
        if os.path.exists(filepath):
            os.remove(filepath)

    await db.delete(resume)
    return None
