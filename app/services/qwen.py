import httpx
import json
import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)

QWEN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"


class QwenService:
    """Service for interacting with Qwen (DashScope) API."""

    def __init__(self):
        self.api_key = settings.QWEN_API_KEY
        self.model = settings.QWEN_MODEL
        self.timeout = 60.0  # seconds

    async def _make_request(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> Optional[str]:
        """Make a request to the Qwen API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    QWEN_API_URL,
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()

                # Extract the response content
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0]["message"]["content"]
                else:
                    logger.error(f"Unexpected Qwen API response: {data}")
                    return None

            except httpx.TimeoutException:
                logger.error("Qwen API request timed out")
                return None
            except httpx.HTTPStatusError as e:
                logger.error(f"Qwen API HTTP error: {e.response.status_code} - {e.response.text}")
                return None
            except Exception as e:
                logger.error(f"Qwen API request failed: {str(e)}")
                return None

    async def polish_resume(
        self,
        summary: str,
        skills: list[dict],
        experience: list[dict],
        education: list[dict],
        projects: list[dict] = None,
    ) -> dict:
        """
        Polish resume content using AI.
        Returns dict with polished summary, skills, experience, education, projects.
        """
        if projects is None:
            projects = []
            
        system_prompt = """You are an expert resume writer and career coach with 20+ years of experience.
Your task is to improve resume content to make it more impactful, professional, and ATS-friendly.

Rules:
- Use strong action verbs (Led, Architected, Optimized, Spearheaded)
- Quantify achievements with metrics where possible
- Keep descriptions concise but impactful
- Remove filler words and passive language
- Ensure consistency in tense (past for previous roles, present for current)
- Maintain the original meaning while enhancing the language
- Return ONLY valid JSON with no additional text"""

        # Format the resume data for the prompt
        experience_text = "\n".join([
            f"- {exp.get('position', '')} at {exp.get('company', '')} ({exp.get('start_date', '')} - {exp.get('end_date', '')}): {exp.get('description', '')}"
            for exp in experience
        ])

        skills_text = ", ".join([f"{s.get('name', '')} ({s.get('level', '')})" for s in skills])

        education_text = "\n".join([
            f"- {edu.get('degree', '')} in {edu.get('field_of_study', '')} from {edu.get('institution', '')} ({edu.get('graduation_date', '')})"
            for edu in education
        ])
        
        projects_text = "\n".join([
            f"- {proj.get('name', '')} ({proj.get('start_date', '')} - {proj.get('end_date', '')}): {proj.get('description', '')} [Technologies: {', '.join(proj.get('technologies', []))}]"
            for proj in projects
        ])

        user_message = f"""Please polish this resume content and return it as valid JSON:

PROFESSIONAL SUMMARY:
{summary}

SKILLS:
{skills_text}

WORK EXPERIENCE:
{experience_text}

PROJECTS:
{projects_text if projects_text else "No projects"}

EDUCATION:
{education_text}

Return the polished content in this EXACT JSON format:
{{
  "summary": "polished summary...",
  "skills": [{{"name": "...", "level": "...", "category": "..."}}],
  "experience": [{{"company": "...", "position": "...", "start_date": "...", "end_date": "...", "location": "...", "description": "polished...", "achievements": "bullet points..."}}],
  "projects": [{{"name": "...", "description": "...", "technologies": [...], "link": "...", "start_date": "...", "end_date": "..."}}],
  "education": [{{"institution": "...", "degree": "...", "field_of_study": "...", "graduation_date": "...", "gpa": "...", "honors": "..."}}]
}}"""

        response = await self._make_request(
            system_prompt,
            user_message,
            temperature=0.7,
            max_tokens=3000,
        )

        if response:
            try:
                # Try to extract JSON from the response (in case there's markdown formatting)
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    return json.loads(json_str)
                return json.loads(response)
            except json.JSONDecodeError:
                logger.error(f"Failed to parse Qwen response as JSON: {response}")
                return {
                    "summary": summary,
                    "skills": skills,
                    "experience": experience,
                    "education": education,
                    "projects": projects,
                }

        return {
            "summary": summary,
            "skills": skills,
            "experience": experience,
            "education": education,
            "projects": projects,
        }

    async def optimize_for_job(
        self,
        current_summary: str,
        current_skills: list[dict],
        current_experience: list[dict],
        current_education: list[dict],
        job_description: str,
    ) -> dict:
        """
        Optimize resume for a specific job description.
        Returns dict with optimized content and keyword match score.
        """
        system_prompt = """You are an expert resume optimizer. Your task is to tailor a resume to match a job description perfectly.

Rules:
- Identify key skills, technologies, and qualifications from the job description
- Rewrite the summary to directly address the role requirements
- Reorder and emphasize skills that match the job requirements
- Reframe experience bullet points to highlight relevant achievements
- Add missing keywords naturally (don't just list them)
- Calculate a keyword match score (0-100) based on how well the resume matches
- Return ONLY valid JSON with no additional text"""

        resume_text = f"""
SUMMARY: {current_summary}

SKILLS: {', '.join([f"{s.get('name', '')} ({s.get('level', '')})" for s in current_skills])}

EXPERIENCE:
{chr(10).join([f"- {exp.get('position', '')} at {exp.get('company', '')}: {exp.get('description', '')}" for exp in current_experience])}

EDUCATION:
{chr(10).join([f"- {edu.get('degree', '')} in {edu.get('field_of_study', '')}, {edu.get('institution', '')}" for edu in current_education])}
"""

        user_message = f"""Optimize this resume for the following job description:

JOB DESCRIPTION:
{job_description}

CURRENT RESUME:
{resume_text}

Return the optimized resume in this EXACT JSON format:
{{
  "summary": "optimized summary targeting this role...",
  "skills": [{{"name": "...", "level": "...", "category": "..."}}],
  "experience": [{{"company": "...", "position": "...", "start_date": "...", "end_date": "...", "location": "...", "description": "optimized...", "achievements": "..."}}],
  "education": [{{"institution": "...", "degree": "...", "field_of_study": "...", "graduation_date": "...", "gpa": "...", "honors": "..."}}],
  "keyword_match_score": 85.5
}}"""

        response = await self._make_request(
            system_prompt,
            user_message,
            temperature=0.5,
            max_tokens=3500,
        )

        if response:
            try:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    return json.loads(json_str)
                return json.loads(response)
            except json.JSONDecodeError:
                logger.error(f"Failed to parse Qwen response as JSON: {response}")
                return {
                    "summary": current_summary,
                    "skills": current_skills,
                    "experience": current_experience,
                    "education": current_education,
                    "keyword_match_score": 50.0,
                }

        return {
            "summary": current_summary,
            "skills": current_skills,
            "experience": current_experience,
            "education": current_education,
            "keyword_match_score": 50.0,
        }

    async def interview_question(
        self,
        role: str,
        experience_level: str,
        question_number: int,
        previous_answer: Optional[str] = None,
        focus_areas: Optional[list[str]] = None,
    ) -> dict:
        """
        Generate interview question or provide feedback on an answer.
        Returns dict with question/feedback and next steps.
        """
        if previous_answer:
            # Provide feedback on the previous answer and ask next question
            system_prompt = f"""You are a senior hiring manager conducting a technical interview for a {role} position ({experience_level} level).

Rules:
- Provide constructive, specific feedback on the candidate's answer
- Score the answer from 1-10 based on completeness, accuracy, and communication
- Ask one question at a time
- Vary question types: technical depth, system design, behavioral, problem-solving
- Be professional but encouraging
- Return ONLY valid JSON"""

            user_message = f"""The candidate answered the previous question with:

"{previous_answer}"

Provide feedback and ask the next question (Question #{question_number + 1}).

Return in this EXACT JSON format:
{{
  "feedback": "detailed constructive feedback...",
  "score": 7,
  "next_question": "your next interview question...",
  "is_complete": false
}}"""

            response = await self._make_request(
                system_prompt,
                user_message,
                temperature=0.8,
                max_tokens=1500,
            )
        else:
            # Generate the first question
            system_prompt = f"""You are a senior hiring manager conducting a technical interview for a {role} position ({experience_level} level).

Rules:
- Start with a question that assesses both technical knowledge and problem-solving approach
- Make it specific and practical, not theoretical
- Return ONLY valid JSON"""

            focus_text = f" Focus areas: {', '.join(focus_areas)}" if focus_areas else ""

            user_message = f"""Generate the first interview question (Question #1).{focus_text}

Return in this EXACT JSON format:
{{
  "feedback": "",
  "score": 0,
  "next_question": "your first interview question...",
  "is_complete": false
}}"""

            response = await self._make_request(
                system_prompt,
                user_message,
                temperature=0.8,
                max_tokens=800,
            )

        if response:
            try:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    return json.loads(json_str)
                return json.loads(response)
            except json.JSONDecodeError:
                logger.error(f"Failed to parse Qwen response as JSON: {response}")
                return {
                    "feedback": "Error processing response",
                    "score": 0,
                    "next_question": "Can you tell me about your experience?",
                    "is_complete": False,
                }

        return {
            "feedback": "",
            "score": 0,
            "next_question": "Tell me about your background.",
            "is_complete": False,
        }


# Singleton instance
qwen_service = QwenService()
