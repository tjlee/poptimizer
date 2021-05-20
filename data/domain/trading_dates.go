package domain

import (
	"context"
	"time"

	"github.com/WLM1ke/gomoex"
	"go.uber.org/zap"
)

// GroupTradingDates - группа таблицы с торговыми данными.
const GroupTradingDates = "trading_dates"

// TradingDates - таблица с диапазоном торговых дат.
type TradingDates struct {
	ID

	iss *gomoex.ISSClient

	Rows []gomoex.Date
}

// Update - полностью переписывает таблицу, если появились новые данные о торговых датах.
func (t TradingDates) Update(ctx context.Context) []Event {
	newRows, err := t.iss.MarketDates(ctx, gomoex.EngineStock, gomoex.MarketShares)

	switch {
	case err != nil:
		zap.L().Panic("Не удалось получить данные ISS", zap.Error(err))
	case len(newRows) != 1:
		zap.L().Panic("Ошибка валидации данных ISS", zap.Error(err))
	case t.Rows == nil, !newRows[0].Till.Equal(t.Rows[0].Till):
		return []Event{RowsReplaced{t.ID, newRows}}
	}

	return nil
}

// Информация о торгах публикуется на MOEX ISS в 0:45 по московскому времени на следующий день.
const (
	issTZ     = "Europe/Moscow"
	issHour   = 0
	issMinute = 45
)

func prepareZone(tz string) *time.Location {
	loc, err := time.LoadLocation(tz)
	if err != nil {
		zap.L().Panic("Не удалось загрузить часовой пояс", zap.Error(err))
	}

	return loc
}

func nextISSDailyUpdate(now time.Time, tz *time.Location) time.Time {
	now = now.In(tz)
	end := time.Date(now.Year(), now.Month(), now.Day(), issHour, issMinute, 0, 0, tz)

	if end.Before(now) {
		end = end.AddDate(0, 0, 1)
	}

	return end
}

// UpdateTradingDates - правило обновления данных о торговых датах.
//
// Требуется при запуске приложения и ежедневно после публикации данных на MOEX ISS.
// Так как компьютер может заснуть, что вызывает расхождение между монотонным и фактическим временем,
// то проверку публикации данных лучше проводить на регулярной основе, а не привязать к конкретному времени.
type UpdateTradingDates struct {
	iss *gomoex.ISSClient
	tz  *time.Location

	ticker <-chan time.Time
	stopFn func()
}

// NewUpdateTradingDates создает правило.
func NewUpdateTradingDates(iss *gomoex.ISSClient) *UpdateTradingDates {
	ticker := time.NewTicker(time.Hour)

	return &UpdateTradingDates{
		iss: iss,
		tz:  prepareZone(issTZ),

		ticker: ticker.C,
		stopFn: ticker.Stop,
	}
}

// Activate активирует правило.
// Не использует входящие события и посылает событие с обновлением таблицы торговых дат.
func (d *UpdateTradingDates) Activate(ctx context.Context, in <-chan Event, out chan<- Event) {
	defer d.stopFn()

	out <- UpdateRequired{&TradingDates{ID: NewID(GroupTradingDates, GroupTradingDates), iss: d.iss}}

	now := time.Now()
	nextDataUpdate := nextISSDailyUpdate(now, d.tz)

	for {
		select {
		case <-in:
			continue
		case now = <-d.ticker:
			if now.After(nextDataUpdate) {
				out <- UpdateRequired{&TradingDates{ID: NewID(GroupTradingDates, GroupTradingDates), iss: d.iss}}

				nextDataUpdate = nextISSDailyUpdate(now, d.tz)
			}
		case <-ctx.Done():
			return
		}
	}
}
