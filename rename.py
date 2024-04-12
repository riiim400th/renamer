import os
import tkinter as tk
from tkinter import filedialog, messagebox
import locale

language, _ = locale.getdefaultlocale()
if language == "ja_JP":
    from ms_ja import *
else:
    from ms_us import *

class FileRenamer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Renamer")

        self.select_label = tk.Label(self, text=dt_root_ms)
        self.select_label.pack()

        self.file_listbox = tk.Listbox(self, width=80, height=10)
        self.file_listbox.pack()

        self.rename_button = tk.Button(self, text=dt_root_text, command=self.rename_file)
        self.rename_button.pack(pady=20)

    def rename_file(self):
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            self.update_file_listbox(file_paths)

        name_input = self.get_multiline_input("Rename File", ms_newnames)
        if name_input is None:
            messagebox.showwarning("Error", ms_noinput)
            return

        new_filenames = name_input.split('\n')
        if len(file_paths) != len(new_filenames):
            messagebox.showwarning("Error", ms_dontmatch)
            return

        self.renamed_files = []
        for file_path, new_name in zip(file_paths, new_filenames):
            dir, old_name_e = os.path.split(file_path)
            _, extension = os.path.splitext(old_name_e)
            old_path = file_path
            new_name_e = new_name.strip() + extension
            new_path = os.path.join(dir, new_name_e)
            os.rename(old_path, new_path)
            self.renamed_files.append((old_name_e, new_name_e))

        messagebox.showinfo("Success", ms_success)
        self.show_renamed_files(self.renamed_files)

    def update_file_listbox(self, file_paths):
        self.file_listbox.delete(0, tk.END)
        for file_path in file_paths:
            _, filename_e = os.path.split(file_path)
            filename, _ = os.path.splitext(filename_e)
            self.file_listbox.insert(tk.END, filename)

    def get_multiline_input(self, title, prompt):
        dialog = tk.Toplevel(self)
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

    def show_renamed_files(self, files):
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

if __name__ == "__main__":
    app = FileRenamer()
    app.mainloop()