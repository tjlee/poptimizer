"""Стандартные представления информации для остальных пакетов программы."""
import pandas as pd

from poptimizer.data.core import ports
from poptimizer.data.core.app import config, requests


def last_history_date() -> pd.Timestamp:
    """Последняя доступная дата исторических котировок."""
    table_name = ports.TableName("trading_dates", "trading_dates")
    app_config = config.get()
    df = requests.get_table(table_name, app_config)
    return pd.Timestamp(df.loc[0, "till"])
