# Simple LMS Backend

Aplikasi Learning Management System (LMS) backend yang dibangun dengan Django dan Django Ninja.

## Table of Contents

- [Teknologi](#teknologi)
- [Prerequisites](#prerequisites)
- [Setup Project](#setup-project)
- [Menjalankan Project](#menjalankan-project)
- [Testing API](#testing-api)
- [Project Structure](#project-structure)

## Teknologi

- **Django 5.2+** - Web framework
- **Django Ninja** - REST API framework
- **PyJWT** - JWT authentication
- **Redis** - Caching dan session management
- **SQLite** - Database
- **Docker & Docker Compose** - Containerization

## Prerequisites

Pastikan Anda sudah menginstal:

- **Docker** ([Download Docker Desktop](https://www.docker.com/products/docker-desktop))
- **Docker Compose** (biasanya sudah termasuk dengan Docker Desktop)
- **Git**

Untuk development tanpa Docker, memerlukan:

- Python 3.11+
- pip (Python package manager)

## Setup Project

### Dengan Docker (Recommended)

1. **Clone repository**

   ```bash
   git clone <repository-url>
   cd uas-simple-lms-backend
   ```

2. **Setup environment variables** (optional)

   - (opsional)Buat file `.env` untuk konfigurasi tambahan
   - Configurasi Redis dan database dapat diatur di `docker-compose.yml`

3. **Build dan jalankan dengan Docker Compose**

   ```bash
   docker compose up --build
   ```

   Perintah ini akan:

   - Build image Docker untuk aplikasi Django
   - Menjalankan Redis container
   - Menjalankan Django application
   - Otomatis menjalankan migrations
   - Otomatis membuat seed data

4. **Verifikasi aplikasi berjalan**
   ```
   Server akan berjalan di: http://localhost:8000
   Redis akan berjalan di: localhost:6379
   ```

### Tanpa Docker (Local Development)

1. **Clone repository**

   ```bash
   git clone <repository-url>
   cd uas-simple-lms-backend
   ```

2. **Buat virtual environment**

   ```bash
   # Windows
   python -m venv uas-venv
   uas-venv\Scripts\activate

   # Linux/Mac
   python3 -m venv uas-venv
   source uas-venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup database**

   ```bash
   python manage.py migrate
   python manage.py seed_data
   ```

5. **Jalankan server**

   ```bash
   python manage.py runserver
   ```

   Server akan berjalan di: `http://localhost:8000`

## Menjalankan Project

### Docker Compose

**Menjalankan project:**

```bash
docker compose up --build
```

**Options:**

- `--build` : Rebuild image jika ada perubahan di requirements atau Dockerfile
- `-d` : Jalankan di background mode
  ```bash
  docker compose up --build -d
  ```

**Menghentikan project:**

```bash
docker compose down
```

**Melihat logs:**

```bash
docker compose logs -f web
```

**Jalankan command di container:**

```bash
docker compose exec web python manage.py <command>
```

### Local Development

```bash
# Aktifkan virtual environment
# Windows
uas-venv\Scripts\activate
# Linux/Mac
source uas-venv/bin/activate

# Jalankan server
python manage.py runserver
```

**Setup Redis (diperlukan untuk caching):**

Jika menggunakan local development, perlu menjalankan Redis secara terpisah:

```bash
# Windows (menggunakan WSL atau Redis untuk Windows)
redis-server

# Linux/Mac
redis-server
```

## Testing API

### Akses Dokumentasi Ninja

Django Ninja menyediakan dokumentasi API interaktif otomatis. Akses dari browser:

1. **Swagger UI Documentation**

   ```
   http://localhost:8000/api/docs
   ```

   - Dokumentasi interaktif dengan Swagger UI
   - Dapat langsung test API dari browser
   - Request/response examples

2. **ReDoc Documentation** (alternatif)

   ```
   http://localhost:8000/api/redoc
   ```

   - Dokumentasi dengan ReDoc
   - Format yang lebih detail dan organized

3. **OpenAPI Schema** (JSON)
   ```
   http://localhost:8000/api/openapi.json
   ```
   - Raw OpenAPI schema dalam format JSON

### Testing API dengan Tools

#### Menggunakan Swagger UI (Recommended)

1. Buka `http://localhost:8000/api/docs` di browser
2. Expand endpoint yang ingin ditest
3. Klik "Try it out"
4. Masukkan parameter/body jika diperlukan
5. Klik "Execute"
6. Lihat response

#### Menggunakan cURL

```bash
# Contoh GET request
curl http://localhost:8000/api/users/

# Contoh POST request dengan authentication
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'

# Request dengan JWT token
curl http://localhost:8000/api/users/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### Menggunakan Postman

1. Download dan buka [Postman](https://www.postman.com/downloads/)
2. Import OpenAPI schema:
   - Klik "Import"
   - Pilih "Link"
   - Paste: `http://localhost:8000/api/openapi.json`
3. Postman akan otomatis membuat collection
4. Test setiap endpoint

#### Menggunakan Python requests

```python
import requests

# Login
response = requests.post('http://localhost:8000/api/login/',
    json={'username': 'admin', 'password': 'admin'}
)
token = response.json()['access']

# Get users dengan token
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:8000/api/users/',
    headers=headers
)
print(response.json())
```

### Common Testing Scenarios

**1. Authentication Test**

```
Endpoint: POST /api/login/
Body: {"username": "admin", "password": "admin"}
Response: Token yang dapat digunakan untuk request berikutnya
```

**2. CRUD Operations**

- Test GET, POST, PUT, DELETE untuk setiap resource
- Sesuaikan dengan endpoint yang tersedia

**3. Permission Check**

- Test dengan user yang berbeda
- Verifikasi RBAC (Role-Based Access Control) berfungsi dengan baik

## Project Structure

```
uas-simple-lms-backend/
├── lms/                          # Main application
│   ├── api.py                    # API endpoints (Ninja router)
│   ├── models.py                 # Database models
│   ├── schemas.py                # Pydantic schemas untuk request/response
│   ├── views.py                  # View functions
│   ├── auth_utils.py             # Authentication utilities
│   ├── jwt_auth.py               # JWT authentication handler
│   ├── rbac.py                   # Role-Based Access Control
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py      # Script untuk populate sample data
│   ├── migrations/               # Database migrations
│   └── tests.py                  # Unit tests
│
├── simple_lms/                   # Django project settings
│   ├── settings.py               # Django settings
│   ├── urls.py                   # URL configuration
│   ├── asgi.py                   # ASGI configuration
│   └── wsgi.py                   # WSGI configuration
│
├── docker-compose.yml            # Docker Compose configuration
├── Dockerfile                    # Docker image definition
├── docker-entrypoint.sh          # Startup script untuk container
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Troubleshooting

### Port 8000 sudah digunakan

```bash
# Linux/Mac: Lihat process yang menggunakan port 8000
lsof -i :8000

# Windows: Gunakan netstat
netstat -ano | findstr :8000

# Kill process atau gunakan port lain
python manage.py runserver 8001
```

### Redis connection error

- Pastikan Redis sudah running
- Cek `REDIS_HOST` dan `REDIS_PORT` di settings.py
- Jika menggunakan Docker, Redis service harus healthy

### Database migration error

```bash
# Reset database (hati-hati, akan menghapus semua data)
python manage.py flush
python manage.py migrate
python manage.py seed_data
```

### Docker build failed

```bash
# Rebuild tanpa cache
docker compose build --no-cache
docker compose up
```

## Development Tips

- Dokumentasi Django Ninja: https://django-ninja.dev/
- Dokumentasi Django: https://docs.djangoproject.com/
- Docs Pydantic: https://docs.pydantic.dev/

## License

[Specify your license here]
