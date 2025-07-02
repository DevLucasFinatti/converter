import os
import io
from typing import Union, Optional, Dict, Any
from PIL import Image, UnidentifiedImageError
from django.core.files.uploadedfile import UploadedFile
from django.core.files.images import get_image_dimensions


class ImgService:
    ALLOWED_EXTENSIONS = frozenset({
        # Comuns
        '.jpg', '.jpeg', '.jpe', '.jif', '.jfif', '.jfi',
        '.png', '.gif', '.bmp', '.dib', '.webp', '.tiff', '.tif',

        # RAW
        '.arw', '.cr2', '.cr3', '.crw', '.dng', '.erf', '.kdc', '.mdc', '.mrw',
        '.nef', '.nrw', '.orf', '.pef', '.raf', '.raw', '.rw2', '.rwl', '.srf', '.srw', '.x3f',

        # Profissionais
        '.psd', '.psb', '.ai', '.eps', '.svg', '.svgz',

        # Científicos
        '.dcm', '.fits',

        # Outros
        '.ico', '.icns', '.exr', '.hdr', '.pbm', '.pgm', '.ppm', '.pnm',
        '.heif', '.heic', '.avif', '.jp2', '.j2k', '.jpf', '.jpx', '.jpm', '.mj2',

        # Legados
        '.pcx', '.tga', '.icb', '.vda', '.vst', '.cut', '.dds',
        '.xbm', '.xpm', '.wbmp', '.cd5', '.cht', '.fpx', '.pdd'
    })

    @classmethod
    def get_file_extension(cls, filename: str) -> str:
        _, ext = os.path.splitext(filename)
        return ext.lower()

    @classmethod
    def validate_image_file(cls, uploaded_file: UploadedFile) -> bool:
        try:
            ext = cls.get_file_extension(uploaded_file.name)
            if ext not in cls.ALLOWED_EXTENSIONS:
                return False

            uploaded_file.seek(0)
            width, height = get_image_dimensions(uploaded_file)
            uploaded_file.seek(0)

            return width is not None and height is not None
        except (TypeError, AttributeError, UnidentifiedImageError, Exception):
            return False

    @classmethod
    def get_image_metadata(cls, uploaded_file: UploadedFile) -> Optional[Dict[str, Any]]:
        try:
            uploaded_file.seek(0)
            with Image.open(uploaded_file) as img:
                # Limpa dados binários de 'info'
                info_clean = {
                    k: (v.decode('utf-8', errors='ignore') if isinstance(v, bytes) else v)
                    for k, v in img.info.items()
                }

                return {
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.width,
                    'height': img.height,
                    'info': info_clean
                }
        except Exception:
            return None
        
    @classmethod
    def convert_image(
        cls,
        input_ext: str,
        uploaded_file: UploadedFile,
        output_ext: str
    ) -> Optional[io.BytesIO]:
        try:
            uploaded_file.seek(0)
            with Image.open(uploaded_file) as img:
                # Remover alpha para formatos que não suportam (ex: JPEG)
                if output_ext.lower() in ['.jpg', '.jpeg'] and img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3]) 
                    img = background
                else:
                    # Converte para modo RGB para evitar erros na hora de salvar
                    if img.mode not in ('RGB', 'L'):
                        img = img.convert('RGB')

                output_buffer = io.BytesIO()
                
                img.save(output_buffer, format=output_ext.lstrip('.').upper())
                output_buffer.seek(0)
                return output_buffer

        except Exception as e:
            print(f"Erro na conversão de imagem: {e}")
            return None
