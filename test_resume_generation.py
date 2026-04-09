"""
Тест для проверки генерации резюме
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_resume_generation():
    print("=" * 60)
    print("ТЕСТ: Генерация резюме")
    print("=" * 60)
    
    # Шаг 1: Создаем пользователя
    print("\n1. Создаем пользователя...")
    user_data = {
        "first_name": "Иван",
        "last_name": "Петров",
        "email": "ivan.petrov@example.com",
        "phone": "+7-999-123-4567",
        "location": "Москва, Россия",
        "professional_title": "Senior Python Developer",
        "linkedin": "https://linkedin.com/in/ivanpetrov",
        "github": "https://github.com/ivanpetrov",
        "summary": "Опытный Python разработчик с 5-летним стажем..."
    }
    
    response = requests.post(f"{BASE_URL}/api/users/", json=user_data)
    if response.status_code != 200:
        print(f"❌ Ошибка создания пользователя: {response.status_code}")
        print(response.text)
        return
    
    user = response.json()
    user_id = user["id"]
    print(f"✅ Пользователь создан с ID: {user_id}")
    
    # Шаг 2: Генерируем резюме
    print("\n2. Генерируем резюме...")
    resume_data = {
        "user_id": user_id,
        "title": "Python Developer Resume",
        "summary": "Experienced Python developer specializing in backend development",
        "skills": [
            {"name": "Python", "level": "Expert"},
            {"name": "FastAPI", "level": "Advanced"},
            {"name": "PostgreSQL", "level": "Advanced"}
        ],
        "experience": [
            {
                "company": "Tech Corp",
                "position": "Senior Python Developer",
                "start_date": "Jan 2020",
                "end_date": "Present",
                "location": "Moscow",
                "description": "Led development of microservices architecture"
            }
        ],
        "projects": [
            {
                "name": "AI Resume Builder",
                "description": "Built an AI-powered resume builder using FastAPI and React",
                "technologies": ["Python", "FastAPI", "React"],
                "link": "https://github.com/project",
                "start_date": "Jan 2024",
                "end_date": "Present"
            }
        ],
        "education": [
            {
                "institution": "Moscow State University",
                "degree": "Bachelor of Science",
                "field_of_study": "Computer Science",
                "graduation_date": "Jun 2019"
            }
        ],
        "job_description": None
    }
    
    response = requests.post(f"{BASE_URL}/api/resumes/generate", json=resume_data)
    if response.status_code != 200:
        print(f"❌ Ошибка генерации резюме: {response.status_code}")
        print(response.text)
        return
    
    result = response.json()
    print(f"✅ Резюме сгенерировано!")
    print(f"   Resume ID: {result['resume_id']}")
    print(f"   PDF URL: {result['pdf_url']}")
    print(f"   Message: {result['message']}")
    
    # Шаг 3: Проверяем, что PDF доступен для скачивания
    print("\n3. Проверяем доступность PDF...")
    pdf_url = f"{BASE_URL}{result['pdf_url']}"
    response = requests.get(pdf_url)
    
    if response.status_code == 200:
        print(f"✅ PDF файл доступен для скачивания!")
        print(f"   Размер: {len(response.content)} байт")
    else:
        print(f"❌ PDF файл недоступен: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("ТЕСТ ЗАВЕРШЕН УСПЕШНО! ✅")
    print("=" * 60)
    print("\nТеперь откройте браузер и перейдите по адресу:")
    print(f"http://localhost:8000/app")
    print("\nИли скачайте PDF напрямую:")
    print(pdf_url)

if __name__ == "__main__":
    try:
        test_resume_generation()
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
