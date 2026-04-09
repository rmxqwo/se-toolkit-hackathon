from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from app.models.base import Base, CommonMixin


class ResumeHistory(Base, CommonMixin):
    """Stores generated resume versions for history tracking."""
    __tablename__ = "resume_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)

    # Resume content (polished version from AI)
    title = Column(String(200), nullable=True)  # Version title
    summary = Column(Text, nullable=True)
    skills_json = Column(JSON, nullable=True)  # Array of skill objects
    experience_json = Column(JSON, nullable=True)  # Array of experience objects
    education_json = Column(JSON, nullable=True)  # Array of education objects
    projects_json = Column(JSON, nullable=True)  # Array of project objects

    # Generated files
    pdf_filename = Column(String(500), nullable=True)
    pdf_url = Column(String(500), nullable=True)

    # Metadata
    job_description = Column(Text, nullable=True)  # Original job description (if optimized)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("UserProfile", backref="resumes")

    def __repr__(self):
        return f"<ResumeHistory {self.title or 'Untitled'} for user {self.user_id}>"


class Skill(Base, CommonMixin):
    """Individual skills (stored as JSON in ResumeHistory, but kept for reference)."""
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    level = Column(String(20), nullable=True)  # Beginner, Intermediate, Advanced, Expert
    category = Column(String(50), nullable=True)  # Technical, Soft, Language, etc.

    def __repr__(self):
        return f"<Skill {self.name} ({self.level})>"


class Experience(Base, CommonMixin):
    """Work experience entries (stored as JSON in ResumeHistory)."""
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    company = Column(String(200), nullable=False)
    position = Column(String(200), nullable=False)
    start_date = Column(String(20), nullable=True)  # e.g., "Jan 2020"
    end_date = Column(String(20), nullable=True)  # e.g., "Present" or "Dec 2023"
    location = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    achievements = Column(Text, nullable=True)  # Bullet points, newline-separated

    def __repr__(self):
        return f"<Experience {self.position} at {self.company}>"


class Education(Base, CommonMixin):
    """Education entries (stored as JSON in ResumeHistory)."""
    __tablename__ = "educations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    institution = Column(String(200), nullable=False)
    degree = Column(String(200), nullable=False)
    field_of_study = Column(String(200), nullable=True)
    graduation_date = Column(String(20), nullable=True)
    gpa = Column(String(10), nullable=True)
    honors = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Education {self.degree} in {self.field_of_study}>"
