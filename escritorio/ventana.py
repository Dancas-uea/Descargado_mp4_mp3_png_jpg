import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
from configuracion import Configuracion  # AGREGADO


class VentanaPrincipal:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.ventana = ctk.CTk()
        self.ventana.title("App Downloader")
        self.ventana.geometry("900x700")
        self.ventana.resizable(True, True)

        # Cargar configuración
        self.config = Configuracion()  # AGREGADO

        self.setup_ui()

    def setup_ui(self):
        self.frame_principal = ctk.CTkFrame(self.ventana)
        self.frame_principal.pack(padx=20, pady=20, fill="both", expand=True)

        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text="📥 APP DOWNLOADER",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.titulo.pack(pady=20)

        self.subtitulo = ctk.CTkLabel(
            self.frame_principal,
            text="Descarga videos, audio e imágenes de TikTok, YouTube, Instagram y X",
            font=ctk.CTkFont(size=12)
        )
        self.subtitulo.pack(pady=(0, 20))

        frame_url = ctk.CTkFrame(self.frame_principal)
        frame_url.pack(fill="x", padx=20, pady=10)

        self.lbl_url = ctk.CTkLabel(frame_url, text="🔗 URL:", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_url.pack(anchor="w", padx=10, pady=(10, 0))

        self.txt_url = ctk.CTkEntry(
            frame_url,
            placeholder_text="https://www.youtube.com/watch?v=...",
            height=40,
            font=ctk.CTkFont(size=12)
        )
        self.txt_url.pack(fill="x", padx=10, pady=5)

        frame_opciones = ctk.CTkFrame(self.frame_principal)
        frame_opciones.pack(fill="x", padx=20, pady=10)

        self.lbl_tipo = ctk.CTkLabel(frame_opciones, text="📁 Tipo de descarga:",
                                     font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_tipo.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.tipo_descarga = ctk.CTkComboBox(
            frame_opciones,
            values=["🎬 Video", "🎵 Audio", "🖼️ Imagen"],
            width=200,
            height=35
        )
        # Cargar último tipo guardado
        ultimo_tipo = self.config.get_ultimo_tipo()  # AGREGADO
        self.tipo_descarga.set(ultimo_tipo)  # AGREGADO
        self.tipo_descarga.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_carpeta = ctk.CTkLabel(frame_opciones, text="📂 Carpeta destino:",
                                        font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_carpeta.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        frame_carpeta = ctk.CTkFrame(frame_opciones)
        frame_carpeta.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        frame_carpeta.grid_columnconfigure(0, weight=1)

        self.txt_carpeta = ctk.CTkEntry(frame_carpeta, placeholder_text="Selecciona carpeta de destino", height=35)
        # Cargar última carpeta guardada
        carpeta_guardada = self.config.get_ultima_carpeta()  # AGREGADO
        self.txt_carpeta.insert(0, carpeta_guardada)  # AGREGADO
        self.txt_carpeta.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.btn_carpeta = ctk.CTkButton(frame_carpeta, text="📁", width=50, height=35, command=self.seleccionar_carpeta)
        self.btn_carpeta.grid(row=0, column=1)

        frame_opciones.grid_columnconfigure(1, weight=1)

        self.btn_descargar = ctk.CTkButton(
            self.frame_principal,
            text="🚀 INICIAR DESCARGA",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=self.iniciar_descarga
        )
        self.btn_descargar.pack(pady=20, padx=20, fill="x")

        frame_log = ctk.CTkFrame(self.frame_principal)
        frame_log.pack(padx=20, pady=10, fill="both", expand=True)

        self.lbl_log = ctk.CTkLabel(frame_log, text="📋 LOG DE DESCARGA:", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_log.pack(anchor="w", padx=10, pady=5)

        self.txt_log = ctk.CTkTextbox(frame_log, height=200, font=ctk.CTkFont(size=11))
        self.txt_log.pack(fill="both", expand=True, padx=10, pady=5)

        self.progress = ctk.CTkProgressBar(self.frame_principal)
        self.progress.pack(padx=20, pady=10, fill="x")
        self.progress.set(0)

        self.lbl_estado = ctk.CTkLabel(self.frame_principal, text="✅ Listo para descargar", font=ctk.CTkFont(size=11))
        self.lbl_estado.pack(pady=5)

    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.txt_carpeta.delete(0, "end")
            self.txt_carpeta.insert(0, carpeta)
            # Guardar la carpeta seleccionada
            self.config.set_ultima_carpeta(carpeta)  # AGREGADO

    def log(self, mensaje):
        self.txt_log.insert("end", f"{mensaje}\n")
        self.txt_log.see("end")
        self.ventana.update()

    def iniciar_descarga(self):
        url = self.txt_url.get().strip()
        if not url:
            messagebox.showwarning("Advertencia", "Por favor ingresa una URL")
            return

        carpeta = self.txt_carpeta.get().strip()
        if not carpeta:
            carpeta = "descargas"

        # Obtener tipo sin emojis
        tipo_raw = self.tipo_descarga.get()
        if "Video" in tipo_raw:
            tipo_final = "video"
        elif "Audio" in tipo_raw:
            tipo_final = "audio"
        else:
            tipo_final = "imagen"

        # Guardar el tipo seleccionado
        self.config.set_ultimo_tipo(tipo_raw)  # AGREGADO

        self.btn_descargar.configure(state="disabled", text="⏳ DESCARGANDO...")
        self.progress.set(0.5)
        self.lbl_estado.configure(text="⏳ Descargando...")

        # Pasar los 3 parámetros correctamente
        thread = threading.Thread(target=self.procesar_descarga, args=(url, carpeta, tipo_final))
        thread.daemon = True
        thread.start()

    def procesar_descarga(self, url, carpeta, tipo_final):
        try:
            from analizador_urls import AnalizadorURLs
            from descargador import Descargador

            self.log(f"🔍 Analizando URL: {url}")
            analizador = AnalizadorURLs()
            info = analizador.analizar(url)

            if not info:
                self.log("❌ URL no soportada")
                return

            self.log(f"📱 Plataforma: {info['plataforma'].upper()}")
            self.log(f"📂 Carpeta destino: {carpeta}")
            self.log(f"🎯 Tipo: {tipo_final}")

            self.log("⬇️ Iniciando descarga...")
            descargador = Descargador(carpeta)
            resultado = descargador.descargar(url, carpeta, tipo_final)

            if resultado and "Error" not in resultado:
                self.log(f"✅ ¡Descarga completada! - {resultado}")
                self.lbl_estado.configure(text="✅ Descarga completada")
                self.progress.set(1)
            else:
                self.log(f"❌ Error en descarga: {resultado}")
                self.lbl_estado.configure(text="❌ Error en descarga")

        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            self.lbl_estado.configure(text=f"❌ Error: {str(e)}")
        finally:
            self.btn_descargar.configure(state="normal", text="🚀 INICIAR DESCARGA")

    def ejecutar(self):
        self.ventana.mainloop()