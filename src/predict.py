from typing import Dict, List, Union
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import re

class SentimentAnalyzer:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Основная модель
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "D:/Steve/data/models/sentiment_model"
        ).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained("D:/Steve/data/models/sentiment_model")

        # Паттерны для определения тональности
        self.positive_patterns = [
            re.compile(r'отличн\w+', re.I),
            re.compile(r'рекоменд\w+', re.I),
            re.compile(r'довол\w+', re.I)
        ]

        self.negative_patterns = [
            re.compile(r'ужасн\w+', re.I),
            re.compile(r'никогда не', re.I),
            re.compile(r'отвратительн\w+', re.I),
            re.compile(r'проблем\w+', re.I)
        ]

    def analyze_text(self, text: str) -> Dict[str, any]:
        # Проверка по паттернам
        if any(p.search(text) for p in self.negative_patterns):
            return {
                'label': 'negative',
                'confidence': 0.95,
                'scores': [0.95, 0.03, 0.02]
            }

        if any(p.search(text) for p in self.positive_patterns):
            return {
                'label': 'positive',
                'confidence': 0.95,
                'scores': [0.02, 0.03, 0.95]
            }

        # Анализ моделью
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        probs = torch.softmax(outputs.logits, dim=1)[0].cpu().numpy()
        label = ["negative", "neutral", "positive"][np.argmax(probs)]

        return {
            'label': label,
            'confidence': float(np.max(probs)),
            'scores': probs.tolist()
        }
