# 🐳 Деплой AI Resume Builder на виртуальную машину через Docker Compose

## 📋 Предварительные требования

### На вашей виртуальной машине должно быть установлено:

1. **Docker** (версия 20.10+)
2. **Docker Compose** (версия 2.0+)
3. **Git**

### Установка Docker и Docker Compose (Ubuntu/Debian):

```bash
# Обновить пакеты
sudo apt update

# Установить необходимые пакеты
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Добавить GPG ключ Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Добавить репозиторий Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Установить Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Добавить пользователя в группу docker (чтобы запускать без sudo)
sudo usermod -aG docker $USER
newgrp docker

# Проверить установку
docker --version
docker compose version
```

## 🚀 Пошаговая инструкция по деплою

### Шаг 1: Клонировать репозиторий на VM

```bash
# Клонировать репозиторий
git clone https://github.com/YOUR_USERNAME/se-toolkit-hackathon.git
cd se-toolkit-hackathon
```

### Шаг 2: Настроить переменные окружения

```bash
# Создать файл .env из примера
cp .env.example .env

# Открыть для редактирования
nano .env
```

**Пример конфигурации .env для production:**

```env
# PostgreSQL Database
POSTGRES_PASSWORD=your_secure_password_here
DATABASE_URL=postgresql+asyncpg://postgres:your_secure_password_here@postgres:5432/resume_builder

# Qwen API (DashScope) - Получите ключ: https://dashscope.console.aliyun.com/
QWEN_API_KEY=your_actual_api_key_here
QWEN_MODEL=qwen-plus

# Application Settings
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=False

# Rate Limiting (запросов в минуту)
RATE_LIMIT_PER_MINUTE=30

# PDF Settings
PDF_DEFAULT_FONT=Helvetica
PDF_PAGE_SIZE=A4

# Docker Compose Settings
DB_PORT=5432
APP_PORT=8000
```

⚠️ **ВАЖНО:**
- Замените `your_secure_password_here` на надёжный пароль
- Замените `your_actual_api_key_here` на ваш ключ API Qwen
- В production установите `DEBUG=False`

### Шаг 3: Собрать и запустить контейнеры

```bash
# Собрать и запустить все сервисы (в фоновом режиме)
docker compose up -d --build

# Посмотреть логи
docker compose logs -f

# Посмотреть статус контейнеров
docker compose ps
```

### Шаг 4: Проверить работу приложения

```bash
# Проверить health endpoint
curl http://localhost:8000/health

# Или открыть в браузере
# http://YOUR_VM_IP:8000
```

## 📊 Основные команды Docker Compose

### Запуск:
```bash
docker compose up -d              # Запустить в фоне
docker compose up -d --build      # Пересобрать и запустить
```

### Остановка:
```bash
docker compose down               # Остановить контейнеры
docker compose down -v            # Остановить и удалить volumes (БД будет удалена!)
```

### Логи:
```bash
docker compose logs -f            # Все логи
docker compose logs -f app        # Логи приложения
docker compose logs -f postgres   # Логи базы данных
```

### Перезапуск:
```bash
docker compose restart            # Перезапустить все
docker compose restart app        # Перезапустить только приложение
```

### Статус:
```bash
docker compose ps                 # Статус контейнеров
docker compose stats              # Использование ресурсов
```

### Обновление кода:
```bash
git pull                          # Получить последние изменения
docker compose down               # Остановить
docker compose up -d --build      # Пересобрать и запустить
```

## 🔧 Архитектура контейнеров

```
┌─────────────────────────────────────────┐
│         Docker Compose Network          │
│                                         │
│  ┌──────────────────┐                   │
│  │   PostgreSQL 15  │ ◄── Port 5432     │
│  │   (postgres)     │                   │
│  └────────┬─────────┘                   │
│           │                             │
│           ▼                             │
│  ┌──────────────────┐                   │
│  │   FastAPI App    │ ◄── Port 8000     │
│  │   (app)          │                   │
│  └──────────────────┘                   │
│                                         │
└─────────────────────────────────────────┘
```

## 🔐 Настройка файрвола (опционально)

Если нужно ограничить доступ только по порту 8000:

```bash
# UFW (Ubuntu Firewall)
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 8000/tcp    # Приложение
sudo ufw enable

# Или iptables
sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

## 🌐 Настройка Nginx как reverse proxy (опционально)

Если хотите использовать домен и SSL:

```bash
# Установить Nginx
sudo apt install nginx

# Создать конфигурацию
sudo nano /etc/nginx/sites-available/resume-builder
```

**Пример конфигурации Nginx:**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Активировать сайт
sudo ln -s /etc/nginx/sites-available/resume-builder /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Для SSL используйте Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 🐛 Решение проблем

### Контейнер не запускается:
```bash
# Посмотреть логи
docker compose logs app

# Проверить, что БД готова
docker compose logs postgres
```

### Ошибка подключения к БД:
```bash
# Убедиться, что postgres запущен
docker compose ps postgres

# Перезапустить БД
docker compose restart postgres
```

### Порт уже используется:
```bash
# Проверить, что использует порт 8000
sudo lsof -i :8000

# Изменить порт в .env
APP_PORT=8080
```

### Ошибка миграции БД:
```bash
# Запустить миграцию вручную
docker compose run --rm migrate
```

## 📁 Структура файлов для деплоя

```
se-toolkit-hackathon/
├── .env                        # Ваши настройки (НЕ коммитить в Git!)
├── .env.example               # Пример настроек
├── docker-compose.yml         # Конфигурация контейнеров
├── Dockerfile                 # Образ приложения
├── .dockerignore              # Исключения для Docker
├── app/                       # Backend код
├── frontend/                  # Frontend код
├── generated_pdfs/            # Сгенерированные PDF
└── generated_resumes/         # Сгенерированные резюме
```

## 💾 Бэкап базы данных

```bash
# Создать бэкап
docker compose exec postgres pg_dump -U postgres resume_builder > backup.sql

# Восстановить из бэкапа
cat backup.sql | docker compose exec -T postgres psql -U postgres resume_builder
```

## 📈 Мониторинг

```bash
# Статус контейнеров
docker compose ps

# Использование ресурсов
docker stats

# Логи в реальном времени
docker compose logs -f --tail=100
```

## 🔄 Автоматическое обновление (опционально)

Создайте скрипт `update.sh`:

```bash
#!/bin/bash
cd /path/to/se-toolkit-hackathon
git pull
docker compose down
docker compose up -d --build
docker system prune -f
```

Сделайте его исполняемым:
```bash
chmod +x update.sh
```

## ✅ Чеклист перед деплоем

- [ ] Установлен Docker и Docker Compose
- [ ] Склонирован репозиторий
- [ ] Настроен файл `.env` с правильными паролями и API ключами
- [ ] `DEBUG=False` в production
- [ ] Запущены контейнеры: `docker compose up -d --build`
- [ ] Проверен health endpoint: `curl http://localhost:8000/health`
- [ ] Настроен файрвол (только нужные порты)
- [ ] Настроен Nginx и SSL (если нужно)
- [ ] Настроен бэкап базы данных

## 🎉 Готово!

После успешного деплоя ваше приложение будет доступно по адресу:
- **Локально:** http://localhost:8000
- **Внешне:** http://YOUR_VM_IP:8000 (или ваш домен)

Удачи с деплоем! 🚀
