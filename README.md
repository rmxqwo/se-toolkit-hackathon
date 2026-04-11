# 🤖 AI Resume Builder

## One-line description
AI-powered resume builder that helps job seekers create professional, ATS-friendly resumes tailored to specific job descriptions.

## Demo

![Resume Builder Interface](screenshots/interface.png)
![Generated Resume](screenshots/resume.png)

## Product Context

### End users
Job seekers, students, and professionals looking to create or improve their resumes for job applications.

### Problem
Writing a professional resume is time-consuming and challenging. Many people struggle with:
- Formatting and design
- Using action verbs and quantifiable achievements
- Tailoring resumes for specific job descriptions
- Making resumes ATS-friendly

### Solution
AI Resume Builder solves this by:
- Providing an intuitive web interface to enter personal information
- Using AI to polish and improve resume content
- Optimizing resumes for specific job descriptions
- Generating professional PDF/HTML resumes instantly

## Features

### Implemented (Version 1)
- ✅ User profile management (personal info, skills, experience, education)
- ✅ AI-powered resume content polishing
- ✅ Professional PDF generation via ReportLab
- ✅ Resume history tracking
- ✅ Job description optimization

### Implemented (Version 2)
- ✅ Interview simulation with AI
- ✅ Keyword match scoring
- ✅ Multiple resume templates
- ✅ Docker containerization
- ✅ Deployed production version
- ✅ One-click deployment script

### Not yet implemented
- ⬜ Social media integration
- ⬜ Export to Word/Google Docs
- ⬜ Collaborative editing
- ⬜ Resume score analytics

## Usage

### For End Users (Web Application)

1. **Create Profile**
   - Enter your personal information
   - Add skills, work experience, and education

2. **Generate Resume**
   - Click "Generate Resume" button
   - AI will polish your content
   - Download as PDF or HTML

3. **Optimize for Job**
   - Paste job description
   - Click "Optimize"
   - Get keyword match score
   - Download tailored resume

4. **Practice Interview**
   - Start interview simulation
   - Answer AI-generated questions
   - Receive feedback and scores

### For Developers (Local Setup)

#### Prerequisites
- Python 3.11+
- PostgreSQL 14+ (or SQLite for development)
- Docker (optional)

#### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/se-toolkit-hackathon.git
cd se-toolkit-hackathon

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run database migrations
python -m app.db.init_db

# Start application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000