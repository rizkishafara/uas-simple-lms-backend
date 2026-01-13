from ninja import Schema


class RegisterSchema(Schema):
    username: str
    email: str | None = None
    password: str
    role: str | None = "mahasiswa"


class LoginSchema(Schema):
    username: str
    password: str


class CourseSchema(Schema):
    id: int
    title: str
    description: str


class CourseCreateSchema(Schema):
    title: str
    description: str
