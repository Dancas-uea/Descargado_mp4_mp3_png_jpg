import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import tkinter as tk

from actualizador import Actualizador
from descargador import Descargador
from analizador_urls import AnalizadorURLs
from configuracion import Configuracion

# Configurar tema de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AppDescargas:
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title("App Downloader")
        self.ventana.geometry("900x700")
        self.ventana.minsize(800, 600)

        # Eliminar barra de menú tradicional
        self.ventana.option_add('*tearOff', False)

        # Icono de la ventana (si tienes)
        try:
            self.ventana.iconbitmap("recursos/icon.ico")
        except:
            pass

        self.descargador = Descargador()
        self.analizador = AnalizadorURLs()
        self.config = Configuracion()

        # Versión actual del programa
        self.version_actual = "1.0.1"
        self.actualizador = Actualizador(self.version_actual)

        self.setup_ui()

    def setup_ui(self):
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.ventana, corner_radius=15)
        self.frame_principal.pack(padx=25, pady=25, fill="both", expand=True)

        # Header con gradiente visual
        header_frame = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        header_frame.pack(fill="x", pady=(10, 20))

        # Título principal
        titulo = ctk.CTkLabel(
            header_frame,
            text="🎬 APP DOWNLOADER",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#2ecc71"
        )
        titulo.pack()

        # Subtítulo
        subtitulo = ctk.CTkLabel(
            header_frame,
            text="Descarga contenido de las plataformas más populares",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        subtitulo.pack(pady=(5, 0))

        # Barra de opciones (reemplaza el menú)
        options_bar = ctk.CTkFrame(self.frame_principal, height=40, fg_color="#2b2b2b", corner_radius=8)
        options_bar.pack(fill="x", pady=(10, 15))
        options_bar.pack_propagate(False)

        # Botones de opciones
        btn_actualizar = ctk.CTkButton(
            options_bar,
            text="🔄 Verificar actualizaciones",
            width=180,
            height=32,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            hover_color="#3a3a3a",
            command=self.verificar_actualizacion
        )
        btn_actualizar.pack(side="left", padx=10, pady=4)

        btn_acerca = ctk.CTkButton(
            options_bar,
            text="ℹ️ Acerca de",
            width=120,
            height=32,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            hover_color="#3a3a3a",
            command=self.acerca_de
        )
        btn_acerca.pack(side="left", padx=5, pady=4)

        btn_salir = ctk.CTkButton(
            options_bar,
            text="🚪 Salir",
            width=100,
            height=32,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            hover_color="#aa3333",
            command=self.ventana.quit
        )
        btn_salir.pack(side="right", padx=10, pady=4)

        # Separador
        separador = ctk.CTkFrame(self.frame_principal, height=2, fg_color="#2ecc71")
        separador.pack(fill="x", pady=10)

        # --- Sección URL ---
        url_frame = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        url_frame.pack(fill="x", pady=10)

        lbl_url = ctk.CTkLabel(
            url_frame,
            text="🔗 URL DEL CONTENIDO",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2ecc71"
        )
        lbl_url.pack(anchor="w", padx=5)

        self.txt_url = ctk.CTkEntry(
            url_frame,
            placeholder_text="https://www.youtube.com/watch?v=...",
            height=45,
            font=ctk.CTkFont(size=13),
            corner_radius=10,
            border_width=1,
            border_color="#3a3a3a"
        )
        self.txt_url.pack(fill="x", padx=5, pady=(5, 0))

        # --- Grid de opciones ---
        options_frame = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        options_frame.pack(fill="x", pady=15)

        # Fila 1: Tipo de descarga
        tipo_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        tipo_frame.pack(fill="x", pady=5)

        lbl_tipo = ctk.CTkLabel(
            tipo_frame,
            text="📀 TIPO",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2ecc71",
            width=120
        )
        lbl_tipo.pack(side="left", padx=5)

        self.tipo_descarga = ctk.CTkComboBox(
            tipo_frame,
            values=["🎬 Video", "🎵 Audio", "🖼️ Imagen"],
            width=200,
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=12)
        )
        # Cargar último tipo guardado
        ultimo_tipo = self.config.get_ultimo_tipo()
        self.tipo_descarga.set(ultimo_tipo)
        self.tipo_descarga.pack(side="left", padx=10)

        # Fila 2: Carpeta destino
        carpeta_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        carpeta_frame.pack(fill="x", pady=10)

        lbl_carpeta = ctk.CTkLabel(
            carpeta_frame,
            text="📁 DESTINO",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#2ecc71",
            width=120
        )
        lbl_carpeta.pack(side="left", padx=5)

        frame_carpeta = ctk.CTkFrame(carpeta_frame, fg_color="transparent")
        frame_carpeta.pack(side="left", fill="x", expand=True, padx=10)

        self.txt_carpeta = ctk.CTkEntry(
            frame_carpeta,
            placeholder_text="Selecciona carpeta de destino",
            height=40,
            font=ctk.CTkFont(size=12),
            corner_radius=8,
            border_width=1,
            border_color="#3a3a3a"
        )
        carpeta_guardada = self.config.get_ultima_carpeta()
        self.txt_carpeta.insert(0, carpeta_guardada)
        self.txt_carpeta.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_carpeta = ctk.CTkButton(
            frame_carpeta,
            text="📂",
            width=50,
            height=40,
            corner_radius=8,
            command=self.seleccionar_carpeta,
            fg_color="#3a3a3a",
            hover_color="#4a4a4a"
        )
        btn_carpeta.pack(side="right")

        # --- Botón Descargar ---
        self.btn_descargar = ctk.CTkButton(
            self.frame_principal,
            text="⬇️ DESCARGAR",
            height=55,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60",
            corner_radius=12,
            command=self.descargar
        )
        self.btn_descargar.pack(pady=25, padx=20, fill="x")

        # --- Sección Log ---
        log_frame = ctk.CTkFrame(self.frame_principal, corner_radius=10)
        log_frame.pack(fill="both", expand=True, pady=(10, 0))

        log_header = ctk.CTkFrame(log_frame, fg_color="transparent", height=30)
        log_header.pack(fill="x", padx=10, pady=5)

        lbl_log = ctk.CTkLabel(
            log_header,
            text="📋 CONSOLA",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#2ecc71"
        )
        lbl_log.pack(side="left")

        self.txt_log = ctk.CTkTextbox(
            log_frame,
            height=180,
            font=ctk.CTkFont(size=11),
            corner_radius=8,
            border_width=0
        )
        self.txt_log.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Barra de estado inferior
        status_frame = ctk.CTkFrame(self.frame_principal, height=30, fg_color="#1a1a1a", corner_radius=8)
        status_frame.pack(fill="x", pady=(10, 0))

        self.lbl_estado = ctk.CTkLabel(
            status_frame,
            text="✅ Listo para descargar",
            font=ctk.CTkFont(size=11),
            text_color="#888888"
        )
        self.lbl_estado.pack(side="left", padx=15, pady=5)

        version_label = ctk.CTkLabel(
            status_frame,
            text=f"v{self.version_actual}",
            font=ctk.CTkFont(size=10),
            text_color="#555555"
        )
        version_label.pack(side="right", padx=15, pady=5)

    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.txt_carpeta.delete(0, "end")
            self.txt_carpeta.insert(0, carpeta)
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

        tipo_raw = self.tipo_descarga.get()
        if "Video" in tipo_raw:
            tipo = "video"
        elif "Audio" in tipo_raw:
            tipo = "audio"
        else:
            tipo = "imagen"

        self.config.set_ultimo_tipo(tipo_raw)

        self.btn_descargar.configure(state="disabled", text="⏳ DESCARGANDO...")
        self.lbl_estado.configure(text="⏳ Descargando...")

        thread = threading.Thread(target=self.procesar_descarga, args=(url, carpeta, tipo))
        thread.daemon = True
        thread.start()

    def procesar_descarga(self, url, carpeta, tipo):
        try:
            self.log(f"🔍 Analizando URL: {url}")
            info = self.analizador.analizar(url)

            if not info:
                self.log("❌ Error: URL no soportada")
                self.lbl_estado.configure(text="❌ URL no soportada")
                return

            self.log(f"📱 Plataforma: {info['plataforma'].upper()}")
            self.log(f"🎯 Tipo seleccionado: {tipo}")

            self.log("⬇️ Iniciando descarga...")
            resultado = self.descargador.descargar(url, carpeta, tipo)

            if resultado and "Error" not in resultado:
                self.log(f"✅ Descarga completada: {resultado}")
                self.lbl_estado.configure(text="✅ Descarga completada")
            else:
                self.log(f"❌ Error en descarga: {resultado}")
                self.lbl_estado.configure(text="❌ Error en descarga")

        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            self.lbl_estado.configure(text=f"❌ {str(e)[:50]}")
        finally:
            self.btn_descargar.configure(state="normal", text="⬇️ DESCARGAR")

    def verificar_actualizacion(self):
        """Verifica si hay una nueva versión disponible"""
        self.log("🔍 Verificando actualizaciones...")
        info = self.actualizador.verificar_actualizacion(mostrar_mensaje=False)

        if info.get("hay_actualizacion"):
            self.log(f"📢 Nueva versión {info['version']} disponible!")
            self.actualizador.mostrar_dialogo_actualizacion(info)
        elif info.get("error"):
            self.log(f"❌ Error al verificar: {info['error']}")
            messagebox.showerror("Error", f"No se pudo verificar actualizaciones:\n{info['error']}")
        else:
            self.log(f"✅ Ya tienes la última versión ({self.version_actual})")
            messagebox.showinfo("Actualizaciones", f"Ya tienes la última versión ({self.version_actual})")

    def acerca_de(self):
        """Muestra información sobre el programa"""
        messagebox.showinfo(
            "Acerca de App Downloader",
            f"🎬 App Downloader\nVersión: {self.version_actual}\n\n"
            "Descarga videos, audio e imágenes de:\n"
            "• YouTube\n• TikTok\n• Instagram\n• X (Twitter)\n\n"
            "Desarrollado por: Dancas-uea\n"
            "GitHub: https://github.com/Dancas-uea/Descargado_mp4_mp3_png_jpg"
        )

    def ejecutar(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    app = AppDescargas()
    app.ejecutar()