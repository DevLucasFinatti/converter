from rest_framework.decorators import api_view
from rest_framework.request import Request

from converter.app.models.responses import Response as ApiResponse
from converter.app.services.image import ImgService
from django.http import HttpResponse

@api_view(['POST'])
def img_convert(request: Request):
    if 'file' not in request.FILES:
        return ApiResponse.ErrorResponse(
            message="Nenhum arquivo enviado",
            status_code=400
        ).to_drf_response()

    uploaded_file = request.FILES['file']
    extension = request.data.get('extension', '').lower()

    if not extension.startswith('.'):
        extension = '.' + extension

    if not ImgService.validate_image_file(uploaded_file):
        return ApiResponse.ErrorResponse(
            message="Imagem inválida ou formato não suportado",
            status_code=400,
            error_details={
                "allowed_extensions": list(ImgService.ALLOWED_EXTENSIONS),
                "received_file": uploaded_file.name
            }
        ).to_drf_response()

    try:
        file_extension = ImgService.get_file_extension(uploaded_file.name)

        converted_buffer = ImgService.convert_image(
            input_ext=file_extension,
            uploaded_file=uploaded_file,
            output_ext=extension
        )

        if converted_buffer is None:
            return ApiResponse.ErrorResponse(
                message="Erro ao converter a imagem",
                status_code=500
            ).to_drf_response()

        content_type = f"image/{extension.lstrip('.')}"
        response = HttpResponse(converted_buffer.getvalue(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="converted{extension}"'
        return response

    except Exception as e:
        return ApiResponse.ErrorResponse(
            message="Erro ao processar imagem",
            status_code=500,
            error_details=str(e)
        ).to_drf_response()