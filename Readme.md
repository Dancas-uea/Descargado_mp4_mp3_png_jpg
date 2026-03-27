markdown
# 🎬 App Downloader

Una aplicación de escritorio moderna para descargar videos, música e imágenes de las plataformas más populares como YouTube, TikTok, Instagram y X (Twitter).

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)

## ✨ Características

- 📥 **Descarga videos** en calidad HD (hasta 4K)
- 🎵 **Extrae audio** a formato MP3 (192kbps)
- 🖼️ **Guarda imágenes** de publicaciones
- 🎨 **Interfaz moderna** con CustomTkinter
- 💾 **Guarda configuración** (recuerda última carpeta y tipo)
- 🚀 **Descarga rápida** con hilos de ejecución
- 📋 **Log en tiempo real** de la descarga c

## 📱 Plataformas Soportadas

| Plataforma | Videos | Audio | Imágenes |
|------------|--------|-------|----------|
| YouTube    | ✅     | ✅    | ❌       |
| TikTok     | ✅     | ✅    | ❌       |
| Instagram  | ✅     | ✅    | ✅       |
| X (Twitter)| ✅     | ✅    | ✅       |

## 🚀 Instalación

### Requisitos previos
- Python 3.8 o superior
- pip (gestor de paquetes)
- ffmpeg (opcional, para mejor calidad)

### Instalación de dependencias

```bash
pip install -r escritorio/escritorio.txt
Instalación de ffmpeg (opcional)
Windows:

bash
# Usando winget
winget install Gyan.FFmpeg

# O manual: descargar de https://ffmpeg.org/
Linux:

bash
sudo apt install ffmpeg
💻 Uso
Ejecutar la aplicación:

bash
cd escritorio
python programa_principal.py
Pegar la URL del contenido que deseas descargar

Seleccionar el tipo (Video, Audio o Imagen)

Elegir carpeta de destino (se guarda automáticamente)

Hacer clic en "Descargar" y esperar

📦 Compilar a EXE
Para crear un ejecutable independiente:

bash
cd escritorio
pip install pyinstaller
pyinstaller --onefile --windowed --name "AppDownloader" programa_principal.py
El ejecutable estará en la carpeta dist/

🗂️ Estructura del Proyecto
text
App_Downloader/
├── escritorio/
│   ├── programa_principal.py   # Punto de entrada
│   ├── ventana.py              # Interfaz gráfica
│   ├── descargador.py          # Lógica de descarga
│   ├── analizador_urls.py      # Análisis de URLs
│   ├── configuracion.py        # Gestión de configuración
│   └── escritorio.txt          # Dependencias
├── descargas/                  # Carpeta por defecto
└── README.md
🔧 Configuración
La aplicación crea automáticamente un archivo de configuración en:

text
C:\Users\[Usuario]\.app_downloader\config.json
Contenido:

json
{
    "ultima_carpeta": "C:\\Users\\Usuario\\Downloads",
    "ultimo_tipo": "Video"
}
🤝 Contribuciones
Las contribuciones son bienvenidas. Por favor:

Fork el proyecto

Crea tu rama (git checkout -b feature/nueva-funcionalidad)

Commit tus cambios (git commit -m 'Agregar nueva funcionalidad')

Push a la rama (git push origin feature/nueva-funcionalidad)

Abre un Pull Request

📝 Licencia
Este proyecto está bajo la licencia MIT. Ver el archivo LICENSE para más detalles.

⚠️ Notas
Respetar los derechos de autor y términos de servicio de cada plataforma

Algunas plataformas pueden tener restricciones de descarga

Este software es solo para uso personal y educativo

📧 Contacto
GitHub: @Dancas-uea

Proyecto: Descargado_mp4_mp3_png_jpg