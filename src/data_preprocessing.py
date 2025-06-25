import pandas as pd
from sklearn.model_selection import train_test_split
from config import Config
import torch


def load_data():
    """Загрузка и подготовка данных"""
    df = pd.read_csv(Config.DATA_PATH)
    # Предполагаем колонки: 'text' и 'sentiment' (0-негатив, 1-нейтрал, 2-позитив)
    texts = df['text'].values
    labels = df['sentiment'].values
    return train_test_split(
        texts, labels,
        test_size=Config.TEST_SIZE,
        random_state=Config.RANDOM_STATE
    )


class ReviewDataset(torch.utils.data.Dataset):
    """Кастомный Dataset для обработки текстов"""

    def __init__(self, texts, labels, tokenizer):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            max_length=Config.MAX_LENGTH,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(self.labels[idx], dtype=torch.long)
        }

    def __len__(self):
        return len(self.texts)


def create_data_loader(texts, labels, tokenizer, batch_size):
    """Создание DataLoader"""
    dataset = ReviewDataset(texts, labels, tokenizer)
    return torch.utils.data.DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True
    )
