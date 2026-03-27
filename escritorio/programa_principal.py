import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os

from descargador import Descargador
from analizador_urls import AnalizadorURLs
from configuracion import Configuracion


class AppDescargas:
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title("App Downloader")
        self.ventana.geometry("800x600")

        self.descargador = Descargador()
        self.analizador = AnalizadorURLs()
        self.config = Configuracion()

        self.setup_ui()

    def setup_ui(self):
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.ventana)
        self.frame_principal.pack(padx=20, pady=20, fill="both", expand=True)

        # Título
        titulo = ctk.CTkLabel(
            self.frame_principal,
            text="App Downloader",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=10)

        # Campo URL
        lbl_url = ctk.CTkLabel(self.frame_principal, text="URL:")
        lbl_url.pack(anchor="w", padx=10)

        self.txt_url = ctk.CTkEntry(self.frame_principal, placeholder_text="Pega la URL aquí...")
        self.txt_url.pack(fill="x", padx=10, pady=5)

        # Tipo de descarga
        lbl_tipo = ctk.CTkLabel(self.frame_principal, text="Tipo:")
        lbl_tipo.pack(anchor="w", padx=10, pady=(10, 0))

        self.tipo_descarga = ctk.CTkComboBox(
            self.frame_principal,
            values=["Video", "Audio", "Imagen"]
        )
        # Cargar último tipo guardado
        ultimo_tipo = self.config.get_ultimo_tipo()
        self.tipo_descarga.set(ultimo_tipo)
        self.tipo_descarga.pack(fill="x", padx=10, pady=5)

        # Carpeta destino
        lbl_carpeta = ctk.CTkLabel(self.frame_principal, text="Carpeta destino:")
        lbl_carpeta.pack(anchor="w", padx=10, pady=(10, 0))

        frame_carpeta = ctk.CTkFrame(self.frame_principal)
        frame_carpeta.pack(fill="x", padx=10, pady=5)

        self.txt_carpeta = ctk.CTkEntry(frame_carpeta, placeholder_text="Selecciona carpeta...")
        # Cargar última carpeta guardada
        carpeta_guardada = self.config.get_ultima_carpeta()
        self.txt_carpeta.insert(0, carpeta_guardada)
        self.txt_carpeta.pack(side="left", fill="x", expand=True, padx=(0, 5))

        btn_carpeta = ctk.CTkButton(frame_carpeta, text="Examinar", width=80, command=self.seleccionar_carpeta)
        btn_carpeta.pack(side="right")

        # Botón descargar
        self.btn_descargar = ctk.CTkButton(
            self.frame_principal,
            text="Descargar",
            height=40,
            font=("Arial", 14, "bold"),
            command=self.descargar
        )
        self.btn_descargar.pack(pady=20)

        # Área de log
        lbl_log = ctk.CTkLabel(self.frame_principal, text="Log:")
        lbl_log.pack(anchor="w", padx=10)

        self.txt_log = ctk.CTkTextbox(self.frame_principal, height=200)
        self.txt_log.pack(fill="both", expand=True, padx=10, pady=5)

    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.txt_carpeta.delete(0, "end")
            self.txt_carpeta.insert(0, carpeta)
            # Guardar la carpeta seleccionada
            self.config.set_ultima_carpeta(carpeta)

    def log(self, mensaje):
        self.txt_log.insert("end", f"{mensaje}\n")
        self.txt_log.see("end")
        self.ventana.update()

    def descargar(self):
        url = self.txt_url.get().strip()
        if not url:
            messagebox.showwarning("Advertencia", "Ingresa una URL")
            return

        carpeta = self.txt_carpeta.get().strip()
        if not carpeta:
            carpeta = "descargas"

        tipo = self.tipo_descarga.get().lower()

        # Guardar el tipo seleccionado
        self.config.set_ultimo_tipo(self.tipo_descarga.get())

        self.btn_descargar.configure(state="disabled", text="Descargando...")

        thread = threading.Thread(target=self.procesar_descarga, args=(url, carpeta, tipo))
        thread.daemon = True
        thread.start()

    def procesar_descarga(self, url, carpeta, tipo):
        try:
            self.log(f"Analizando URL: {url}")
            info = self.analizador.analizar(url)

            if not info:
                self.log("Error: URL no soportada")
                return

            self.log(f"Plataforma: {info['plataforma']}")
            self.log(f"Tipo detectado: {info['tipo_detectado']}")

            self.log("Iniciando descarga...")
            resultado = self.descargador.descargar(url, carpeta, tipo)

            if resultado and "Error" not in resultado:
                self.log(f"✅ Descarga completada: {resultado}")
            else:
                self.log(f"❌ Error en la descarga: {resultado}")

        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
        finally:
            self.btn_descargar.configure(state="normal", text="Descargar")

    def ejecutar(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    app = AppDescargas()
    app.ejecutar()