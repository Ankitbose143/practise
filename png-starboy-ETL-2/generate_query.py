class Query:
    def __init__(self):
        pass

    def generate_query_insert_country(self):
        query = "Insert into starboy.dbo.DIM_COUNTRY (country,country_prd) values (?,?)"
        return query

    def generate_query_rf_product(self):
        query = "Insert into starboy.dbo.REF_PRODUCT (brand, sub_brand,type_pg, pack_size,size, pack_count_pg) values(?, ?, ?, ?,?,?)"
        return query

    def generate_query_rf_product_koi(self):
        query = "Insert into starboy.dbo.REF_PRODUCT_BKP (brand, sub_brand,type_pg, pack_size,size, pack_count_pg) values(?, ?, ?, ?,?,?)"
        return query

    def generate_query_fact_market_perf_agg_mth(self):
        query = "Insert into starboy.dbo.FACT_MARKET_PERF_AGG_MTH (month_id, product_id,country_id,channel,region,acv,avg_price,value_sales,value_share,volume_sppd,volume_share,volume_msu) values (?,?,?,?,?,?,?,?,?,?,?,?)"
        return query

    def generate_query_fact_market_perf_agg_mth_japan(self):
        query = "Insert into starboy.dbo.FACT_MARKET_PERF_AGG_MTH (month_id, product_id,country_id,channel,region,acv,avg_price,value_sales,volume_share,volume_sppd,tdp,volume_msu) values (?,?,?,?,?,?,?,?,?,?,?,?)"
        return query

    def generate_query_fact_market_perf_agg_mth_japan_koi(self):
        query = "Insert into starboy.dbo.FACT_MARKET_PERF_AGG_MTH_BKP (month_id, product_id,country_id,channel,region,acv,avg_price,value_sales,volume_share,volume_sppd,tdp,volume_msu) values (?,?,?,?,?,?,?,?,?,?,?,?)"
        return query

    def generate_query_fact_market_perf_agg_wk_japan(self):
        query = "Insert into starboy.dbo.FACT_MARKET_PERF_AGG_WK (week_id, product_id,country_id,channel,region,acv,avg_price,value_sales,volume_share,volume_sppd,tdp,volume_msu) values (?,?,?,?,?,?,?,?,?,?,?,?)"
        return query

    def generate_query_fact_market_perf_agg_wk_japan_koi(self):
        query = "Insert into starboy.dbo.FACT_MARKET_PERF_AGG_WK_BKP (week_id, product_id,country_id,channel,region,acv,avg_price,value_sales,volume_share,volume_sppd,tdp,volume_msu) values (?,?,?,?,?,?,?,?,?,?,?,?)"
        return query

    def generate_query_fact_market_perf_agg_wk(self):
        query = "Insert into starboy.dbo.FACT_MARKET_PERF_AGG_WK (week_id,product_id,country_id,channel,region,acv,avg_price,value_sales,value_share,volume_sppd,volume_share,volume_msu) values (?,?,?,?,?,?,?,?,?,?,?,?)"
        return query

    def select_query_country_id(self):
        query = "Select country_id from starboy.dbo.DIM_COUNTRY where country= ? and country_prd= ?"
        return query

    def select_query_prd_id(self, params):
        query = 'Select product_id from starboy.dbo.REF_PRODUCT where brand {brand_search} and sub_brand {sub_brand_search} and type_pg {type_search} and pack_size {pack_size_search} and size {size_search} and pack_count_pg {pack_count_search}'
        query = self.format_query(query, params)
        return query

    def select_query_prd_id_koi(self, params):
        query = 'Select product_id from starboy.dbo.REF_PRODUCT_BKP where brand {brand_search} and sub_brand {sub_brand_search} and type_pg {type_search} and pack_size {pack_size_search} and size {size_search} and pack_count_pg {pack_count_search}'
        query = self.format_query(query, params)
        return query

    def insert_analyis_query(self):
        query = "Insert into FACT_ANALYSIS (country_id,segment,month_id,fact,value) values (?,?,?,?,?)"
        return query

    def format_query(self, query, params):
        query = query.format(
            brand_search="is null" if params[0] is None else "=?",
            sub_brand_search="is null" if params[1] is None else "=?",
            type_search="is null" if params[2] is None else "=?",
            pack_size_search="is null" if params[3] is None else "=?",
            size_search="is null" if params[4] is None else "=?",
            pack_count_search="is null" if params[5] is None else "=?"
        )
        return query

    def select_query_prd_media(self):
        query = "Select product_id from REF_PRODUCT_MEDIA where brand= ?"
        return query

    def insert_media_prd(self):
        query = "Insert into REF_PRODUCT_MEDIA (brand) values (?)"
        return query

    def insert_fact_media(self):
        query = "Insert into FACT_MEDIA (product_id,country_id,month_id,insertion,insert_twenty_five_plus,insert_sixteen_to_twenty_four,grp,grp_twenty_five_plus,grp_sixteen_to_twenty_four,grp_per_spot,grp_per_spot_twenty_five_plus,grp_per_spot_sixteen_to_twenty_four) values (?,?,?,?,?,?,?,?,?,?,?,?)"
        return query

    def generate_query_fact_penetration_japan(self):
        query = "Insert into FACT_MARKET_PEN_AGG_MTH (month_id,product_id,country_id,region,penetration) values (?,?,?,?,?)"
        return query
