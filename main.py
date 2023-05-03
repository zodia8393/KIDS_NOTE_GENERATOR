# main.py
import tkinter as tk
from tkinter import filedialog
from generator import fine_tune_model, generate_note, save_and_load_model
from gui import start_gui, create_folder_selection, update_keywords, create_activity_details, add_activity_detail, create_result_textbox

def select_folder():
    global model  # Move this line to the top
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_var.set(folder_path)
        model_var.set("미세조정 중...")
        window.update()
        model = fine_tune_model(folder_path)
        model_var.set("미세조정 완료!")

        # Save and load the fine-tuned model
        save_and_load_model(folder_path)

def generate():
    if model is None:
        result_textbox.delete(1.0, tk.END)
        result_textbox.insert(tk.END, "먼저 폴더를 선택하여 모델을 미세조정하세요.")
        return

    keywords = {
        "주제": topic_var.get(),
        "활동": activity_var.get(),
        "특징": feature_var.get(),
        "활동내용": [detail_var.get() for detail_var in activity_detail_vars]
    }
    folder_path = "학습된_어린이_노트_파일_폴더_경로"
    result = generate_note(model, keywords)
    result_textbox.delete(1.0, tk.END)
    result_textbox.insert(tk.END, result)

model = None
window = start_gui()

window.configure(bg='#f0f0f0')
window.option_add("*Font", "TkDefaultFont 9")

folder_var = create_folder_selection(window)

topic_var, activity_var, feature_var = update_keywords(window)

activity_details_frame = create_activity_details(window)
activity_detail_vars = []

def add_detail():
    detail_var = add_activity_detail(activity_details_frame)
    activity_detail_vars.append(detail_var)

add_detail_button = tk.Button(window, text="활동 내용 추가", command=add_detail, bg='#2196F3', fg='white', relief='raised', width=12, height=1)
add_detail_button.grid(row=4, column=0, padx=10, pady=10)

generate_btn = tk.Button(window, text="생성", command=generate, bg='#4CAF50', fg='white', relief='raised', width=10, height=2)
generate_btn.grid(row=6, column=0, padx=10, pady=20)

result_textbox = create_result_textbox(window)

# Model variable and label
model_var = tk.StringVar()
model_var.set("미세조정 대기 중")
model_label = tk.Label(window, textvariable=model_var, bg='#f0f0f0')
model_label.grid(row=0, column=2, padx=10, pady=10)

folder_btn = tk.Button(window, text="폴더 선택", command=select_folder, bg='#2196F3', fg='white', relief='raised', width=10, height=1)
folder_btn.grid(row=0, column=0, padx=10, pady=10)

window.mainloop()
