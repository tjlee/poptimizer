"""Конфигурация приложения."""
import datetime
from types import MappingProxyType
from typing import Final, Mapping

from poptimizer.data.adapters import db
from poptimizer.data.adapters.loaders import (
    conomy,
    cpi,
    dividends,
    dohod,
    moex,
    smart_lab,
    trading_dates,
)
from poptimizer.data.ports import app, base

TRADING_DATES = app.TableDescription(
    loader=trading_dates.TradingDatesLoader(),
    index_checks=app.IndexChecks.NO_CHECKS,
    validate=False,
)
CONOMY = app.TableDescription(
    loader=conomy.ConomyLoader(),
    index_checks=app.IndexChecks.ASCENDING,
    validate=False,
)
DOHOD = app.TableDescription(
    loader=dohod.DohodLoader(),
    index_checks=app.IndexChecks.ASCENDING,
    validate=False,
)
SMART_LAB = app.TableDescription(
    loader=smart_lab.SmartLabLoader(),
    index_checks=app.IndexChecks.NO_CHECKS,
    validate=False,
)
DIVIDENDS = app.TableDescription(
    loader=dividends.DividendsLoader(),
    index_checks=app.IndexChecks.UNIQUE_ASCENDING,
    validate=False,
)
CPI = app.TableDescription(
    loader=cpi.CPILoader(),
    index_checks=app.IndexChecks.UNIQUE_ASCENDING,
    validate=True,
)
SECURITIES = app.TableDescription(
    loader=moex.SecuritiesLoader(),
    index_checks=app.IndexChecks.UNIQUE_ASCENDING,
    validate=False,
)
INDEX = app.TableDescription(
    loader=moex.IndexLoader(),
    index_checks=app.IndexChecks.UNIQUE_ASCENDING,
    validate=True,
)

TABLES_REGISTRY: Mapping[base.GroupName, app.TableDescription] = MappingProxyType(
    {
        base.TRADING_DATES: TRADING_DATES,
        base.CONOMY: CONOMY,
        base.DOHOD: DOHOD,
        base.SMART_LAB: SMART_LAB,
        base.DIVIDENDS: DIVIDENDS,
        base.CPI: CPI,
        base.SECURITIES: SECURITIES,
        base.INDEX: INDEX,
    },
)
_START_YEAR = 2015
STATS_START: Final = datetime.date(_START_YEAR, 1, 1)
CONFIG = app.Config(db_session=db.MongoDBSession(), description_registry=TABLES_REGISTRY)


def get() -> app.Config:
    """Возвращает конфигурацию приложения."""
    return CONFIG
