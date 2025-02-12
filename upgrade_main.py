import tkinter as tk
import time
import os
import threading
import webbrowser
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import mammoth

def convert_to_html(folder_path):
    try:
        docx_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".docx")]
        if not docx_paths:
            messagebox.showwarning("No Files", "No .docx file found in the selected folder.")
            return
        total_files=len(docx_paths)
        for index, docx_path in enumerate(docx_paths):
            progress_label.config(text=f"Converting file {index+1}/{total_files}...",fg="blue")
            progress_bar["value"]=(index/total_files)*100
            root.update_idletasks()
            with open(docx_path, "rb") as docx_file:
                result = mammoth.convert_to_html(docx_file)
                html_content = result.value
                escaped_html = html_content.replace('"', '\\"')
                space_html = escaped_html.replace('</p>','</p><br>')
                html_no_p = space_html.replace('<p>','')
                lines = html_no_p.split('</p><br>')
                if lines:
                    lines[0] = f'<center>{lines[0]}</center>'
                for i in range(1, len(lines)):
                    lines[i] = f'{lines[i]}</p>'
                centered_html = '</p><br>'.join(lines)
            output_path=os.path.splitext(docx_path)[0]+".html"
            with open (output_path,"w",encoding= "utf-8") as html_file:
                html_file.write(centered_html)
            time.sleep(0.5)
        progress_bar["value"]=100
        progress_label.config(text="Conversion completed!", fg="green")
        messagebox.showinfo("Success", "All files have been converted successfully!")
        def open_directory():
            directory = os.path.dirname(output_path)
            webbrowser.open(directory)
        success_message=tk.Toplevel(root)
        success_message.title("Success")
        tk.Label(success_message,
                text=f"Conversion completed\nHTML files saved at:\n{folder_path}",
                wraplength=300).pack(pady=10)
        tk.Button(success_message, text="Open Directory", command = open_directory).pack(pady=5)
        tk.Button(success_message, text=f"Close", command = root.destroy).pack(pady=5)
    except Exception as e:
        progress_bar.stop()
        progress_label.config(text="Conversion failed!", fg="red")
        messagebox.showerror("Error",f"An error occurred: {e}")
    finally:
        progress_bar.stop()
        convert_button.config(state=tk.NORMAL)

def select_folder_and_convert():
    global folder_path
    folder_path=filedialog.askdirectory(title="Select Folder Containing Word Files")
    if not folder_path:
        return
    selected_folder_label.config(text=f"Selected Folder: {folder_path}",fg="blue")
    convert_button.config(state=tk.NORMAL)

def convert_folder_to_html():
    if not folder_path:
        messagebox.showerror("Error",f"An error occurred: {e}")
        return
    convert_button.config(state=tk.DISABLED)
    threading.Thread(target=convert_to_html,args=(folder_path,),daemon=True).start()

def update_progress(percent):
    progress_bar["value"]=percent
    progress_bar.update_idletasks()
root = tk.Tk() 
root.title("Word to HTML Converter")
root.geometry("500x300")
root.resizable(False, False)
instruction_label=tk.Label(root, text="Select a folder containing .docx files and click 'Convert' to generate HTML files", fg="blue", wraplength=500)
instruction_label.pack(pady=10)
selected_folder_label=tk.Label(root, text="No folder selected.",fg="red",wraplength=400)
selected_folder_label.pack(pady=5)
open_button = tk.Button(root, text="Select Folder", command = select_folder_and_convert)
open_button.pack(pady=10)
convert_button=tk.Button(root, text="Convert to HTML", command = convert_folder_to_html, state=tk.DISABLED)
convert_button.pack(pady=10)
progress_bar=Progressbar(root, mode="determinate", length=400)
progress_bar.pack(pady=10)
progress_label=tk.Label(root, text="",fg="blue",wraplength=400)
progress_label.pack(pady=10)
root.mainloop()
    
    
