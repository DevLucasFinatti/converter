import os
import io
import subprocess
from typing import Optional, Dict, Any
from django.core.files.uploadedfile import UploadedFile
import subprocess

class VideoService:
    """Serviço para processamento e validação de vídeos"""

    ALLOWED_EXTENSIONS = frozenset({
        '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm', '.mpeg', '.mpg', '.m4v'
    })

    @classmethod
    def get_file_extension(cls, filename: str) -> str:
        _, ext = os.path.splitext(filename)
        return ext.lower() 

    @classmethod
    def validate_video_file(cls, uploaded_file: UploadedFile) -> bool:
        ext = cls.get_file_extension(uploaded_file.name)
        
        if ext not in VideoService.ALLOWED_EXTENSIONS:
            return False
        return True

    @classmethod
    def get_video_metadata(cls, filepath: str) -> Optional[Dict[str, Any]]:
        """
        Extrai metadados básicos do vídeo usando ffprobe (parte do ffmpeg).
        filepath deve ser caminho do arquivo salvo em disco.
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height,duration,codec_name',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                filepath
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            lines = result.stdout.strip().split('\n')
            width = int(lines[0])
            height = int(lines[1])
            duration = float(lines[2])
            codec = lines[3]

            return {
                'width': width,
                'height': height,
                'duration': duration,
                'codec': codec
            }
        except Exception as e:
            print(f"Erro ao extrair metadados do vídeo: {e}")
            return None

    @classmethod
    def convert_video(
        cls,
        input_path: str,
        output_path: str,
        output_ext: str
    ) -> bool:
        """
        Converte vídeo para outro formato usando ffmpeg.

        Args:
            input_path (str): Caminho do arquivo de vídeo original.
            output_path (str): Caminho onde o arquivo convertido será salvo.
            output_ext (str): Extensão do formato desejado (ex: '.mp4').

        Returns:
            bool: True se a conversão for bem-sucedida, False caso contrário.
        """
        try:
            cmd = [
                'ffmpeg',
                '-i', input_path,
                '-c:v', 'libx264',           # Codec de vídeo
                '-c:a', 'aac',               # Codec de áudio
                '-strict', 'experimental',   # Para permitir uso de codecs experimentais
                '-y',                        # Sobrescreve sem perguntar
                output_path
            ]
            subprocess.run([
                r'C:\ffmpeg\bin\ffmpeg.exe',
                '-i', input_path,
                '-y', output_path
            ])

            return True
        except subprocess.CalledProcessError as e:
            print(f"[FFMPEG ERRO] Código {e.returncode}: {e.stderr.decode(errors='ignore')}")
            return False
        except Exception as e:
            print(f"Erro inesperado ao converter vídeo: {e}")
            return False
