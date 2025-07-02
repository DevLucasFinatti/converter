from dataclasses import dataclass, asdict
from typing import Any, Optional, Dict
from rest_framework.response import Response as DRFResponse


class Response:
    class BaseResponse:
        def to_dict(self) -> Dict[str, Any]:
            return asdict(self)

        def to_drf_response(self) -> DRFResponse:
            return DRFResponse(self.to_dict(), status=self.status_code)

    @dataclass
    class SuccessResponse(BaseResponse):
        data: Any
        message: str = "Operação realizada com sucesso"
        status_code: int = 200
        success: bool = True

    @dataclass
    class ErrorResponse(BaseResponse):
        message: str
        status_code: int = 400
        error_details: Optional[Any] = None
        success: bool = False

    @dataclass
    class NotFoundResponse(ErrorResponse):
        message: str = "Recurso não encontrado"
        status_code: int = 404

    @dataclass
    class ValidationErrorResponse(ErrorResponse):
        message: str = "Erro de validação"
        errors: Optional[Dict[str, Any]] = None
        status_code: int = 422
