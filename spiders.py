from utils import SpiderTimeBased, SpiderStokeBased, pro


class DailyBasic(SpiderTimeBased):
    '''
    每日指标
    '''
    pickle_path = 'raw/daily_basic'
    pkl_prefix = 'daily_basic_'
    sql_table = 'daily_basic'
    sql_record_table = 'daily_basic_record'

    @staticmethod
    def fetch(val):
        df = pro.daily_basic(trade_date=val)
        return df


class DayTick(SpiderTimeBased):
    '''
    日线行情
    '''
    pickle_path = 'raw/day_tick'
    pkl_prefix = 'day_tick_'
    sql_table = 'day_tick'
    sql_record_table = 'day_tick_record'

    @staticmethod
    def fetch(val):
        df = pro.daily(trade_date=val)
        return df


class AdjFactor(SpiderTimeBased):
    '''
    复权因子
    '''
    pickle_path = 'raw/adj_factor'
    pkl_prefix = 'adj_factor_'
    sql_table = 'adj_factor'
    sql_record_table = 'adj_factor_record'

    @staticmethod
    def fetch(val):
        df = pro.adj_factor(trade_date=val)
        return df


class Suspend(SpiderTimeBased):
    '''
    停复牌信息
    '''
    pickle_path = 'raw/suspend'
    pkl_prefix = 'suspend_'
    sql_table = 'suspend'
    sql_record_table = 'suspend_record'

    @staticmethod
    def fetch(val):
        df = pro.suspend(suspend_date=val)
        return df


class MoneyFlow(SpiderTimeBased):
    '''
    个股资金流向
    '''
    pickle_path = 'raw/money_flow'
    pkl_prefix = 'money_flow_'
    sql_table = 'money_flow'
    sql_record_table = 'money_flow_record'

    @staticmethod
    def fetch(val):
        df = pro.moneyflow(trade_date=val)
        return df


class NameChange(SpiderStokeBased):
    pickle_path = 'raw/name_change'
    pkl_prefix = 'name_change_'
    update_limit = 500
    sql_table = 'sec_name_change'
    sql_record_table = 'sec_name_change_record'

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
    # DailyBasic.update_db()
    AdjFactor.update()
    AdjFactor.update_db()
