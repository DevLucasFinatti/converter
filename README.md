
# 🎥🖼️ File Converter - Video and Image

This project provides a simple API to **convert image and video files** to different formats using `multipart/form-data`.

---

## 🚀 Technologies Used

- **Django**
- **Django REST Framework**
- **Pillow** (for image processing)
- **FFmpeg** (for video conversion)

---

## 🌐 Base API URL

```
http://127.0.0.1:8000/api/
```

---

## 📸 Route: `/convert-img/`

Converts **images** from one format to another (e.g., `.png → .jpg`, `.webp → .png`, etc).

### 🔧 Method:
```
POST
```

### 🧾 Content-Type:
```
multipart/form-data
```

### 🧵 Expected Fields:

| Key         | Type     | Description                                 |
|-------------|----------|---------------------------------------------|
| `file`      | File     | The image to be converted                   |
| `extension` | Text     | Target extension (e.g., `.jpg`, `.png`)     |

### 🧪 Postman Example:

- **Key**: `file` → select an image
- **Key**: `extension` → `.png`

---

## 🎞️ Route: `/convert-video/`

Converts **videos** from one format to another (e.g., `.avi → .mp4`, `.mov → .webm`, etc).

### 🔧 Method:
```
POST
```

### 🧾 Content-Type:
```
multipart/form-data
```

### 🧵 Expected Fields:

| Key         | Type     | Description                                 |
|-------------|----------|---------------------------------------------|
| `file`      | File     | The video to be converted                   |
| `extension` | Text     | Target extension (e.g., `.mp4`, `.webm`)     |

### 🧪 Postman Example:

- **Key**: `file` → select a video
- **Key**: `extension` → `.mp4`

---

## 📥 File Download

The API will respond with:
- A **binary file** (`Content-Disposition: attachment`)  
**or**
- A `download_url` field to download the processed file. (TODO)

---

## 🧰 Requirements to Run Locally

- Python 3.11+
- FFmpeg installed and available in the system `PATH`
- Pillow (`pip install pillow`)
- Django + Django REST Framework

*Run:* `pip install -r requirements.txt`

---

## 👨‍💻 Author

Lucas Finatti  
😎💼 Software Engineer
