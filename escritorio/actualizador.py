import requests
import json
import os
import sys
import subprocess
import webbrowser
from tkinter import messagebox
import tkinter as tk
from datetime import datetime


class Actualizador:
    def __init__(self, version_actual="1.0.0"):
        self.version_actual = version_actual
        self.repo_owner = "Dancas-uea"
        self.repo_name = "Descargado_mp4_mp3_png_jpg"
        self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"

    def verificar_actualizacion(self, mostrar_mensaje=True):
        """Verifica si hay una nueva versión disponible"""
        try:
            response = requests.get(self.api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                version_latest = data.get("tag_name", "").replace("v", "")
                descarga_url = data.get("html_url", "")
                notas = data.get("body", "Sin notas de actualización")

                if version_latest > self.version_actual:
                    return {
                        "hay_actualizacion": True,
                        "version": version_latest,
                        "url": descarga_url,
                        "notas": notas
                    }
                else:
                    if mostrar_mensaje:
                        messagebox.showinfo("Actualizaciones", "Ya tienes la última versión")
                    return {"hay_actualizacion": False}
            else:
                return {"hay_actualizacion": False, "error": f"Error {response.status_code}"}
        except Exception as e:
            return {"hay_actualizacion": False, "error": str(e)}

    def mostrar_dialogo_actualizacion(self, info):
        """Muestra ventana para actualizar"""
        ventana = tk.Toplevel()
        ventana.title("Actualización disponible")
        ventana.geometry("500x400")
        ventana.configure(bg="#1e1e2e")
        ventana.transient()
        ventana.grab_set()

        tk.Label(ventana, text="📥 Nueva versión disponible",
                 font=("Arial", 16, "bold"), bg="#1e1e2e", fg="#00ff88").pack(pady=10)

        tk.Label(ventana, text=f"Versión actual: {self.version_actual} → {info['version']}",
                 font=("Arial", 12), bg="#f0f0f0").pack(pady=5)

        tk.Label(ventana, text="Notas de la versión:",
                 font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=(10, 0))

        notas_texto = tk.Text(ventana, height=12, width=60, wrap="word")
        notas_texto.pack(pady=5, padx=10, fill="both", expand=True)
        notas_texto.insert("1.0", info['notas'])
        notas_texto.configure(state="disabled")

        def descargar():
            webbrowser.open(info['url'])
            ventana.destroy()
            messagebox.showinfo("Descarga",
                                "Se abrió el navegador para descargar la nueva versión.\nReemplaza el archivo manualmente.")

        def mas_tarde():
            ventana.destroy()

        def ignorar():
            ventana.destroy()
            messagebox.showinfo("Ignorar", "Puedes verificar actualizaciones manualmente desde el menú")

        frame_btns = tk.Frame(ventana, bg="#f0f0f0")
        frame_btns.pack(pady=15)

        tk.Button(frame_btns, text="Descargar ahora", command=descargar,
                  bg="#2ecc71", fg="white", padx=20, pady=5).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Más tarde", command=mas_tarde,
                  bg="#95a5a6", fg="white", padx=20, pady=5).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Ignorar esta versión", command=ignorar,
                  bg="#e74c3c", fg="white", padx=20, pady=5).pack(side="left", padx=5)

        ventana.wait_window()