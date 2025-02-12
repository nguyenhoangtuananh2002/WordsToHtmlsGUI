import tkinter as tk
import time
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import os
import threading
import webbrowser
import time
import mammoth

def convert_to_html(docx_path):
    try:
        progress_label.config(text="Converting...",fg="blue")
        progress_bar.start(10)
        update_progress(25)
        time.sleep(1)
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
        update_progress(50)
        time.sleep(1)
        output_path=os.path.splitext(docx_path)[0]+".html"
        with open (output_path,"w",encoding= "utf-8") as html_file:
            html_file.write(centered_html)
        update_progress(75)
        time.sleep(1)
        update_progress(100)
        progress_bar.stop()
        progress_label.config(text="Conversion completed!", fg="green")
        def open_directory():
            directory = os.path.dirname(output_path)
            webbrowser.open(directory)
        success_message=tk.Toplevel(root)
        success_message.title("Success")
        tk.Label(success_message,text=f"Conversion completed\nHTML saved at:\n{output_path}",wraplength=300).pack(pady=10)
        tk.Button(success_message, text="Open Directory", command = open_directory).pack(pady=5)
        tk.Button(success_message, text=f"Close", command = root.destroy).pack(pady=5)
    except Exception as e:
        progress_bar.stop()
        progress_label.config(text="Conversion failed!", fg="red")
        messagebox.showerror("Error",f"An error occurred: {e}")
def update_progress(percent):
    progress_bar["value"]=percent
    progress_bar.update_idletasks()
def start_conversion():
    thread=threading.Thread(target=convert_to_html, args=(selected_file_path,))
    thread.start()
def open_file():
    global selected_file_path
    file_path = filedialog.askopenfilename(
        filetypes = [("Word Documents", "*.docx")],
        title="Select a .docx file"
        )
    if file_path:
        selected_file_path=file_path
        selected_file_label.config(text=f"Selected file: {file_path}", fg="blue")
        convert_button.config(state=tk.NORMAL)
    else:
        selected_file_label.config(text="No file selected.")
        convert_button.config(state=tk.DISABLED)
root = tk.Tk() 
root.title("Word to HTML Converter")
root.geometry("500x300")
root.resizable(False, False)
instruction_label=tk.Label(root, text="Select a .docx file and click 'Convert' to generate an HTML file", fg="blue", wraplength=400)
instruction_label.pack(pady=10)
selected_file_label=tk.Label(root, text="No file selected.",fg="red",wraplength=400)
selected_file_label.pack(pady=5)
open_button = tk.Button(root, text="Select .docx File", command = open_file)
open_button.pack(pady=10)
convert_button=tk.Button(root, text="Convert to HTML", command = start_conversion, state=tk.DISABLED)
convert_button.pack(pady=10)
progress_bar=Progressbar(root, mode="determinate", length=400)
progress_bar.pack(pady=10)
progress_label=tk.Label(root, text="",fg="blue",wraplength=400)
progress_label.pack(pady=10)
root.mainloop()
    
    
