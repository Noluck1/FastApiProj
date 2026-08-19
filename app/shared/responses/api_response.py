from typing import TypeVar

from app.shared.responses.api_response_schema import ApiResponseSchema


T = TypeVar("T")

def success(data: T | None = None, message: str = "Success") -> ApiResponseSchema[T]:
    return ApiResponseSchema[T](
        status="success",
        message=message,
        data=data
    )


def error(message: str, data: dict | None = None) -> ApiResponseSchema[dict]:
    return ApiResponseSchema[dict](
        status="error",
        message=message,
        data=data
    )