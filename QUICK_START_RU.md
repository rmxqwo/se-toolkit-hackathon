# 🚀 Быстрый старт - Деплой на VM через Docker Compose

## 📦 Что было создано

Для деплоя вашего приложения AI Resume Builder на виртуальную машину были созданы следующие файлы:

### Docker-файлы:
1. **`Dockerfile`** - образ приложения для контейнеризации
2. **`docker-compose.yml`** - конфигурация для запуска приложения + PostgreSQL
3. **`.dockerignore`** - исключения для Docker (как .gitignore)
4. **`app/db/init_db.py`** - скрипт инициализации базы данных
5. **`deploy.sh`** - скрипт автоматического деплоя
6. **`.env.production`** - пример конфигурации для production
7. **`DEPLOYMENT.md`** - подробная инструкция по деплою

## 🎯 Быстрый старт (5 минут)

### Шаг 1: Подготовьте VM

Установите Docker на вашу виртуальную машину (Ubuntu/Debian):

```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### Шаг 2: Загрузите код на VM

```bash
# На вашей VM
git clone https://github.com/YOUR_USERNAME/se-toolkit-hackathon.git
cd se-toolkit-hackathon
```

### Шаг 3: Настройте .env файл

```bash
# Скопируйте production конфиг
cp .env.production .env

# Отредактируйте .env - ОБЯЗАТЕЛЬНО укажите:
nano .env
```

**Минимальные требования для .env:**
```env
POSTGRES_PASSWORD=ваш_секьюр пароль
QWEN_API_KEY=ваш_api_ключ_от_qwen
DEBUG=False
```

### Шаг 4: Запустите деплой

```bash
# Сделайте скрипт исполняемым
chmod +x deploy.sh

# Запустите деплой
./deploy.sh
```

**Или вручную:**
```bash
docker compose up -d --build
```

### Шаг 5: Проверьте работу

```bash
# Проверьте статус контейнеров
docker compose ps

# Проверьте health endpoint
curl http://localhost:8000/health

# Откройте в браузере
# http://YOUR_VM_IP:8000
```

## 📊 Основные команды

```bash
# Запустить
docker compose up -d

# Посмотреть логи
docker compose logs -f

# Остановить
docker compose down

# Перезапустить
docker compose restart

# Обновить код
git pull
docker compose down
docker compose up -d --build
```

## 🔧 Архитектура

```
┌──────────────────────────────────┐
│  Virtual Machine                 │
│                                  │
│  ┌────────────────────────────┐  │
│  │  docker-compose.yml        │  │
│  │                            │  │
│  │  ┌──────────────────┐     │  │
│  │  │  PostgreSQL 15   │     │  │
│  │  │  (port 5432)     │     │  │
│  │  └────────┬─────────┘     │  │
│  │           │                │  │
│  │           ▼                │  │
│  │  ┌──────────────────┐     │  │
│  │  │  FastAPI App     │     │  │
│  │  │  (port 8000)     │     │  │
│  │  └──────────────────┘     │  │
│  └────────────────────────────┘  │
│                                  │
│  Доступ извне:                   │
│  http://VM_IP:8000              │
└──────────────────────────────────┘
```

## 📝 Что дальше?

1. **Настройте Nginx** (опционально, для production)
   - Reverse proxy для порта 8000
   - SSL сертификат от Let's Encrypt
   
2. **Настройте файрвол**
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 8000/tcp
   sudo ufw enable
   ```

3. **Настройте бэкапы БД**
   ```bash
   docker compose exec postgres pg_dump -U postgres resume_builder > backup.sql
   ```

## 📚 Подробная документация

Полную инструкцию по деплою, настройке Nginx, SSL и решению проблем смотрите в:
- **`DEPLOYMENT.md`** - полная инструкция по деплою

## ❓ Troubleshooting

### Контейнер не запускается?
```bash
docker compose logs app
docker compose logs postgres
```

### Ошибка БД?
```bash
docker compose restart postgres
docker compose run --rm migrate
```

### Порт занят?
Измените порт в `.env`:
```env
APP_PORT=8080
```

## ✅ Чеклист перед деплоем

- [ ] Docker установлен на VM
- [ ] Код загружен через git clone
- [ ] Файл `.env` настроен (особенно POSTGRES_PASSWORD и QWEN_API_KEY)
- [ ] DEBUG=False в production
- [ ] Запущен docker compose up -d --build
- [ ] Health check проходит (curl http://localhost:8000/health)
- [ ] Файрвол настроен (только порты 22 и 8000)

## 🎉 Готово!

Ваше приложение AI Resume Builder успешно задеплоено на виртуальную машину!

**Ссылка:** http://YOUR_VM_IP:8000
