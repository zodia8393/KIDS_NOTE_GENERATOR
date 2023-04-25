import os
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer, TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments

def fine_tune_model(training_folder_path):
    model = T5ForConditionalGeneration.from_pretrained("google/t5-small")
    tokenizer = T5Tokenizer.from_pretrained("google/t5-small")

    def load_dataset(path):
        return TextDataset(
            tokenizer=tokenizer,
            file_path=path,
            block_size=128
        )

    train_dataset = load_dataset(os.path.join(training_folder_path, "train.txt"))
    val_dataset = load_dataset(os.path.join(training_folder_path, "val.txt"))

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

def generate_note(model, keywords, max_length=256):
    tokenizer = T5Tokenizer.from_pretrained("google/t5-small")

    prompt = "어린이 노트 생성:"
    for keyword, value in keywords.items():
        prompt += f" {keyword}: {value};"

    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output_ids = model.generate(input_ids, max_length=max_length, num_return_sequences=1)

    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

