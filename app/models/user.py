from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.models.base import Base, CommonMixin


class UserProfile(Base, CommonMixin):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Personal Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    location = Column(String(200), nullable=True)  # City, Country
    linkedin = Column(String(500), nullable=True)
    github = Column(String(500), nullable=True)
    portfolio = Column(String(500), nullable=True)
    professional_title = Column(String(200), nullable=True)  # e.g., "Senior Software Engineer"

    # Summary
    summary = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<UserProfile {self.first_name} {self.last_name} ({self.email})>"
