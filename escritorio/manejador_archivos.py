import os
import shutil
from pathlib import Path


class ManejadorArchivos:
    def __init__(self):
        pass

    def crear_carpeta(self, ruta):
        try:
            if not os.path.exists(ruta):
                os.makedirs(ruta)
                return True
            return True
        except Exception as e:
            print(f"Error al crear carpeta: {e}")
            return False

    def obtener_tamaño(self, ruta):
        try:
            if os.path.isfile(ruta):
                return os.path.getsize(ruta)
            elif os.path.isdir(ruta):
                total = 0
                for root, dirs, files in os.walk(ruta):
                    for file in files:
                        total += os.path.getsize(os.path.join(root, file))
                return total
            return 0
        except:
            return 0

    def formatear_tamaño(self, bytes):
        for unidad in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unidad}"
            bytes /= 1024
        return f"{bytes:.2f} TB"

    def listar_descargas(self, carpeta):
        try:
            archivos = []
            if os.path.exists(carpeta):
                for archivo in os.listdir(carpeta):
                    ruta = os.path.join(carpeta, archivo)
                    if os.path.isfile(ruta):
                        archivos.append({
                            'nombre': archivo,
                            'tamaño': self.formatear_tamaño(self.obtener_tamaño(ruta)),
                            'ruta': ruta
                        })
            return archivos
        except Exception as e:
            print(f"Error al listar: {e}")
            return []

    def eliminar_archivo(self, ruta):
        try:
            if os.path.isfile(ruta):
                os.remove(ruta)
                return True
            return False
        except:
            return False