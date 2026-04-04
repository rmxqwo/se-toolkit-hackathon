# se-toolkit-hackathon
CareerMate - AI Resume Builder & Interview Coach

User → Telegram Bot → FastAPI Backend → PostgreSQL → Qwen AI
                                                    ↓
                                            Resume Generator
                                                    ↓
                                            PDF File Output


Version 1 - Core Features

Command	What it does	Example

/start	Create profile, welcome message	Hi! Let's build your resume. Tell me about yourself.

/skills	Add your skills	/skills Python, SQL, FastAPI, Docker

/experience	Add work/project experience	/experience Built e-commerce API with FastAPI

/education	Add education	/education BSc Computer Science, Innopolis University, 2026

/generate	Create resume based on your data	Returns a PDF file with professional resume

/view	Show your current profile	Displays all stored info about you

