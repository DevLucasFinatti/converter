# 🎥🖼️ Conversor de Arquivos - Vídeo e Imagem

Este projeto fornece uma API simples para **converter arquivos de imagem e vídeo** para diferentes formatos, utilizando `multipart/form-data`.

---

## 🚀 Tecnologias utilizadas

- **Django**
- **Django REST Framework**
- **Pillow** (para manipulação de imagens)
- **FFmpeg** (para conversão de vídeos)

---

## 🌐 URL Base da API

```
http://127.0.0.1:8000/api/
```

---

## 📸 Rota: `/convert-img/`

Converte **imagens** de um formato para outro (ex: `.png → .jpg`, `.webp → .png`, etc).

### 🔧 Método:
```
POST
```

### 🧾 Content-Type:
```
multipart/form-data
```

### 🧵 Campos esperados:

| Chave       | Tipo     | Descrição                                      |
|-------------|----------|-----------------------------------------------|
| `file`      | Arquivo  | A imagem que será convertida                  |
| `extension` | Texto    | Extensão de destino (ex: `.jpg`, `.png`)      |

### 🧪 Exemplo no Postman:

- **Key**: `file` → selecione uma imagem
- **Key**: `extension` → `.png`

---

## 🎞️ Rota: `/convert-video/`

Converte **vídeos** de um formato para outro (ex: `.avi → .mp4`, `.mov → .webm`, etc).

### 🔧 Método:
```
POST
```

### 🧾 Content-Type:
```
multipart/form-data
```

### 🧵 Campos esperados:

| Chave       | Tipo     | Descrição                                      |
|-------------|----------|-----------------------------------------------|
| `file`      | Arquivo  | O vídeo que será convertido                   |
| `extension` | Texto    | Extensão de destino (ex: `.mp4`, `.webm`)     |

### 🧪 Exemplo no Postman:

- **Key**: `file` → selecione um vídeo
- **Key**: `extension` → `.mp4`

---

## 📥 Download do arquivo

A API vai responder com:
- Um **arquivo binário** (`Content-Disposition: attachment`)  
**ou**
- Um campo `download_url` para baixar o arquivo processado. (TODO)

---

## 🧰 Requisitos para rodar localmente

- Python 3.11+
- FFmpeg instalado e disponível no `PATH`
- Pillow (`pip install pillow`)
- Django + Django REST Framework

*Run:* pip install -r requirements.txt

---

## 👨‍💻 Autor

Lucas Finatti  
😎💼 Engenheiro de Software 
