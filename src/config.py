class Config:
    # Параметры данных
    DATA_PATH = "D:/Steve/data/raw/reviews.csv"
    SAVE_MODEL_PATH = "D:/Steve/data/models/sentiment_model"
    MAX_LENGTH = 128
    BATCH_SIZE = 16
    EPOCHS = 60
    LEARNING_RATE = 10e-5
    TEST_SIZE = 0.2
    RANDOM_STATE = 42

    # Параметры модели
    MODEL_NAME = "cointegrated/rubert-tiny2"
    NUM_LABELS = 3  # негативный, нейтральный, позитивный
