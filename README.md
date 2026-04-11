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
# Edit .env with your settings:
# - DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/resume_builder
# - QWEN_API_KEY=your_api_key_here
```

### Step 4: Run the Application

```powershell
# Start the server
python -m app.main

# Or with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open **http://localhost:8000** in your browser.

---

## API Documentation

Once running, visit **http://localhost:8000/docs** for interactive Swagger API documentation.

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/users/` | Create user profile |
| `GET` | `/api/users/{id}` | Get user profile |
| `PUT` | `/api/users/{id}` | Update user profile |
| `POST` | `/api/resumes/generate` | Generate AI-polished resume PDF |
| `POST` | `/api/resumes/optimize` | Optimize resume for job description |
| `GET` | `/api/resumes/history/{user_id}` | Get resume history |
| `GET` | `/api/resumes/download/{filename}` | Download PDF |
| `POST` | `/api/interview/start` | Start mock interview |
| `POST` | `/api/interview/answer` | Submit answer, get feedback |



## Qwen AI Prompt Structures

### 1. Resume Polishing Prompt

**System Prompt:**
```
You are an expert resume writer and career coach with 20+ years of experience.
Your task is to improve resume content to make it more impactful, professional, and ATS-friendly.

Rules:
- Use strong action verbs (Led, Architected, Optimized, Spearheaded)
- Quantify achievements with metrics where possible
- Keep descriptions concise but impactful
- Remove filler words and passive language
- Ensure consistency in tense
- Return ONLY valid JSON with no additional text
```

**User Message:**
```
Please polish this resume content and return it as valid JSON:

PROFESSIONAL SUMMARY:
{summary}

SKILLS:
{skills}

WORK EXPERIENCE:
{experience}

EDUCATION:
{education}

Return the polished content in this EXACT JSON format:
{
  "summary": "...",
  "skills": [...],
  "experience": [...],
  "education": [...]
}
```

---

### 2. Job Description Optimization Prompt

**System Prompt:**
```
You are an expert resume optimizer. Your task is to tailor a resume to match a job description perfectly.

Rules:
- Identify key skills, technologies, and qualifications from the job description
- Rewrite the summary to directly address the role requirements
- Reorder and emphasize skills that match the job requirements
- Reframe experience bullet points to highlight relevant achievements
- Add missing keywords naturally
- Calculate a keyword match score (0-100)
- Return ONLY valid JSON
```

**User Message:**
```
Optimize this resume for the following job description:

JOB DESCRIPTION:
{job_description}

CURRENT RESUME:
{resume_text}

Return the optimized resume in this EXACT JSON format:
{
  "summary": "...",
  "skills": [...],
  "experience": [...],
  "education": [...],
  "keyword_match_score": 85.5
}
```

---

### 3. Interview Simulation Prompt

**System Prompt (First Question):**
```
You are a senior hiring manager conducting a technical interview for a {role} position ({level} level).

Rules:
- Start with a question that assesses both technical knowledge and problem-solving approach
- Make it specific and practical, not theoretical
- Return ONLY valid JSON
```

**System Prompt (Feedback + Next Question):**
```
You are a senior hiring manager conducting a technical interview for a {role} position ({level} level).

Rules:
- Provide constructive, specific feedback on the candidate's answer
- Score the answer from 1-10 based on completeness, accuracy, and communication
- Ask one question at a time
- Vary question types: technical depth, system design, behavioral, problem-solving
- Be professional but encouraging
- Return ONLY valid JSON
```

**User Message:**
```
The candidate answered the previous question with:

"{answer}"

Provide feedback and ask the next question (Question #{number}).

Return in this EXACT JSON format:
{
  "feedback": "...",
  "score": 7,
  "next_question": "...",
  "is_complete": false
}
```

---

## Common Pitfalls & Solutions

### 1. CORS Issues

**Problem:** Frontend can't reach API due to CORS restrictions.

**Solution:** Already handled in `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production:** Replace `"*"` with specific origins:
```python
allow_origins=["https://yourdomain.com"]
```

---

### 2. PDF Encoding Issues

**Problem:** Special characters (emojis, non-ASCII) break PDF generation.

**Solution:** ReportLab's default fonts don't support Unicode. Options:

**Option A - Strip non-ASCII:**
```python
def clean_text(text: str) -> str:
    return text.encode('ascii', 'ignore').decode('ascii')
```

**Option B - Use Unicode fonts:**
```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
# Then use fontName='DejaVu' in styles
```

---

### 3. Async Database Calls

**Problem:** Mixing sync and async database operations causes errors.

**Solution:** Always use async patterns consistently:

```python
# ✅ Correct
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserProfile).where(UserProfile.id == user_id))
    return result.scalar_one_or_none()

# ❌ Wrong - mixing sync/async
def get_user(user_id: int):
    with Session(engine) as db:  # This blocks the event loop!
        return db.query(UserProfile).filter(UserProfile.id == user_id).first()
```

**Key Rules:**
- Use `AsyncSession` everywhere
- Never use synchronous `Session` in FastAPI async endpoints
- Use `await db.flush()` instead of `await db.commit()` for intermediate saves

---

### 4. Rate Limiting for AI API

**Problem:** Too many requests to Qwen API hit rate limits.

**Solution:** Implemented in `app/core/rate_limiter.py`:

```python
class RateLimiter:
    def __init__(self, max_requests: int = 30):
        self.max_requests = max_requests
        self.window_seconds = 60

    async def __call__(self, request: Request) -> None:
        # Sliding window check
        ...
```

**Apply to routes:**
```python
@router.post("/generate", dependencies=[Depends(rate_limiter)])
async def generate_resume(...):
    ...
```

**Production alternatives:**
- Use Redis for distributed rate limiting
- Use API gateway rate limiting (AWS, Cloudflare)
- Implement token bucket algorithm for better fairness

---

### 5. AI API Errors & Timeouts

**Problem:** Qwen API fails, returns invalid JSON, or times out.

**Solution:** Graceful degradation in `app/services/qwen.py`:

```python
async def _make_request(...) -> Optional[str]:
    try:
        response = await client.post(...)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except httpx.TimeoutException:
        logger.error("Qwen API request timed out")
        return None
    except Exception as e:
        logger.error(f"Qwen API request failed: {str(e)}")
        return None
```

**Best Practices:**
- Always return original content if AI fails (don't lose user data)
- Set reasonable timeouts (60s recommended)
- Implement retry logic with exponential backoff
- Log all errors for debugging

---

### 6. Database Connection Pool Exhaustion

**Problem:** "Too many connections" or pool timeout errors.

**Solution:** Configure pool settings in `app/db.py`:

```python
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,      # Test connections before use
    pool_size=5,             # Base pool size
    max_overflow=10,         # Max extra connections
)
```

**PostgreSQL config (`postgresql.conf`):**
```ini
max_connections = 100
```

---

### 7. Large File Uploads (PDF Storage)

**Problem:** Generated PDFs fill up disk space.

**Solutions:**
- Use cloud storage (S3, GCS, Azure Blob)
- Implement automatic cleanup after X days
- Compress PDFs before storage

```python
# Cleanup old PDFs
async def cleanup_old_pdfs(max_age_days: int = 30):
    cutoff = datetime.now() - timedelta(days=max_age_days)
    old_resumes = await db.execute(
        select(ResumeHistory).where(ResumeHistory.created_at < cutoff)
    )
    for resume in old_resumes.scalars():
        if resume.pdf_filename:
            filepath = os.path.join(PDF_DIR, resume.pdf_filename)
            if os.path.exists(filepath):
                os.remove(filepath)
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://postgres:postgres@localhost:5432/resume_builder` |
| `QWEN_API_KEY` | Your DashScope API key | *(required)* |
| `QWEN_MODEL` | Qwen model to use | `qwen-plus` |
| `APP_HOST` | Server bind address | `0.0.0.0` |
| `APP_PORT` | Server port | `8000` |
| `DEBUG` | Enable debug/reload | `False` |
| `RATE_LIMIT_PER_MINUTE` | Max requests per minute | `30` |

---

## Deployment

### Docker (Coming Soon)

```bash
docker-compose up -d
```

### Production Checklist

- [ ] Change CORS origins to specific domains
- [ ] Set `DEBUG=False`
- [ ] Use production database (not SQLite)
- [ ] Set up HTTPS
- [ ] Configure proper logging
- [ ] Set up monitoring (Prometheus, Sentry)
- [ ] Implement Redis for rate limiting & sessions
- [ ] Use cloud storage for PDFs (S3, GCS)
- [ ] Set up automated backups
- [ ] Configure CI/CD pipeline

---

## License

MIT

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

---

## Support

For issues or questions, please open an issue on the repository.
>>>>>>> fa3addd6d6f076a6d31ff7ba584a27a820a8199c
