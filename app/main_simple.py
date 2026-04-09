from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
import os
import json
import httpx
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

app = FastAPI(title="AI Resume Builder", description="AI-Powered Resume Builder")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
frontend_path = Path("frontend")
frontend_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="frontend", html=True), name="static")

# ============ Data Storage ============
users_db = {}
resumes_db = {}

# ============ Pydantic Models ============
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    professional_title: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    summary: Optional[str] = None

class SkillItem(BaseModel):
    name: str
    level: Optional[str] = None
    category: Optional[str] = None

class ExperienceItem(BaseModel):
    company: str
    position: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    achievements: Optional[str] = None

class EducationItem(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    graduation_date: Optional[str] = None
    gpa: Optional[str] = None
    honors: Optional[str] = None

class ProjectItem(BaseModel):
    name: str
    description: str
    technologies: List[str] = []
    link: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class ResumeGenerateRequest(BaseModel):
    user_id: str
    title: Optional[str] = None
    summary: Optional[str] = None
    skills: List[SkillItem] = []
    experience: List[ExperienceItem] = []
    education: List[EducationItem] = []
    projects: List[ProjectItem] = []
    job_description: Optional[str] = None

# ============ AI Integration ============
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
QWEN_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

async def enhance_with_ai(content: str, content_type: str) -> str:
    if not QWEN_API_KEY or QWEN_API_KEY == "your_api_key_here":
        return content
    
    prompts = {
        "summary": "Improve this professional summary to be more impactful, use action verbs, and quantify achievements:",
        "experience": "Improve this job description. Use strong action verbs (Led, Architected, Optimized), add metrics:",
        "project": "Improve this project description. Highlight technical achievements and impact:"
    }
    
    prompt = prompts.get(content_type, "Improve this content:")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                QWEN_API_URL,
                headers={"Authorization": f"Bearer {QWEN_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "qwen-plus",
                    "input": {
                        "messages": [
                            {"role": "system", "content": "You are an expert resume writer. Improve the content. Return ONLY the improved text."},
                            {"role": "user", "content": f"{prompt}\n\n{content}"}
                        ]
                    },
                    "parameters": {"temperature": 0.7, "max_tokens": 500}
                }
            )
            if response.status_code == 200:
                result = response.json()
                return result.get("output", {}).get("text", content).strip()
        except Exception as e:
            print(f"AI error: {e}")
    return content

# ============ PDF Generation ============
async def generate_pdf_resume(user: dict, title: str, resume_id: str) -> str:
    pdf_path = f"generated_resumes/resume_{resume_id}.pdf"
    os.makedirs("generated_resumes", exist_ok=True)
    
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#2563eb'), spaceAfter=30, alignment=TA_CENTER)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=16, textColor=colors.HexColor('#1e40af'), spaceBefore=20, spaceAfter=10)
    normal_style = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontSize=10, leading=14, spaceAfter=6)
    
    story = []
    name = user.get("name", user.get("first_name", "") + " " + user.get("last_name", ""))
    story.append(Paragraph(name, title_style))
    
    contact = f"<b>Email:</b> {user.get('email', '')}<br/><b>Phone:</b> {user.get('phone', 'N/A')}<br/><b>Location:</b> {user.get('location', '')}"
    story.append(Paragraph(contact, normal_style))
    story.append(Spacer(1, 0.2 * inch))
    
    if user.get("summary"):
        story.append(Paragraph("Professional Summary", heading_style))
        story.append(Paragraph(user["summary"], normal_style))
        story.append(Spacer(1, 0.1 * inch))
    
    if user.get("skills"):
        story.append(Paragraph("Technical Skills", heading_style))
        skills_text = ", ".join([s.get("name", "") for s in user["skills"]])
        story.append(Paragraph(skills_text, normal_style))
        story.append(Spacer(1, 0.1 * inch))
    
    if user.get("experience"):
        story.append(Paragraph("Work Experience", heading_style))
        for exp in user["experience"]:
            exp_text = f"<b>{exp.get('position', '')}</b> at {exp.get('company', '')}<br/><i>{exp.get('start_date', '')} - {exp.get('end_date', 'Present')}</i><br/>{exp.get('description', '')}"
            story.append(Paragraph(exp_text, normal_style))
            story.append(Spacer(1, 0.1 * inch))
    
    if user.get("projects"):
        story.append(Paragraph("Projects", heading_style))
        for proj in user["projects"]:
            proj_text = f"<b>{proj.get('name', '')}</b><br/><i>Technologies: {', '.join(proj.get('technologies', []))}</i><br/>{proj.get('description', '')}"
            story.append(Paragraph(proj_text, normal_style))
            story.append(Spacer(1, 0.1 * inch))
    
    if user.get("education"):
        story.append(Paragraph("Education", heading_style))
        for edu in user["education"]:
            edu_text = f"<b>{edu.get('degree', '')}</b> in {edu.get('field_of_study', '')}<br/>{edu.get('institution', '')}<br/><i>Graduated: {edu.get('graduation_date', '')}</i>"
            story.append(Paragraph(edu_text, normal_style))
            story.append(Spacer(1, 0.1 * inch))
    
    doc.build(story)
    return pdf_path

# ============ HTML Generation ============
def generate_resume_html(user: dict, title: str = None) -> str:
    name = user.get("name", f"{user.get('first_name', '')} {user.get('last_name', '')}")

    skills_html = "".join([f'<span class="skill-tag">{s.get("name", "")}</span>' for s in user.get("skills", [])])

    experience_html = ""
    for exp in user.get("experience", []):
        experience_html += f'''
        <div class="exp-item">
            <div class="exp-header"><strong>{exp.get("position", "")}</strong> at {exp.get("company", "")} <span class="exp-date">{exp.get("start_date", "")} - {exp.get("end_date", "Present")}</span></div>
            <p>{exp.get("description", "")}</p>
        </div>'''

    projects_html = ""
    for proj in user.get("projects", []):
        projects_html += f'''
        <div class="project-item">
            <div class="project-header"><strong>{proj.get("name", "")}</strong> <span class="project-date">{proj.get("start_date", "")} - {proj.get("end_date", "Present")}</span></div>
            <div class="project-tech">Technologies: {", ".join(proj.get("technologies", []))}</div>
            <p>{proj.get("description", "")}</p>
            {f'<a href="{proj.get("link", "")}" target="_blank">🔗 Project Link</a>' if proj.get("link") else ''}
        </div>'''

    education_html = ""
    for edu in user.get("education", []):
        education_html += f'''
        <div class="edu-item">
            <div class="edu-header"><strong>{edu.get("degree", "")}</strong> in {edu.get("field_of_study", "")} <span class="edu-date">{edu.get("graduation_date", "")}</span></div>
            <div>{edu.get("institution", "")}</div>
        </div>'''

    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title or name} - Resume</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; padding: 40px; }}
        .resume {{ max-width: 900px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; padding: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.5rem; margin-bottom: 10px; }}
        .contact {{ display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 15px; }}
        .body {{ padding: 40px; }}
        .section {{ margin-bottom: 30px; }}
        .section h2 {{ color: #2563eb; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; margin-bottom: 20px; }}
        .skill-tag {{ display: inline-block; background: #e0e7ff; padding: 6px 12px; border-radius: 20px; margin: 5px; font-size: 14px; }}
        .exp-item, .project-item, .edu-item {{ margin-bottom: 20px; }}
        .exp-header, .project-header, .edu-header {{ font-weight: bold; margin-bottom: 5px; }}
        .exp-date, .project-date, .edu-date {{ float: right; color: #64748b; font-weight: normal; }}
        .project-tech {{ color: #64748b; font-size: 14px; margin-bottom: 8px; }}
        .summary {{ background: #f8fafc; padding: 20px; border-radius: 8px; line-height: 1.6; }}
        @media (max-width: 600px) {{ body {{ padding: 20px; }} .header {{ padding: 20px; }} .body {{ padding: 20px; }} .exp-date {{ float: none; display: block; }} }}
    </style>
</head>
<body>
    <div class="resume">
        <div class="header">
            <h1>{name}</h1>
            <div class="title">{user.get("professional_title", "Professional")}</div>
            <div class="contact">📧 {user.get("email", "")} {f'📞 {user.get("phone", "")}' if user.get("phone") else ""} {f'📍 {user.get("location", "")}' if user.get("location") else ""}</div>
        </div>
        <div class="body">
            {f'<div class="section"><h2>Professional Summary</h2><div class="summary">{user.get("summary", "")}</div></div>' if user.get("summary") else ""}
            {f'<div class="section"><h2>Technical Skills</h2><div>{skills_html}</div></div>' if skills_html else ""}
            {f'<div class="section"><h2>Work Experience</h2>{experience_html}</div>' if experience_html else ""}
            {f'<div class="section"><h2>Projects</h2>{projects_html}</div>' if projects_html else ""}
            {f'<div class="section"><h2>Education</h2>{education_html}</div>' if education_html else ""}
        </div>
    </div>
</body>
</html>'''

# ============ API Endpoints ============
@app.get("/")
async def root():
    return {"message": "AI Resume Builder API", "version": "2.0", "status": "running"}

@app.get("/app")
async def serve_frontend():
    index_path = Path("frontend/index.html")
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Frontend not found</h1>", status_code=404)

@app.get("/health")
async def health():
    return {"status": "healthy", "users": len(users_db), "resumes": len(resumes_db)}

@app.post("/api/users/")
async def create_user(user: UserCreate):
    user_id = str(uuid.uuid4())
    users_db[user_id] = {
        "id": user_id, "first_name": user.first_name, "last_name": user.last_name,
        "name": f"{user.first_name} {user.last_name}", "email": user.email,
        "phone": user.phone, "location": user.location, "professional_title": user.professional_title,
        "linkedin": user.linkedin, "github": user.github, "portfolio": user.portfolio,
        "summary": user.summary, "skills": [], "experience": [], "education": [], "projects": [],
        "created_at": datetime.now().isoformat()
    }
    return users_db[user_id]

@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    if user_id not in users_db:
        raise HTTPException(404, "User not found")
    return users_db[user_id]

@app.put("/api/users/{user_id}")
async def update_user(user_id: str, user: UserCreate):
    if user_id not in users_db:
        raise HTTPException(404, "User not found")
    users_db[user_id].update({
        "first_name": user.first_name, "last_name": user.last_name,
        "name": f"{user.first_name} {user.last_name}", "email": user.email,
        "phone": user.phone, "location": user.location, "professional_title": user.professional_title,
        "linkedin": user.linkedin, "github": user.github, "portfolio": user.portfolio,
        "summary": user.summary, "updated_at": datetime.now().isoformat()
    })
    return users_db[user_id]

@app.post("/api/users/{user_id}/skills")
async def add_skills(user_id: str, skills: List[SkillItem]):
    if user_id not in users_db:
        raise HTTPException(404, "User not found")
    for skill in skills:
        users_db[user_id]["skills"].append(skill.dict())
    return {"skills": users_db[user_id]["skills"]}

@app.post("/api/users/{user_id}/experience")
async def add_experience(user_id: str, experience: List[ExperienceItem]):
    if user_id not in users_db:
        raise HTTPException(404, "User not found")
    for exp in experience:
        users_db[user_id]["experience"].append(exp.dict())
    return {"experience": users_db[user_id]["experience"]}

@app.post("/api/users/{user_id}/education")
async def add_education(user_id: str, education: List[EducationItem]):
    if user_id not in users_db:
        raise HTTPException(404, "User not found")
    for edu in education:
        users_db[user_id]["education"].append(edu.dict())
    return {"education": users_db[user_id]["education"]}

@app.post("/api/users/{user_id}/projects")
async def add_projects(user_id: str, projects: List[ProjectItem]):
    if user_id not in users_db:
        raise HTTPException(404, "User not found")
    for proj in projects:
        users_db[user_id]["projects"].append(proj.dict())
    return {"projects": users_db[user_id]["projects"]}

@app.post("/api/resumes/generate")
async def generate_resume(request: ResumeGenerateRequest):
    if request.user_id not in users_db:
        raise HTTPException(404, "User not found")
    
    user = users_db[request.user_id]
    resume_id = str(uuid.uuid4())
    
    # Update user data
    if request.summary:
        user["summary"] = await enhance_with_ai(request.summary, "summary") if QWEN_API_KEY else request.summary
    if request.skills:
        user["skills"] = [s.dict() for s in request.skills]
    if request.experience:
        exp_list = []
        for exp in request.experience:
            exp_dict = exp.dict()
            if exp_dict.get("description") and QWEN_API_KEY:
                exp_dict["description"] = await enhance_with_ai(exp_dict["description"], "experience")
            exp_list.append(exp_dict)
        user["experience"] = exp_list
    if request.projects:
        proj_list = []
        for proj in request.projects:
            proj_dict = proj.dict()
            if proj_dict.get("description") and QWEN_API_KEY:
                proj_dict["description"] = await enhance_with_ai(proj_dict["description"], "project")
            proj_list.append(proj_dict)
        user["projects"] = proj_list
    if request.education:
        user["education"] = [e.dict() for e in request.education]
    
    # Generate files
    pdf_path = await generate_pdf_resume(user, request.title or "My Resume", resume_id)
    html = generate_resume_html(user, request.title)
    
    os.makedirs("generated_resumes", exist_ok=True)
    html_path = f"generated_resumes/resume_{resume_id}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    resumes_db[resume_id] = {
        "id": resume_id, "user_id": request.user_id, "title": request.title,
        "html_path": html_path, "pdf_path": pdf_path, "created_at": datetime.now().isoformat()
    }
    
    return {
        "resume_id": resume_id, "message": "Resume generated successfully!",
        "pdf_url": f"/api/resumes/download_pdf/{resume_id}",
        "html_url": f"/api/resumes/download/{resume_id}"
    }

@app.get("/api/resumes/download/{resume_id}")
async def download_html(resume_id: str):
    if resume_id not in resumes_db:
        raise HTTPException(404, "Resume not found")
    html_path = resumes_db[resume_id]["html_path"]
    if os.path.exists(html_path):
        return FileResponse(html_path, media_type="text/html", filename=f"resume_{resume_id}.html")
    raise HTTPException(404, "File not found")

@app.get("/api/resumes/download_pdf/{resume_id}")
async def download_pdf(resume_id: str):
    if resume_id not in resumes_db:
        raise HTTPException(404, "Resume not found")
    pdf_path = resumes_db[resume_id]["pdf_path"]
    if os.path.exists(pdf_path):
        return FileResponse(pdf_path, media_type="application/pdf", filename=f"resume_{resume_id}.pdf")
    raise HTTPException(404, "PDF not found")

@app.get("/api/resumes/history/{user_id}")
async def get_history(user_id: str):
    if user_id not in users_db:
        raise HTTPException(404, "User not found")
    return [{"id": rid, "title": data.get("title", "Untitled"), "created_at": data["created_at"]} for rid, data in resumes_db.items() if data["user_id"] == user_id]

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🤖 AI Resume Builder - Server Running")
    print("=" * 60)
    print(f"📱 Frontend: http://localhost:8000/app")
    print(f"📚 API Docs: http://localhost:8000/docs")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")