from ninja.responses import Response
import functools


def require_role(roles):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            user_role = request.auth.get("role") if request.auth else None
            if user_role in roles:
                return func(request, *args, **kwargs)
            return Response(
                {"error": "Tidak diizinkan: Peran tidak sesuai"}, status=403
            )

        return wrapper

    return decorator
