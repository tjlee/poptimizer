"""Основные настраиваемые параметры"""
import logging
import pathlib

import pandas as pd


class POptimizerError(Exception):
    """Базовое исключение."""


# Конфигурация логгера
logging.basicConfig(level=logging.INFO)

# Количество колонок в распечатках без переноса на несколько страниц
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 90)
pd.set_option("display.width", None)

# Путь к директории с отчетам
REPORTS_PATH = pathlib.Path(__file__).parents[1] / "reports"

# Путь к MongoDB и dump с данными по дивидендам
MONGO_PATH = pathlib.Path(__file__).parents[1] / "db"
MONGO_DUMP = pathlib.Path(__file__).parents[1] / "dump"

# Множитель, для переходя к после налоговым значениям
AFTER_TAX = 1 - 0.13

# Параметр для доверительных интервалов
T_SCORE = 2.0

# База дивидендов содержит данные с начала 2010 года
# Постепенно срок будет сдвигаться к началу режима TQBR для корректного учета сдвига T+2
STATS_START = pd.Timestamp("2010-08-01")

# Максимальный объем одной торговой операции в долях портфеля
MAX_TRADE = 1 / 100

# Параметры ML-модели
ML_PARAMS = {
    "data": (
        ("Label", {"days": 341, "div_share": 0.6, "on_off": True}),
        ("Scaler", {"days": 215, "on_off": True}),
        ("Ticker", {"on_off": True}),
        ("Mom12m", {"days": 264, "on_off": True, "periods": 6}),
        ("DivYield", {"days": 256, "on_off": True, "periods": 1}),
        ("Mom1m", {"days": 24, "on_off": False}),
        ("RetMax", {"days": 46, "on_off": True}),
        ("ChMom6m", {"days": 105, "on_off": True}),
        ("STD", {"days": 31, "on_off": True}),
        ("DayOfYear", {"on_off": False}),
        ("TurnOver", {"days": 217, "normalize": False, "on_off": True}),
        ("TurnOverVar", {"days": 273, "on_off": True}),
    ),
    "model": {
        "bagging_temperature": 0.7361215103910758,
        "depth": 9,
        "l2_leaf_reg": 1.8201584031440834,
        "learning_rate": 0.0029058892544552226,
        "one_hot_max_size": 1000,
        "random_strength": 2.286606195688752,
    },
}
