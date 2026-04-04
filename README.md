# se-toolkit-hackathon

User → Telegram Bot → FastAPI Backend → PostgreSQL → Qwen AI
                                                    ↓
                                            Resume Generator
                                                    ↓
                                            PDF File Output


Version 1 - Core Features

Commands:

/start	Create profile, welcome message	Hi! Let's build your resume. Tell me about yourself.

/skills	Add your skills	/skills Python, SQL, FastAPI, Docker

/experience	Add work/project experience	/experience Built e-commerce API with FastAPI

/education	Add education	/education BSc Computer Science, Innopolis University, 2026

/generate	Create resume based on your data	Returns a PDF file with professional resume

/view	Show your current profile	Displays all stored info about you

Version 2 - Advanced Features

/optimize [job_link]	Optimize resume for specific job posting

/interview [role]	Start AI interview simulation for given role

/feedback	Get AI feedback on your interview answers

/improve	AI suggests improvements to your resume

/export	Download resume in multiple formats (PDF, DOCX, TXT)

/history	See all your previous resumes and interviews
