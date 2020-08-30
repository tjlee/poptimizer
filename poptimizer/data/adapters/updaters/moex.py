"""Загрузка данных с MOEX."""
import datetime

import apimoex
import pandas as pd

from poptimizer.data.adapters.updaters import connection, logger
from poptimizer.data.ports import base, names, outer


class SecuritiesUpdater(logger.LoggerMixin, outer.AbstractUpdater):
    """Информация о всех торгующихся акциях."""

    def __call__(self, table_name: base.TableName) -> pd.DataFrame:
        """Получение дивидендов для заданного тикера."""
        name = self._log_and_validate_group(table_name, base.SECURITIES)
        if name != base.SECURITIES:
            raise base.DataError(f"Некорректное имя таблицы для обновления {table_name}")

        columns = ("SECID", "REGNUMBER", "LOTSIZE")
        json = apimoex.get_board_securities(connection.get_http_session(), columns=columns)
        df = pd.DataFrame(json)
        df.columns = [names.TICKER, names.REG_NUMBER, names.LOT_SIZE]
        return df.set_index(names.TICKER)


class IndexUpdater(logger.LoggerMixin, outer.AbstractIncrementalUpdater):
    """Котировки индекса полной доходности с учетом российских налогов - MCFTRR."""

    def __call__(self, table_name: base.TableName, start_date: datetime.date) -> pd.DataFrame:
        """Получение дивидендов для заданного тикера."""
        name = self._log_and_validate_group(table_name, base.INDEX)
        if name != base.INDEX:
            raise base.DataError(f"Некорректное имя таблицы для обновления {table_name}")

        json = apimoex.get_board_history(
            session=connection.get_http_session(),
            start=str(start_date),
            security=base.INDEX,
            columns=("TRADEDATE", "CLOSE"),
            board="RTSI",
            market="index",
        )
        df = pd.DataFrame(json)
        df.columns = [names.DATE, names.CLOSE]
        df[names.DATE] = pd.to_datetime(df[names.DATE])
        return df.set_index(names.DATE)
