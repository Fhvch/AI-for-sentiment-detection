from transformers import AutoModelForSequenceClassification
from config import Config

def get_model():
    """Инициализация предобученной модели"""
    return AutoModelForSequenceClassification.from_pretrained(
        Config.MODEL_NAME,
        num_labels=Config.NUM_LABELS
    )
