from typing import TypeVar

from shared.responses.api_response_schema import ApiResponseSchema


T = TypeVar("T")

def success(
        data: T | None = None, 
        message: str = "Success"
) -> ApiResponseSchema[T]:
    
    return ApiResponseSchema[T](
        status="success",
        message=message,
        data=data
    )


def error(
        message: str, 
        data: dict[str, object] | None = None
) -> ApiResponseSchema[dict[str, object]]:
    
    return ApiResponseSchema[dict[str, object]](
        status="error",
        message=message,
        data=data
    )