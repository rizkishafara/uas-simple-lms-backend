from ninja import Router
from django.contrib.auth import get_user_model, authenticate
from django.http import HttpRequest
from django.core.cache import cache
from .models import Course
from .schemas import CourseSchema, CourseCreateSchema
from .jwt_auth import JWTAuth
from .auth_utils import create_jwt
from lms.rbac import require_role
from .schemas import CourseSchema, CourseCreateSchema, LoginSchema, RegisterSchema
from .utils.rate_limit import is_rate_limited

router = Router()
User = get_user_model()


@router.post("/register")
def register_user(request, data: RegisterSchema):
    user = User.objects.create_user(
        username=data.username,
        email=data.email or "",
        password=data.password,
        role=data.role or "mahasiswa",
    )
    return {"id": user.id, "username": user.username}


@router.post("/login")
def login_user(request, data: LoginSchema):
    # rate_limit

    if is_rate_limited(data.username):
        return {"error": "Terlalu banyak percobaan login. Silakan coba lagi nanti."}

    user = authenticate(username=data.username, password=data.password)
    if not user:
        return {"error": "Invalid credentials"}

    token = create_jwt(user)
    return {"token": token}


# test session
@router.get("/test-session", auth=JWTAuth())
def session_test(request: HttpRequest):
    return {
        "message": "Session is valid",
        "user_role": getattr(request, "user_role", "unknown"),
    }


def get_popular_courses():
    data = cache.get("popular_courses")
    if not data:
        data = list(
            Course.objects.order_by("-created_at").values("id", "title", "description")[
                :5
            ]
        )
        cache.set("popular_courses", data, timeout=600)  # 10 menit
    return data


@router.get("/courses", auth=JWTAuth(), response=list[CourseSchema])
def list_courses(request):
    cache_key = "courses_list"
    data = cache.get(cache_key)
    if not data:
        data = list(Course.objects.all().values())
        cache.set(cache_key, data, timeout=60)
    return data


@router.get("/courses/popular", auth=JWTAuth(), response=list[CourseSchema])
def list_popular_courses(request):
    return get_popular_courses()


@router.post("/courses", auth=JWTAuth(), response=CourseSchema)
@require_role(["admin", "dosen"])
def create_course(request, data: CourseCreateSchema):
    cache.delete("courses_list")
    cache.delete("popular_courses")
    return Course.objects.create(**data.dict())


@router.get("/courses/{course_id}", response=CourseSchema, auth=JWTAuth())
def get_course(request, course_id: int):
    return Course.objects.get(id=course_id)


@router.put("/courses/{course_id}", auth=JWTAuth(), response=CourseSchema)
@require_role(["admin", "dosen"])
def update_course(request, course_id: int, data: CourseCreateSchema):
    course = Course.objects.get(id=course_id)
    for key, value in data.dict().items():
        setattr(course, key, value)
    course.save()
    cache.delete("courses_list")
    cache.delete("popular_courses")
    return course


@router.delete("/courses/{course_id}", auth=JWTAuth())
@require_role(["admin", "dosen"])
def delete_course(request, course_id: int):
    course = Course.objects.get(id=course_id)
    course.delete()
    cache.delete("courses_list")
    cache.delete("popular_courses")
    return {"success": True}
