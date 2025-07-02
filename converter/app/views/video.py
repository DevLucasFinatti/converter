import os
import tempfile
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request

from converter.app.models.responses import Response as ApiResponse
from converter.app.services.video import VideoService

@api_view(['POST'])
def video_convert(request: Request):
    if 'file' not in request.FILES:
        return ApiResponse.ErrorResponse(
            message="Nenhum arquivo enviado",
            status_code=400
        ).to_drf_response()

    uploaded_file = request.FILES['file']
    extension = request.data.get('extension', '').lower()
    if not extension.startswith('.'):
        extension = '.' + extension

    if not VideoService.validate_video_file(uploaded_file):
        print('aaaaaaaaa', uploaded_file)
        return ApiResponse.ErrorResponse(
            message="Vídeo inválido ou formato não suportado",
            status_code=400,
            error_details={
                "allowed_extensions": list(VideoService.ALLOWED_EXTENSIONS),
                "received_file": uploaded_file.name
            }
        ).to_drf_response()

    try:
        input_ext = VideoService.get_file_extension(uploaded_file.name)

        # Salva o vídeo temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix=input_ext) as temp_in:
            for chunk in uploaded_file.chunks():
                temp_in.write(chunk)
            temp_in_path = temp_in.name

        temp_out_path = temp_in_path.rsplit('.', 1)[0] + extension

        # Converte vídeo
        success = VideoService.convert_video(input_path=temp_in_path, output_path=temp_out_path, output_ext=extension)
        if not success:
            os.unlink(temp_in_path)
            return ApiResponse.ErrorResponse(
                message="Erro ao converter o vídeo",
                status_code=500
            ).to_drf_response()

        # Lê o vídeo convertido para memória
        with open(temp_out_path, 'rb') as f_out:
            video_content = f_out.read()

        # Remove arquivos temporários
        os.unlink(temp_in_path)
        os.unlink(temp_out_path)

        # Retorna o arquivo convertido para download
        content_type = f'video/{extension.lstrip(".")}'
        response = HttpResponse(video_content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="converted{extension}"'
        return response

    except Exception as e:
        return ApiResponse.ErrorResponse(
            message="Erro ao processar vídeo",
            status_code=500,
            error_details=str(e)
        ).to_drf_response()
