from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import ctypes
from functools import partial
from idlelib.tooltip import Hovertip

ctypes.windll.shcore.SetProcessDpiAwareness(True)

name = "LiteHex"
padding = 5

# Setup
root = Tk()
root.geometry('600x600')
root.title(name)
root.iconbitmap("icon.ico")

def null():
    messagebox.showerror('LiteHex - Error', 'Error: This Function is still in development!')

s = ttk.Style()
s.theme_use('clam')

save_img = PhotoImage(file="save.png")
open_img = PhotoImage(file="open.png")
about_img = PhotoImage(file="about.png")
com_img = PhotoImage(file="compare.png")

# Notebook setup
notebook = ttk.Notebook(root)
notebook.pack(fill=X, pady=(0, 0))

style = ttk.Style(root)
style.configure('TNotebook.Tab', width=1000)

file_tab = Frame(notebook)
notebook.add(file_tab, text='File')

edit_tab = Frame(notebook)
notebook.add(edit_tab, text='Edit')

help_tab = Frame(notebook)
notebook.add(help_tab, text='Help')

# Guide label
guide = Label(root, text="00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F Offset   Decoded:", font=("Courier", 10), anchor="w")
guide.pack(fill=X)

# Text widgets
txt = Text(root, width=48, undo=True)
txt.pack(fill=BOTH, expand=False, side=LEFT)

offset_text = Text(root, width=9, state=DISABLED)
offset_text.pack(fill=BOTH, expand=False, side=LEFT)

decoded = Text(root, width=16)
decoded.pack(fill=BOTH, expand=False, side=LEFT)

filePath = ""

def update_decoded_and_offset(*args):
    """Update offset and decoded text dynamically."""
    try:
        hex_data = txt.get(1.0, "end").strip().replace(" ", "").replace("\n", "")
        binary_data = bytes.fromhex(hex_data)

        # Update offsets
        offset_text.config(state=NORMAL)
        offset_text.delete(1.0, "end")
        for i in range(0, len(binary_data), 16):
            offset_text.insert("end", f"{i:08X}\n")
        offset_text.config(state=DISABLED)

        # Update decoded text
        decoded.delete(1.0, "end")
        for i in range(0, len(binary_data), 16):
            line = binary_data[i:i+16]
            decoded_text = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in line)
            decoded.insert("end", decoded_text + "\n")

    except ValueError:
        # Invalid hex data
        decoded.delete(1.0, "end")
        offset_text.config(state=NORMAL)
        offset_text.delete(1.0, "end")
        offset_text.config(state=DISABLED)

txt.bind("<KeyRelease>", update_decoded_and_offset)

def open_file():
    global filePath
    filePath = askopenfilename(filetypes=[("All files", "*.*")])
    if not filePath:
        return
    
    try:
        with open(filePath, 'rb') as fp:
            file_content = fp.read()
        
        # Generate hex and decoded text
        hex_list = ["{:02x}".format(byte) for byte in file_content]

        txt.delete(1.0, "end")
        txt.insert("end", "\n".join(" ".join(hex_list[i:i+16]) for i in range(0, len(hex_list), 16)))
        
        # Trigger update for offsets and decoded text
        update_decoded_and_offset()

        root.title(f'{name} - {filePath}')
    
    except Exception as e:
        messagebox.showerror('Error Opening File', f'Error: Unable to open file.\n{e}')


def save_file():
    global filePath
    if not filePath:
        filePath = asksaveasfilename(defaultextension=".txt", 
                                     filetypes=[("Text files", "*.txt"), 
                                                ("All files", "*.*")])
        if not filePath:
            return
    
    try:
        hex_data = txt.get(1.0, "end").strip().replace(" ", "").replace("\n", "")
        binary_data = bytes.fromhex(hex_data)

        with open(filePath, 'wb') as f:
            f.write(binary_data)
        
        messagebox.showinfo('Save File', f'File saved successfully as {filePath}')
    except ValueError as e:
        messagebox.showerror('Save Error', f'Error: Invalid hex data.\n{e}')


def about():
    abt = Toplevel()
    abt.title("About LiteHex")
    abt.iconbitmap("icon.ico")
    abt.configure(bg="#DCDAD5")

    abt.banner_img = PhotoImage(file="banner.png")

    banner = Label(abt, image=abt.banner_img)
    banner.pack(side=LEFT, padx=5)
    
    # Store the image as an attribute of the window
    abt.logo_img = PhotoImage(file="logo.png")
    img = Label(abt, image=abt.logo_img)
    img.pack()
    
    title = Label(abt, text="LiteHex", font=("FixedSys", 25))
    title.pack()

    txt = Label(abt, text="""
A simple Hexeditor.

by Sebastian Taylor
Version: 1.0
""")
    txt.pack(padx=30, pady=30)


save_button = Button(file_tab, image=save_img, command=save_file)
save_button.pack(side=LEFT, padx=5, pady=5)
Hovertip(save_button, 'Save File\nCtrl+S\n\nSave the current File.')

open_button = Button(file_tab, image=open_img, command=open_file)
open_button.pack(side=LEFT, padx=5, pady=5)
Hovertip(open_button, 'Open File\nCtrl+O\n\nOpen a File.')

abt_button = Button(help_tab, image=about_img, command=about)
abt_button.pack(side=LEFT, padx=5, pady=5)
Hovertip(abt_button, 'About\nF1\n\nOpen the about screen.')

com_button = Button(edit_tab, image=com_img, command=null)
com_button.pack(side=LEFT, padx=5, pady=5)
tip_com = Hovertip(com_button,'Compare Data\nCtrl+K\n\nCompare two files hex data')

root.mainloop()
