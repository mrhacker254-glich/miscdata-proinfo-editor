import os
import struct
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import time

class GlowFrame(tk.Frame):
    def __init__(self, master, color="blue", glow_size=9):
        super().__init__(master, bg=color)
        self.glow_size = glow_size
        self.inner_frame = tk.Frame(self, bg='#f0f0f0')
        self.inner_frame.pack(expand=True, fill='both', padx=glow_size, pady=glow_size)
        self.glow_colors = self._generate_glow_colors(color)
        self._current_glow = 0
        self._animate_glow()

    def _generate_glow_colors(self, base_color):
        
        colors = []
        r = int(base_color[1:3], 16)
        g = int(base_color[3:5], 16)
        b = int(base_color[5:7], 16)
        for i in range(10):
            factor = i / 10
            color = f'#{int(r*factor):02x}{int(g*factor):02x}{int(b*factor):02x}'
            colors.append(color)
        return colors

    def _animate_glow(self):
        self._current_glow = (self._current_glow + 1) % len(self.glow_colors)
        self.configure(bg=self.glow_colors[self._current_glow])
        self.after(100, self._animate_glow)

def edit_file(file_path):
    try:
        with open(file_path, 'rb+') as f:
            
            f.seek(0, os.SEEK_END)
            file_size = f.tell()
            
            for offset in range(0x000C1000, 0x000C1040 + 7):
                if file_size > offset:
                    f.seek(offset)
                    f.write(b'\x00')
                else:
                    messagebox.showwarning("Warning", f"File too small for modification at {hex(offset)}.")
                    return
            
        
            target_offset = 0x000C17F0 + 6  
            if file_size > target_offset:
                f.seek(target_offset)
                f.write(struct.pack('B', 0x3A))
            else:
                messagebox.showwarning("Warning", f"File too small for modification at {hex(target_offset)}.")
                return
            
        messagebox.showinfo("Success", f"security plugin and mdm successfully removed inthe miscdata,you can now restore the miscdata and super file if you want mdm file contact +254113399438")
    except Exception as e:
        messagebox.showerror("Error", f"Error editing file: {e}")

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("BIN & IMG Files", "*.bin;*.img")])
    if file_path:
        edit_file(file_path)

def create_gui():
    root = tk.Tk()
    root.title("JoseTek File Modifier")
    root.geometry("400x300")
    root.resizable(False, False)
    root.configure(bg='black')
    
    
    glow_frame = GlowFrame(root, color="#00ff00", glow_size=3)
    glow_frame.pack(expand=True, fill='both', padx=2, pady=2)
    
    style = ttk.Style()
    style.configure('Custom.TButton', padding=10)
    style.configure('Custom.TFrame', background='#f0f0f0')
    
    main_frame = ttk.Frame(glow_frame.inner_frame, padding="20", style='Custom.TFrame')
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    title_label = ttk.Label(
        main_frame, 
        text="JoseTek misceditor",
        font=('Helvetica', 16, 'bold')
    )
    title_label.pack(pady=(0, 20))
    
  
    instr_label = ttk.Label(
        main_frame,
        text="Select a .img or .bin file to remove mdm:",
        font=('Helvetica', 10, 'bold')
    )
    instr_label.pack(pady=(0, 10))
    

    select_btn = ttk.Button(
        main_frame,
        text="Select miscdata.img/bin",
        command=select_file,
        style='Custom.TButton'
    )
    select_btn.pack(pady=10)
    
    status_frame = ttk.Frame(root)
    status_frame.pack(fill=tk.X, side=tk.BOTTOM)
    status_label = ttk.Label(
        status_frame,
        text="Ready",
        relief=tk.SUNKEN,
        anchor=tk.W,
        padding=(5, 2)
    )
    status_label.pack(fill=tk.X)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()