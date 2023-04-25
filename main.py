import tkinter as tk
from tkinter import filedialog
from generator import fine_tune_model, generate_note
from gui import start_gui, update_keywords

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        model_var.set("미세조정 중...")
        window.update()
        global model
        model = fine_tune_model(folder_path)
        model_var.set("미세조정 완료!")

def generate():
    keywords = {
        "수업목표": goal_var.get(),
        "수업내용": content_var.get(),
        "교재 및 재료": materials_var.get(),
        "선생님 소개": teacher_var.get(),
        "활동내용": activities_var.get(),
        "권장사항": recommendations_var.get(),
        "성과평가": evaluation_var.get(),
        "학습결과": results_var.get(),
        "질문과 답변": qna_var.get(),
        "보조자료": supplementary_var.get(),
        "피드백": feedback_var.get()
    }
    result = generate_note(model, keywords)
    result_var.set(result)

model = None
window = start_gui()

folder_btn = tk.Button(window, text="폴더 선택", command=select_folder)
folder_btn.grid(row=0, column=0, padx=10, pady=10)

model_var = tk.StringVar()
model_var.set("미세조정 대기 중")
model_label = tk.Label(window, textvariable=model_var)
model_label.grid(row=0, column=1)

goal_var, content_var, materials_var, teacher_var, activities_var, recommendations_var, evaluation_var, results_var, qna_var, supplementary_var, feedback_var = update_keywords(window)

generate_btn = tk.Button(window, text="생성", command=generate)
generate_btn.grid(row=12, column=0, padx=10, pady=10)

result_var = tk.StringVar()
result_label = tk.Label(window, textvariable=result_var, wraplength=500)
result_label.grid(row=12, column=1, padx=10, pady=10)

window.mainloop()
