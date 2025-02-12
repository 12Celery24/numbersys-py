import tkinter as tk
from tkinter import ttk, filedialog
import os
import shutil
from playsound import playsound
import json
from pathlib import Path
import threading

class PriorityNumberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Priority Number System")
        self.root.geometry("800x600")
        
        # Create data directory if it doesn't exist
        self.app_dir = Path.home() / "PriorityNumberSystem"
        self.app_dir.mkdir(exist_ok=True)
        self.sound_file = None  # Will be set when sound is selected
        self.config_file = self.app_dir / "config.json"
        
        # Load or initialize settings
        self.load_settings()
        
        # Create main container
        self.container = ttk.Frame(root)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Create frames
        self.main_frame = ttk.Frame(self.container)
        self.settings_frame = ttk.Frame(self.container)
        
        self.setup_main_frame()
        self.setup_settings_frame()
        
        # Show main frame initially
        self.show_main_frame()
        
        # Bind space bar event
        self.root.bind('<space>', self.next_number)

    def load_settings(self):
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.settings = json.load(f)
                if self.settings.get('sound_file'):
                    self.sound_file = Path(self.settings['sound_file'])
        else:
            self.settings = {
                'current_number': 1,
                'sound_file': None
            }
            self.save_settings()

    def save_settings(self):
        self.settings['sound_file'] = str(self.sound_file) if self.sound_file else None
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f)

    def setup_main_frame(self):
        # Configure main display styles
        style = ttk.Style()
        style.configure('Number.TLabel', font=('Arial', 120, 'bold'))
        style.configure('Title.TLabel', font=('Arial', 24))
        
        # Main frame widgets
        title_label = ttk.Label(self.main_frame, text="Now Serving", style='Title.TLabel')
        title_label.pack(pady=20)
        
        self.number_label = ttk.Label(self.main_frame, 
                                    text=str(self.settings['current_number']).zfill(2),
                                    style='Number.TLabel')
        self.number_label.pack(pady=40)
        
        instruction_label = ttk.Label(self.main_frame, 
                                    text="Press SPACE BAR to call next number",
                                    font=('Arial', 14))
        instruction_label.pack(pady=20)
        
        settings_button = ttk.Button(self.main_frame, 
                                   text="Settings",
                                   command=self.show_settings_frame)
        settings_button.pack(pady=10)

    def setup_settings_frame(self):
        # Settings frame widgets
        title_label = ttk.Label(self.settings_frame, 
                              text="Settings",
                              font=('Arial', 24))
        title_label.pack(pady=20)
        
        # Sound settings section
        sound_frame = ttk.LabelFrame(self.settings_frame, text="Sound Settings")
        sound_frame.pack(pady=20, padx=20, fill='x')
        
        # Current sound label
        self.current_sound_label = ttk.Label(sound_frame, 
                                           text="No sound selected",
                                           font=('Arial', 10))
        self.current_sound_label.pack(pady=5, padx=10)
        if self.sound_file:
            self.current_sound_label.config(text=f"Current sound: {self.sound_file.name}")
        
        select_sound_btn = ttk.Button(sound_frame,
                                    text="Select Sound File",
                                    command=self.select_sound)
        select_sound_btn.pack(pady=10, padx=10)
        
        test_sound_btn = ttk.Button(sound_frame,
                                  text="Test Sound",
                                  command=self.test_sound)
        test_sound_btn.pack(pady=10, padx=10)
        
        # Counter settings section
        counter_frame = ttk.LabelFrame(self.settings_frame, text="Counter Settings")
        counter_frame.pack(pady=20, padx=20, fill='x')
        
        reset_btn = ttk.Button(counter_frame,
                             text="Reset Counter to 1",
                             command=self.reset_counter)
        reset_btn.pack(pady=10, padx=10)
        
        back_btn = ttk.Button(self.settings_frame,
                            text="Back to Main Display",
                            command=self.show_main_frame)
        back_btn.pack(pady=20)

    def select_sound(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.ogg *.m4a *.flac *.aac"),
                ("MP3 Files", "*.mp3"),
                ("WAV Files", "*.wav"),
                ("OGG Files", "*.ogg"),
                ("M4A Files", "*.m4a"),
                ("FLAC Files", "*.flac"),
                ("AAC Files", "*.aac"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            # Copy file to app directory with original extension
            source_path = Path(file_path)
            new_path = self.app_dir / f"notification{source_path.suffix}"
            shutil.copy(file_path, new_path)
            self.sound_file = new_path
            self.current_sound_label.config(text=f"Current sound: {self.sound_file.name}")
            self.save_settings()

    def play_sound_thread(self):
        try:
            playsound(str(self.sound_file))
        except Exception as e:
            print(f"Error playing sound: {e}")

    def test_sound(self):
        if self.sound_file and self.sound_file.exists():
            threading.Thread(target=self.play_sound_thread, daemon=True).start()

    def play_sound(self):
        if self.sound_file and self.sound_file.exists():
            threading.Thread(target=self.play_sound_thread, daemon=True).start()

    def next_number(self, event=None):
        if self.settings['current_number'] < 50:
            self.settings['current_number'] += 1
            self.number_label.config(text=str(self.settings['current_number']).zfill(2))
            self.save_settings()
            self.play_sound()

    def reset_counter(self):
        self.settings['current_number'] = 1
        self.number_label.config(text="01")
        self.save_settings()
        self.show_main_frame()

    def show_main_frame(self):
        self.settings_frame.pack_forget()
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def show_settings_frame(self):
        self.main_frame.pack_forget()
        self.settings_frame.pack(fill=tk.BOTH, expand=True)

def main():
    root = tk.Tk()
    app = PriorityNumberApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()