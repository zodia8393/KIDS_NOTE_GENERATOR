import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import messagebox
import openai

# ChatGPT 모델과 연동을 위한 초기화
openai.api_key = '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'
model_name = 'gpt-3.5-turbo'

# GUI 창 생성
window = tk.Tk()
window.title("어린이노트 생성 프로그램")
window.geometry("800x600")

# 활동 카운터
activity_counter = 1

# 예시 초기화
examples = []

# GUI 요소 생성
topic_label = tk.Label(window, text="주제를 입력하세요:", font=("Arial", 14))
topic_label.pack(pady=10)

topic_entry = tk.Entry(window, width=50)
topic_entry.pack(pady=5)

activity_label = tk.Label(window, text="세부 활동을 입력하세요:", font=("Arial", 14))
activity_label.pack(pady=10)

activity_entries = []
activity_buttons = []

def add_activity():
    global activity_counter
    activity_entry = tkst.ScrolledText(window, height=5)
    activity_entry.pack(pady=5)
    activity_entries.append(activity_entry)
    
    activity_button_frame = tk.Frame(window)
    activity_button_frame.pack(pady=5)
    
    activity_button = tk.Button(activity_button_frame, text="수정", command=lambda: modify_activity(activity_button))
    activity_button.pack(side=tk.LEFT, padx=5)
    
    delete_button = tk.Button(activity_button_frame, text="삭제", command=lambda: delete_activity(activity_entry, activity_button_frame))
    delete_button.pack(side=tk.LEFT)
    
    activity_buttons.append(activity_button)
    
    activity_counter += 1

def modify_activity(button):
    index = activity_buttons.index(button)
    activity_entry = activity_entries[index]
    activity_text = activity_entry.get("1.0", "end-1c")
    modify_window = tk.Toplevel(window)
    
    modify_label = tk.Label(modify_window, text="활동 수정:", font=("Arial", 14))
    modify_label.pack(pady=10)
    
    modify_entry = tkst.ScrolledText(modify_window, height=5)
    modify_entry.insert("1.0", activity_text)
    modify_entry.pack(pady=5)
    
    save_button = tk.Button(modify_window, text="저장", command=lambda: save_modified_activity(index, modify_entry, modify_window))
    save_button.pack(pady=5)

def save_modified_activity(index, entry, window):
    activity_entry = activity_entries[index]
    activity_entry.delete("1.0", "end")
    activity_entry.insert("1.0", entry.get("1.0", "end-1c"))
    window.destroy()

def delete_activity(entry, button_frame):
    activity_entries.remove(entry)
    activity_buttons.pop(activity_buttons.index(button_frame.winfo_children()[0]))
    entry.destroy()
    button_frame.destroy()

add_activity_button = tk.Button(window, text="세부 활동 추가", command=add_activity)
add_activity_button.pack(pady=5)

result_label = tk.Label(window, text="어린이노트 결과:", font=("Arial", 14))
result_label.pack(pady=10)

result_text = tkst.ScrolledText(window, height=15, width=80)
result_text.pack(pady=10)

# 예시 추가 함수
def add_example():
    example_window = tk.Toplevel(window)
    example_window.title("어린이노트 예시 추가")
    example_window.geometry("400x300")
    
    example_label = tk.Label(example_window, text="예시를 입력하세요:", font=("Arial", 14))
    example_label.pack(pady=10)
    
    example_entry = tkst.ScrolledText(example_window, height=5)
    example_entry.pack(pady=5)
    
    save_example_button = tk.Button(example_window, text="예시 저장", command=lambda: save_example(example_entry, example_window))
    save_example_button.pack(pady=5)

def save_example(entry, window):
    example = entry.get("1.0", "end-1c")
    examples.append(example)
    messagebox.showinfo("예시 추가", "예시가 성공적으로 추가되었습니다.")
    window.destroy()

add_example_button = tk.Button(window, text="예시 추가", command=add_example)
add_example_button.pack(pady=5)

# 어린이노트 생성 함수
def generate_note():
    topic = topic_entry.get()
    activities = [activity.get("1.0", "end-1c") for activity in activity_entries]
    
    # 어린이노트 생성을 위한 입력 조합
    prompt = f"주제: {topic}\n\n세부 활동:\n"
    prompt += "\n".join([f"활동 {i}: {activity}" for i, activity in enumerate(activities, start=1)])
    
    # 예시를 포함하여 ChatGPT를 통해 어린이노트 생성
    messages = [
        {"role": "system", "content": "You are A kind day care art teacher who has a kind way of telling the child's parents what they have done today."},
        {"role": "user", "content": prompt}
    ]
    if examples:
        messages.append({"role": "user", "content": f"예시:\n{examples[0]}"})
    
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.75
    )
    
    generated_note = response.choices[0].message.content.strip()
    
    # 생성된 어린이노트를 결과 텍스트 상자에 표시
    result_text.delete("1.0", "end")
    result_text.insert("1.0", generated_note)

# 어린이노트 생성 버튼 생성
generate_button = tk.Button(window, text="어린이노트 생성", command=generate_note)
generate_button.pack(pady=10)

# 프로그램 실행
window.mainloop()
