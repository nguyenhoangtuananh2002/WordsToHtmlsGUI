import subprocess
import tkinter as tk
from tkinter import filedialog, HORIZONTAL, ttk, messagebox
import os
import mammoth


def browse_files():
    global folder_path
    convert_button['state'] = tk.DISABLED
    progress_bar['value'] = 0
    open_button['state'] = tk.DISABLED
    folder_path = filedialog.askdirectory(initialdir="/",
                                          title="Select DOCX Files",
                                          )
    text_box.delete('1.0', tk.END)

    if folder_path:
        text_box.insert(tk.END, folder_path)
        convert_button['state'] = tk.ACTIVE
    else:
        text_box.insert(tk.END, 'no folder selected')


def convert_files():
    global html_paths_temp

    docx_paths, html_paths = scan_file_word()
    html_paths = [None] * len(docx_paths)
    result = [None] * len(docx_paths)
    html = [None] * len(docx_paths)
    html_spacing = [None] * len(docx_paths)
    html_no_p = [None] * len(docx_paths)
    lines = [None] * len(docx_paths)
    centered_html = [None] * len(docx_paths)
    escaped_html = [None] * len(docx_paths)
    html_open = [None] * len(docx_paths)
    progress_bar['value'] = 0
    progress_bar['max'] = len(docx_paths)
    open_button['state'] = tk.DISABLED
    try:
        for i in range(len(docx_paths)):
            html_paths[i] = docx_paths[i].replace('docx', 'html')
            with open(docx_paths[i], 'rb') as docx_paths[i]:
                result[i] = mammoth.convert_to_html(docx_paths[i])
                html[i] = result[i].value
                html_spacing[i] = html[i].replace('</p>', '</p><br>')
                html_no_p[i] = html_spacing[i].replace('<p>', '')
                escaped_html[i] = html_no_p[i].replace('"', '\\"')
                lines[i] = escaped_html[i].split('</p><br>')
                if lines:
                    lines[i][0] = f'<center>{lines[i][0]}</center>'
                centered_html[i] = '</p><br>'.join(lines[i])
            with open(html_paths[i], 'w', encoding='utf-8') as html_paths[i]:
                if html_paths[i].write(centered_html[i]):
                    progress_bar['value'] += 1
                    Window.update_idletasks()
        messagebox.showinfo('success', f'Conversion Success')
        open_button['state'] = tk.ACTIVE
    except Exception as e:
        messagebox.showerror('Error', f'There are Error in process {e}')


def scan_file_word():
    global folder_path
    docx_paths = []
    html_paths = []
    if folder_path:
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.docx'):
                docx_path = os.path.join(folder_path, file_name)
                html_path = os.path.join(
                    folder_path, file_name.replace(
                        '.docx', '.html'))
                docx_paths.append(docx_path)
                html_paths.append(html_path)
    return docx_paths, html_paths


def open_output_folder():
    global folder_path
    new_folder_path = folder_path.replace('/', '\\')
    subprocess.Popen(f'explorer "{new_folder_path}"')


def create_window():
    global progress_bar, text_box, Window, convert_button, open_button

    Window = tk.Tk()
    Window.title('Convert Docx Files to HTML')
    Window.configure(background='White')
    Window.minsize(600, 500)

    docx_label = tk.Label(
        Window,
        text="No DOCX file selected",
        bg="white",
    )

    docx_button = tk.Button(
        Window,
        text='Browse Docx File',
        width=25,
        command=browse_files
    )
    docx_button.pack(pady=10)

    text_box = tk.Text(Window, height=10, width=70)
    text_box.pack(pady=10)

    progress_bar = ttk.Progressbar(
        Window,
        orient=HORIZONTAL,
        length=100,
        mode='determinate')
    progress_bar.pack(pady=10)

    convert_button = tk.Button(
        Window,
        text='Click to Convert',
        width=25,
        state=tk.DISABLED,
        command=convert_files
    )
    convert_button.pack(pady=10)

    open_button = tk.Button(
        Window,
        text='Open Output Folder',
        width=25,
        state=tk.DISABLED,
        command=open_output_folder
    )
    open_button.pack(pady=10)

    Window.mainloop()


def main():
    create_window()


if __name__ == '__main__':
    main()
