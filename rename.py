import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import locale
language, _ = locale.getdefaultlocale()
if language == "ja_JP":
    from ms_ja import *
else:
    from ms_us import *

def rename_file():
    file_paths = filedialog.askopenfilenames()
    
    name_input = get_multiline_input("Rename File", ms_newnames)
    if name_input is None:
        messagebox.showwarning("Error", ms_noinput)
        return
    
    new_filenames = name_input.split('\n')
    
    if len(file_paths) != len(new_filenames):
        messagebox.showwarning("Error", ms_dontmatch)
        return
    
    renamed_files = []
    if file_paths:
        for file_path, new_name in zip(file_paths, new_filenames):
            dic, old_name_e = os.path.split(file_path)
            _ , extension = os.path.splitext(old_name_e)
            old_path = file_path
            new_name_e = new_name.strip()+extension
            new_path = os.path.join(dic, new_name_e)
            os.rename(old_path, new_path)
            renamed_files.append((old_name_e, new_name_e))
        messagebox.showinfo("Success", ms_success)
        show_renamed_files(renamed_files)

def get_multiline_input(title, prompt):
    dialog = tk.Toplevel(root)
    dialog.title(title)
    
    label = tk.Label(dialog, text=prompt)
    label.pack()
    
    text_widget = tk.Text(dialog, width=50, height=10)
    text_widget.pack()
    
    result = None
    
    button_frame = tk.Frame(dialog)
    button_frame.pack()
    
    def ok_click():
        nonlocal result
        result = text_widget.get("1.0", tk.END).strip()
        dialog.destroy()
    
    ok_button = tk.Button(button_frame, text="OK", command=ok_click)
    ok_button.pack(side=tk.LEFT)
    
    cancel_button = tk.Button(button_frame, text="Cancel", command=dialog.destroy)
    cancel_button.pack(side=tk.LEFT)
    
    dialog.wait_window()
    return result


def show_renamed_files(files):
    dialog = tk.Toplevel()
    dialog.title(dt_top)
    
    label = tk.Label(dialog, text=dt_top_text)
    label.pack()
    
    listbox = tk.Listbox(dialog, width=80, height=10)
    for old_path, new_path in files:
        listbox.insert(tk.END, f"{old_path} -> {new_path}")
    listbox.pack()
    
    close_button = tk.Button(dialog, text="Close", command=dialog.destroy)
    close_button.pack()





root = tk.Tk()
root.title("File Renamer")

select_label = tk.Label(root, text=dt_root_ms)
select_label.pack()

rename_button = tk.Button(root, text=dt_root_text, command=rename_file)
rename_button.pack(pady=20)

root.mainloop()



