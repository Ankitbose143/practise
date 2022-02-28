def test():
    from db import Database
    Db = Database()
    query = "Select * from FACT_MARKET_PERF_AGG_MTH where month_id= ?"
    params = ('201905')
    res = Db.select(query, params)
    print(res)


if __name__ == "__main__":
    test()
