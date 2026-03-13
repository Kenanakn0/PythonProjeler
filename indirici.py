
import customtkinter as ctk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import yt_dlp
import os
import threading
from pathlib import Path


ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("blue")

class ModernDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Modern MP3/MP4 İndirici")
        self.root.geometry("750x650")
        self.root.resizable(False, False)
        
        
        self.text_main = "#2d3436" 
        self.text_sub = "#636e72"   
        self.accent = "#00b894"    
        
       
        self.download_folder = str(Path.home() / "Downloads")
        
        self.create_gui()
    
    def create_gui(self):
        """Ferah ve Profesyonel Arayüz Oluştur"""
        
        
        self.title_label = ctk.CTkLabel(
            self.root, 
            text="Video/Müzik İndirici", 
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color=self.accent
        )
        self.title_label.pack(pady=(30, 5))
        
        self.subtitle_label = ctk.CTkLabel(
            self.root, 
            text="YouTube, SoundCloud ve 1000+ siteden en yüksek kalitede indirin", 
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=self.text_sub
        )
        self.subtitle_label.pack(pady=(0, 20))

        
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15, fg_color="#ffffff") 
        self.main_frame.pack(fill="both", expand=True, padx=40, pady=(0, 30))

    
        self.url_label = ctk.CTkLabel(self.main_frame, text="Video veya Müzik Linki:", font=ctk.CTkFont(weight="bold"), text_color=self.text_main)
        self.url_label.pack(anchor="w", padx=30, pady=(20, 5))

        self.url_entry = ctk.CTkEntry(
            self.main_frame, 
            placeholder_text="https://www.youtube.com/watch?v=...", 
            height=45,
            corner_radius=8,
            border_width=1,
            fg_color="#f5f6fa", 
            text_color=self.text_main
        )
        self.url_entry.pack(fill="x", padx=30)

        
        self.type_label = ctk.CTkLabel(self.main_frame, text="İndirme Formatı:", font=ctk.CTkFont(weight="bold"), text_color=self.text_main)
        self.type_label.pack(anchor="w", padx=30, pady=(20, 5))

        self.radio_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.radio_frame.pack(fill="x", padx=30)

        self.download_type = ctk.StringVar(value="mp3")
        
        self.mp3_radio = ctk.CTkRadioButton(
            self.radio_frame, 
            text="🎵 Sadece Ses (MP3)", 
            variable=self.download_type, 
            value="mp3",
            text_color=self.text_main,
            hover_color=self.accent,
            fg_color=self.accent
        )
        self.mp3_radio.pack(side="left", padx=(0, 20))

        self.mp4_radio = ctk.CTkRadioButton(
            self.radio_frame, 
            text="🎬 Video + Ses (MP4)", 
            variable=self.download_type, 
            value="mp4",
            text_color=self.text_main,
            hover_color=self.accent,
            fg_color=self.accent
        )
        self.mp4_radio.pack(side="left")

        
        self.folder_label = ctk.CTkLabel(self.main_frame, text="Kayıt Yeri:", font=ctk.CTkFont(weight="bold"), text_color=self.text_main)
        self.folder_label.pack(anchor="w", padx=30, pady=(20, 5))

        self.folder_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.folder_frame.pack(fill="x", padx=30)

        self.folder_path_label = ctk.CTkLabel(
            self.folder_frame, 
            text=self.download_folder, 
            text_color=self.text_sub,
            anchor="w"
        )
        self.folder_path_label.pack(side="left", fill="x", expand=True)

        self.folder_btn = ctk.CTkButton(
            self.folder_frame, 
            text="📁 Değiştir", 
            width=100,
            fg_color="#dfe6e9", 
            text_color=self.text_main,
            hover_color="#b2bec3",
            command=self.select_folder
        )
        self.folder_btn.pack(side="right")

        
        self.progress_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.progress_frame.pack(fill="x", padx=30, pady=(30, 0))

        self.progress_label = ctk.CTkLabel(self.progress_frame, text="", text_color=self.text_sub, font=ctk.CTkFont(size=12))
        self.progress_label.pack(anchor="w", pady=(0, 5))

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, height=12, corner_radius=5, progress_color=self.accent)
        self.progress_bar.pack(fill="x")
        self.progress_bar.set(0)

       
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(pady=(30, 10))

        self.download_btn = ctk.CTkButton(
            self.button_frame, 
            text="⬇ İNDİRMEYİ BAŞLAT", 
            font=ctk.CTkFont(weight="bold", size=14),
            height=45,
            width=200,
            fg_color=self.accent,
            text_color="white",
            hover_color="#008f73",
            command=self.start_download
        )
        self.download_btn.pack(side="left", padx=10)

        self.clear_btn = ctk.CTkButton(
            self.button_frame, 
            text="🗑 TEMİZLE", 
            font=ctk.CTkFont(weight="bold", size=14),
            height=45,
            width=120,
            fg_color="#ff7675", 
            text_color="white",
            hover_color="#d63031",
            command=self.clear_form
        )
        self.clear_btn.pack(side="left", padx=10)

        
        self.status_label = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(weight="bold"))
        self.status_label.pack(pady=(10, 10))

    

    def select_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_folder)
        if folder:
            self.download_folder = folder
            self.folder_path_label.configure(text=folder)
    
    def clear_form(self):
        self.url_entry.delete(0, ctk.END)
        self.progress_bar.set(0)
        self.progress_label.configure(text="")
        self.status_label.configure(text="")
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                if 'downloaded_bytes' in d and 'total_bytes' in d:
                    percent = d['downloaded_bytes'] / d['total_bytes']
                    self.progress_bar.set(percent) 
                    self.progress_label.configure(text=f"İndiriliyor: %{percent*100:.1f} - {d.get('_speed_str', 'N/A')}")
                elif '_percent_str' in d:
                    percent_str = d['_percent_str'].strip().replace('%', '')
                    try:
                        percent = float(percent_str) / 100.0
                        self.progress_bar.set(percent)
                        self.progress_label.configure(text=f"İndiriliyor: %{percent*100:.1f} - {d.get('_speed_str', 'N/A')}")
                    except:
                        pass
            except Exception as e:
                pass
        
        elif d['status'] == 'finished':
            self.progress_bar.set(1.0)
            self.progress_label.configure(text="İndirme tamamlandı, dosya dönüştürülüyor (Lütfen bekleyin)...")
    
    def download_video(self):
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showerror("Hata", "Lütfen geçerli bir URL girin!")
            self.download_btn.configure(state="normal")
            return
        
        try:
            if self.download_type.get() == "mp3":
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'progress_hooks': [self.progress_hook],
                }
            else:
                ydl_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
                    'merge_output_format': 'mp4',
                    'progress_hooks': [self.progress_hook],
                }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Video')
            
            self.status_label.configure(text=f"✅ '{title[:30]}...' başarıyla indirildi!", text_color=self.accent)
            messagebox.showinfo("Başarılı", f"Dosya başarıyla indirildi!\n\nKonum: {self.download_folder}")
            
        except Exception as e:
            self.status_label.configure(text="❌ İndirme sırasında hata oluştu!", text_color="#d63031")
            messagebox.showerror("Hata", f"İndirme başarısız!\n\n{str(e)}")
        
        finally:
            self.download_btn.configure(state="normal")
            self.progress_bar.set(0)
            self.progress_label.configure(text="")
    
    def start_download(self):
        self.download_btn.configure(state="disabled")
        self.status_label.configure(text="⏳ Bağlantı kuruluyor, lütfen bekleyin...", text_color=self.text_main)
        self.progress_bar.set(0)
        
        thread = threading.Thread(target=self.download_video, daemon=True)
        thread.start()

if __name__ == "__main__":
    root = ctk.CTk()
    app = ModernDownloader(root)
    root.mainloop()