import json
import os
from pathlib import Path


class Configuracion:
    def __init__(self):
        # Guardar configuración en la carpeta del usuario, no en la del programa
        self.carpeta_app = Path.home() / ".app_downloader"
        self.archivo_config = self.carpeta_app / "config.json"

        # Crear carpeta si no existe
        if not self.carpeta_app.exists():
            self.carpeta_app.mkdir()

        self.config = self.cargar()

    def cargar(self):
        if self.archivo_config.exists():
            try:
                with open(self.archivo_config, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.config_default()
        else:
            return self.config_default()

    def config_default(self):
        return {
            "ultima_carpeta": str(Path.home() / "Downloads"),
            "ultimo_tipo": "🎬 Video"
        }

    def guardar(self):
        with open(self.archivo_config, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def get_ultima_carpeta(self):
        return self.config.get("ultima_carpeta", str(Path.home() / "Downloads"))

    def set_ultima_carpeta(self, carpeta):
        self.config["ultima_carpeta"] = carpeta
        self.guardar()

    def get_ultimo_tipo(self):
        return self.config.get("ultimo_tipo", "🎬 Video")

    def set_ultimo_tipo(self, tipo):
        self.config["ultimo_tipo"] = tipo
        self.guardar()