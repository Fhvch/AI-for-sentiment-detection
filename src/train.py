import torch
from torch.optim import AdamW
from transformers import get_linear_schedule_with_warmup, AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm
from model import get_model
from data_preprocessing import load_data, create_data_loader
from config import Config
from sklearn.metrics import classification_report

def train():
    # Инициализация
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME)
    model = get_model().to(device)

    # Загрузка данных
    train_texts, val_texts, train_labels, val_labels = load_data()
    train_loader = create_data_loader(train_texts, train_labels, tokenizer, Config.BATCH_SIZE)
    val_loader = create_data_loader(val_texts, val_labels, tokenizer, Config.BATCH_SIZE)

    # Оптимизатор и шедулер
    optimizer = AdamW(model.parameters(), lr=Config.LEARNING_RATE)
    total_steps = len(train_loader) * Config.EPOCHS
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0,
        num_training_steps=total_steps
    )

    # Обучение
    for epoch in range(Config.EPOCHS):
        model.train()
        progress_bar = tqdm(train_loader, desc=f"Epoch {epoch + 1}")
        for batch in progress_bar:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )

            loss = outputs.loss
            loss.backward()

            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()

            progress_bar.set_postfix({'loss': loss.item()})

        # Валидация
        model.eval()
        val_loss = 0
        correct = 0
        total = 0
        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['labels'].to(device)

                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )

                val_loss += outputs.loss.item()
                _, predicted = torch.max(outputs.logits, 1)
                correct += (predicted == labels).sum().item()
                total += labels.size(0)

        print(f"Validation Loss: {val_loss / len(val_loader):.4f}")
        print(f"Validation Accuracy: {correct / total:.4f}")

    # После валидации вывод в терминал
    preds = torch.argmax(outputs.logits, dim=1).cpu().numpy()
    print(classification_report(labels.cpu().numpy(), preds))

    # Сохранение модели
    model.save_pretrained(Config.SAVE_MODEL_PATH)
    tokenizer.save_pretrained(Config.SAVE_MODEL_PATH)


if __name__ == "__main__":
    train()
