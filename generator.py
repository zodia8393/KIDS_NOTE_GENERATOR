# generator.py
import os
import random
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer, TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
from datasets import Dataset

def split_files(folder_path, train_ratio=0.8):
    all_files = [file for file in os.listdir(folder_path) if file.endswith('.txt')]
    random.shuffle(all_files)

    num_train_files = int(len(all_files) * train_ratio)

    train_files = all_files[:num_train_files]
    val_files = all_files[num_train_files:]

    return train_files, val_files

def load_dataset(folder_path, file_list, tokenizer):
    texts = []
    for file in file_list:
        with open(os.path.join(folder_path, file), 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
            texts.append(text)

    dataset = Dataset.from_dict({"text": texts})
    tokenized_dataset = dataset.map(lambda example: tokenizer(example["text"], truncation=True, max_length=128), batched=True)

    return tokenized_dataset

def fine_tune_model(training_folder_path):
    model = T5ForConditionalGeneration.from_pretrained("t5-small")
    tokenizer = T5Tokenizer.from_pretrained("t5-small")

    train_files, val_files = split_files(training_folder_path)

    train_dataset = load_dataset(training_folder_path, train_files, tokenizer)
    val_dataset = load_dataset(training_folder_path, val_files, tokenizer)

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )

    training_args = TrainingArguments(
        output_dir="./output",
        overwrite_output_dir=True,
        num_train_epochs=1,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        eval_steps=400,
        save_steps=800,
        warmup_steps=500,
        prediction_loss_only=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )

    trainer.train()

    return model

def save_and_load_model(folder_path):
    model.save_pretrained(folder_path)
    loaded_model = T5ForConditionalGeneration.from_pretrained(folder_path)
    return loaded_model

def generate_note(model, keywords, max_length=256):
    tokenizer = T5Tokenizer.from_pretrained("t5-small")

    prompt = "어린이 노트 생성:"
    for keyword, value in keywords.items():
        prompt += f" {keyword}: {value};"

    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output_ids = model.generate(input_ids, max_length=max_length, num_return_sequences=1)

    return tokenizer.decode(output_ids[0], skip_special_tokens=True)
