import tkinter as tk
from tkinter import filedialog

def start_gui():
    window = tk.Tk()
    window.title("어린이 노트 생성기")
    return window

def create_folder_selection(window):
    folder_var = tk.StringVar()

    folder_label = tk.Label(window, text="텍스트 파일이 있는 폴더:")
    folder_label.grid(row=0, column=1, padx=10, pady=10, sticky='e')

    folder_entry = tk.Entry(window, textvariable=folder_var, width=40)
    folder_entry.grid(row=0, column=2, padx=10, pady=10, sticky='w')

    return folder_var

def update_keywords(window):
    keywords = ["주제", "활동", "특징"]
    keyword_vars = []

    for i, keyword in enumerate(keywords):
        keyword_label = tk.Label(window, text=keyword)
        keyword_label.grid(row=i+1, column=1, padx=10, pady=10, sticky='e')

        keyword_var = tk.StringVar()
        keyword_entry = tk.Entry(window, textvariable=keyword_var, width=40)
        keyword_entry.grid(row=i+1, column=2, padx=10, pady=10, sticky='w')
        keyword_vars.append(keyword_var)

    return tuple(keyword_vars)

def create_activity_details(window):
    activity_details_label = tk.Label(window, text="활동 내용:")
    activity_details_label.grid(row=4, column=1, padx=10, pady=10, sticky='e')

    activity_details_frame = tk.Frame(window)
    activity_details_frame.grid(row=4, column=2, padx=10, pady=10, sticky='w')

    return activity_details_frame

def add_activity_detail(activity_details_frame):
    detail_var = tk.StringVar()
    detail_entry = tk.Entry(activity_details_frame, textvariable=detail_var, width=40)
    detail_entry.pack(padx=5, pady=5, side=tk.TOP)
    return detail_var

def create_result_textbox(window):
    result_textbox = tk.Text(window, wrap=tk.WORD, width=50, height=10)
    result_textbox.grid(row=6, column=1, padx=10, pady=20, columnspan=2, rowspan=3)

    return result_textbox
