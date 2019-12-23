from utils import SpiderTimeBased, SpiderStokeBased, pro


class DailyBasic(SpiderTimeBased):
    pickle_path = 'raw/daily_basic'
    pkl_prefix = 'daily_basic_'

    @staticmethod
    def fetch(val):
        df = pro.daily_basic(trade_date=val)
        return df


class DayTick(SpiderTimeBased):
    pickle_path = 'raw/day_tick'
    pkl_prefix = 'day_tick_'

    @staticmethod
    def fetch(val):
        df = pro.daily(trade_date=val)
        return df


class MoneyFlow(SpiderTimeBased):
    pickle_path = 'raw/money_flow'
    pkl_prefix = 'money_flow_'

    @staticmethod
    def fetch(val):
        df = pro.moneyflow(trade_date=val)
        return df


class NameChange(SpiderStokeBased):
    pickle_path = 'raw/name_change'
    pkl_prefix = 'name_change_'
    update_limit = 500

    @staticmethod
    def fetch(val):
        df = pro.namechange(ts_code=val)
        return df


class FinanceAudit(SpiderStokeBased):
    pickle_path = 'raw/finance_audit'
    pkl_prefix = 'finance_audit_'
    update_limit = 400

    @staticmethod
    def fetch(val):
        df = pro.fina_audit(ts_code=val)
        return df


if __name__ == '__main__':
    # DailyBasic.update()
    # DayTick.update()
    # MoneyFlow.update()
    FinanceAudit.update()
