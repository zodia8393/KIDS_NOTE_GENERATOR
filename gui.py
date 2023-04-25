import tkinter as tk
from tkinter import filedialog

def start_gui():
    window = tk.Tk()
    window.title("어린이 노트 생성기")
    return window

def create_folder_selection(window):
    folder_var = tk.StringVar()

    folder_label = tk.Label(window, text="텍스트 파일이 있는 폴더:")
    folder_label.grid(row=0, column=0, padx=10, pady=10)

    folder_entry = tk.Entry(window, textvariable=folder_var)
    folder_entry.grid(row=0, column=1, padx=10, pady=10)

    folder_button = tk.Button(window, text="폴더 선택", command=lambda: folder_var.set(filedialog.askdirectory()))
    folder_button.grid(row=0, column=2, padx=10, pady=10)

    return folder_var

def update_keywords(window):
    keywords = ["수업목표", "수업내용", "교재 및 재료", "선생님 소개", "활동내용", "권장사항", "성과평가", "학습결과", "질문과 답변", "보조자료", "피드백"]
    keyword_vars = []

    for i, keyword in enumerate(keywords):
        keyword_label = tk.Label(window, text=keyword)
        keyword_label.grid(row=i+1, column=0, padx=10, pady=10)

        keyword_var = tk.StringVar()
        keyword_entry = tk.Entry(window, textvariable=keyword_var)
        keyword_entry.grid(row=i+1, column=1, padx=10, pady=10)
        keyword_vars.append(keyword_var)

    return tuple(keyword_vars)

def create_generate_button(window, callback):
    generate_button = tk.Button(window, text="생성하기", command=callback)
    generate_button.grid(row=len(window.grid_slaves())+1, column=0, padx=10, pady=10, columnspan=3)
