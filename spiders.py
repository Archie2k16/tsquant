from utils import SpiderTimeBased, SpiderStockBased, pro


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


class LimitList(SpiderTimeBased):
    '''
    当日涨跌停统计
    '''
    pickle_path = 'raw/limit_list'
    pkl_prefix = 'limit_list_'
    sql_table = 'limit_list'
    sql_record_table = 'limit_list_record'

    @staticmethod
    def fetch(val):
        df = pro.limit_list(trade_date=val)
        return df


class NameChange(SpiderStockBased):
    pickle_path = 'raw/name_change'
    pkl_prefix = 'name_change_'
    update_limit = 500
    sql_table = 'sec_name_change'
    sql_record_table = 'sec_name_change_record'

    @staticmethod
    def fetch(val):
        df = pro.namechange(ts_code=val)
        return df


class FinanceAudit(SpiderStockBased):
    pickle_path = 'raw/finance_audit'
    pkl_prefix = 'finance_audit_'
    update_limit = 400

    @staticmethod
    def fetch(val):
        df = pro.fina_audit(ts_code=val)
        return df


if __name__ == '__main__':
    DailyBasic.update_fs()
    DailyBasic.update_db()

    DayTick.update_fs()
    DayTick.update_db()

    MoneyFlow.update_fs()
    MoneyFlow.update_db()

    AdjFactor.update_fs()
    AdjFactor.update_db()

    LimitList.update_fs()
    LimitList.update_db()

    Suspend.update_fs()
    Suspend.update_db()
