import yt_dlp
import os


class Descargador:
    def __init__(self, carpeta_destino="descargas"):
        self.carpeta_destino = carpeta_destino

    def descargar(self, url, carpeta, tipo):
        try:
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)

            ffmpeg_path = r'C:\ffmpeg\ffmpeg-8.1-essentials_build\bin\ffmpeg.exe'

            if tipo == "video":
                ydl_opts = {
                    'outtmpl': f'{carpeta}/%(title)s.%(ext)s',
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'merge_output_format': 'mp4',
                    'ffmpeg_location': ffmpeg_path,
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }]
                }
            elif tipo == "audio":
                ydl_opts = {
                    'outtmpl': f'{carpeta}/%(title)s.%(ext)s',
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'ffmpeg_location': ffmpeg_path
                }
            else:
                ydl_opts = {
                    'outtmpl': f'{carpeta}/%(title)s.%(ext)s',
                    'format': 'best',
                    'ffmpeg_location': ffmpeg_path
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                titulo = info.get('title', 'archivo')
                return f"{carpeta}/{titulo}"

        except Exception as e:
            return f"Error: {str(e)}"