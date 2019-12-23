from utils import SpiderTimeBased, pro


class DailyBasic(SpiderTimeBased):
    pickle_path = 'raw/daily_basic'
    pkl_prefix = 'daily_basic_'

    def fetch(date):
        df = pro.daily_basic(trade_date=date)
        return df

class DayTick(SpiderTimeBased):
    pickle_path = 'raw/day_tick'
    pkl_prefix = 'day_tick_'

    def fetch(date):
        df = pro.daily(trade_date=date)
        return df


class MoneyFlow(SpiderTimeBased):
    pickle_path = 'raw/money_flow'
    pkl_prefix = 'money_flow_'

    def fetch(date):
        df = pro.moneyflow(trade_date=date)
        return df

if __name__ == '__main__':
    DailyBasic.update()
    DayTick.update()
    MoneyFlow.update()
