import tkinter as tk
from tkinter import ttk, filedialog, messagebox  # Added messagebox import
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
        self.config_file = self.app_dir / "config.json"
        
        # Load or initialize settings
        self.load_settings()
        
        # Create main container
        self.container = ttk.Frame(root)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Create frames
        self.main_frame = ttk.Frame(self.container)
        self.settings_frame = ttk.Frame(self.container)
        self.sound_settings_frame = ttk.Frame(self.container)
        
        self.setup_main_frame()
        self.setup_settings_frame()
        self.setup_sound_settings_frame()
        
        # Show main frame initially
        self.show_main_frame()
        
        # Bind space bar event
        self.root.bind('<space>', self.next_number)

    def load_settings(self):
        default_settings = {
            'current_number': 1,
            'number_sounds': {}  # Dictionary to store number-sound mappings
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.settings = json.load(f)
                # Ensure all required keys exist
                for key in default_settings:
                    if key not in self.settings:
                        self.settings[key] = default_settings[key]
        else:
            self.settings = default_settings
            self.save_settings()

    def save_settings(self):
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
        
        sound_settings_btn = ttk.Button(self.settings_frame,
                                      text="Sound Settings",
                                      command=self.show_sound_settings_frame)
        sound_settings_btn.pack(pady=10)
        
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

    def setup_sound_settings_frame(self):
        # Sound settings frame widgets
        title_label = ttk.Label(self.sound_settings_frame, 
                              text="Sound Settings",
                              font=('Arial', 24))
        title_label.pack(pady=20)
        
        # Number sound mapping section
        mapping_frame = ttk.LabelFrame(self.sound_settings_frame, text="Number-Sound Mappings")
        mapping_frame.pack(pady=20, padx=20, fill='x')
        
        # Number entry
        number_frame = ttk.Frame(mapping_frame)
        number_frame.pack(pady=10, padx=10, fill='x')
        
        ttk.Label(number_frame, text="Number:").pack(side=tk.LEFT, padx=5)
        self.number_var = tk.StringVar()
        number_entry = ttk.Entry(number_frame, textvariable=self.number_var, width=10)
        number_entry.pack(side=tk.LEFT, padx=5)
        
        # Sound selection and buttons
        select_sound_btn = ttk.Button(mapping_frame,
                                    text="Select Sound File",
                                    command=self.select_sound_for_number)
        select_sound_btn.pack(pady=5, padx=10)
        
        test_sound_btn = ttk.Button(mapping_frame,
                                  text="Test Current Number Sound",
                                  command=self.test_number_sound)
        test_sound_btn.pack(pady=5, padx=10)
        
        # Display current mappings
        self.mappings_text = tk.Text(mapping_frame, height=10, width=40)
        self.mappings_text.pack(pady=10, padx=10)
        self.update_mappings_display()
        
        # Clear mapping button
        clear_btn = ttk.Button(mapping_frame,
                             text="Clear Selected Number Sound",
                             command=self.clear_number_sound)
        clear_btn.pack(pady=5, padx=10)
        
        back_btn = ttk.Button(self.sound_settings_frame,
                            text="Back to Settings",
                            command=self.show_settings_frame)
        back_btn.pack(pady=20)

    def update_mappings_display(self):
        self.mappings_text.delete('1.0', tk.END)
        for number, sound_file in sorted(self.settings['number_sounds'].items()):
            sound_path = Path(sound_file)
            self.mappings_text.insert(tk.END, f"Number {number}: {sound_path.name}\n")

    def select_sound_for_number(self):
        number = self.number_var.get().strip()
        if not number.isdigit() or not (1 <= int(number) <= 50):
            messagebox.showerror("Error", "Please enter a valid number between 1 and 50")
            return
            
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.ogg *.m4a *.flac *.aac"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            source_path = Path(file_path)
            new_path = self.app_dir / f"sound_{number}{source_path.suffix}"
            shutil.copy(file_path, new_path)
            self.settings['number_sounds'][number] = str(new_path)
            self.save_settings()
            self.update_mappings_display()

    def clear_number_sound(self):
        number = self.number_var.get().strip()
        if not number.isdigit() or not (1 <= int(number) <= 50):
            messagebox.showerror("Error", "Please enter a valid number between 1 and 50")
            return
            
        if number in self.settings['number_sounds']:
            sound_path = Path(self.settings['number_sounds'][number])
            if sound_path.exists():
                sound_path.unlink()  # Delete the sound file
            del self.settings['number_sounds'][number]
            self.save_settings()
            self.update_mappings_display()

    def play_sound_thread(self, sound_file):
        try:
            playsound(str(sound_file))
        except Exception as e:
            print(f"Error playing sound: {e}")

    def test_number_sound(self):
        number = self.number_var.get().strip()
        if not number.isdigit() or not (1 <= int(number) <= 50):
            messagebox.showerror("Error", "Please enter a valid number between 1 and 50")
            return
            
        if number in self.settings['number_sounds']:
            sound_file = Path(self.settings['number_sounds'][number])
            if sound_file.exists():
                threading.Thread(target=self.play_sound_thread, 
                              args=(sound_file,), 
                              daemon=True).start()
        else:
            messagebox.showinfo("Info", f"No sound assigned to number {number}")

    def play_number_sound(self, number):
        str_number = str(number)
        if str_number in self.settings['number_sounds']:
            sound_file = Path(self.settings['number_sounds'][str_number])
            if sound_file.exists():
                threading.Thread(target=self.play_sound_thread, 
                              args=(sound_file,), 
                              daemon=True).start()

    def next_number(self, event=None):
        if self.settings['current_number'] < 50:
            self.settings['current_number'] += 1
            current = self.settings['current_number']
            self.number_label.config(text=str(current).zfill(2))
            self.save_settings()
            self.play_number_sound(current)

    def reset_counter(self):
        self.settings['current_number'] = 1
        self.number_label.config(text="01")
        self.save_settings()
        self.show_main_frame()

    def show_main_frame(self):
        self.settings_frame.pack_forget()
        self.sound_settings_frame.pack_forget()
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def show_settings_frame(self):
        self.main_frame.pack_forget()
        self.sound_settings_frame.pack_forget()
        self.settings_frame.pack(fill=tk.BOTH, expand=True)

    def show_sound_settings_frame(self):
        self.main_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.sound_settings_frame.pack(fill=tk.BOTH, expand=True)

def main():
    root = tk.Tk()
    app = PriorityNumberApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()