# AI Resume Builder

A professional resume builder powered by Qwen AI for content optimization, job description matching, and interview simulation.

## Features

### Current (v1)
- **User Profile Management** - Store personal info, skills, experience, education
- **AI-Powered Resume Polishing** - Improve resume content with Qwen AI
- **Professional PDF Generation** - Download ATS-friendly resume PDFs via ReportLab
- **Resume History** - Track all generated resume versions
- **Job Description Optimization** - Tailor resume to match specific job postings

### Upcoming (v2)
- **Interview Simulation** - Practice with AI-powered mock interviews
- **Keyword Analysis** - See how well your resume matches job requirements
- **Templates** - Multiple resume designs

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Plain HTML/CSS/JS (no frameworks) |
| Backend | FastAPI (Python 3.11+) |
| Database | PostgreSQL + SQLAlchemy ORM |
| AI | Qwen (DashScope API) |
| PDF | ReportLab |

---

## Quick Start

### Prerequisites

1. **Python 3.11+**
2. **PostgreSQL 14+**
3. **Qwen API Key** - Get from [DashScope Console](https://dashscope.console.aliyun.com/)

### Step 1: Install PostgreSQL (Windows)

```powershell
# Download from: https://www.postgresql.org/download/windows/
# Or use Chocolatey:
choco install postgresql

# Start PostgreSQL service
net start postgresql-x64-16

# Create database
psql -U postgres
CREATE DATABASE resume_builder;
\q
```

### Step 2: Setup Python Environment

```powershell
# Navigate to project
cd se-toolkit-hackathon

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment

```powershell
# Copy example env file
copy .env.example .env

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

---

## Project Structure

```
se-toolkit-hackathon/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Settings & env config
│   ├── db.py                   # Database setup & sessions
│   ├── api/
│   │   ├── __init__.py
│   │   ├── users.py            # User CRUD endpoints
│   │   ├── resumes.py          # Resume generation & optimization
│   │   └── interview.py        # Interview simulation
│   ├── core/
│   │   ├── __init__.py
│   │   └── rate_limiter.py     # Rate limiting middleware
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py             # Base model & mixins
│   │   ├── user.py             # UserProfile model
│   │   └── resume.py           # ResumeHistory, Skill, Experience, Education
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── resume.py           # Pydantic request/response schemas
│   └── services/
│       ├── __init__.py
│       ├── qwen.py             # Qwen AI API integration
│       └── pdf_generator.py    # ReportLab PDF generation
├── frontend/
│   ├── index.html              # Main HTML page
│   └── static/
│       ├── css/style.css       # Styles
│       └── js/app.js           # Frontend JavaScript
├── generated_pdfs/             # Output PDF directory
├── requirements.txt
├── .env.example
├── .env
└── README.md
```

---

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
