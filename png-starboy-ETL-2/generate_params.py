class Params:
    def __init__(self):
        pass

    def generate_params_ref_product(self, data):
        param = (data["Brand"], data["Subbrand"],
                 data["Type_PG"], data["Packsize"],
                 data["Size"], data["Pack_Count_PG"])
        return param

    def generate_params_country_id(self, data, type):
        param = (data["Country"], data["country_prd"],)
        return param

    def generate_params_fct_mkt_mth(self, data, country_id, prd_id):
        param = (data["Date"], prd_id[0], country_id[0],
                 data["Channel"], data["Region"], data["ACV"],
                 data["Avg Price"], data["Value Sales"],
                 data["Value Share %"], data["Vol SPPD"],
                 data["Volume Share %"], data["Volume MSU"])
        return param

    def generate_params_fct_mkt_mth_japan(self, data, country_id, prd_id):
        param = (data["Date"], prd_id[0], country_id[0],
                 data["Channel"], data["Region"], data["Acv"],
                 data["Avg_price"], data["Value_sales"],
                 data["Volume_share"], data["Volume_sppd"],
                 data["Tdp"], data["Volume_msu"])
        return param

    def generate_params_analysis(self, data):
        param = (data["Country"], data["Segment"],
                 data["Date"], data["Fact"], data["Value"])
        return param

    def generate_params_prd_media(self, data):
        params = (data["Product"],)
        return params

    def generate_params_fct_media(self, data, country_id, prd_id):
        params = (prd_id[0], country_id[0], data["Date"], data["insertion"],
                  data["insert_twenty_five_plus"],
                  data["insert_sixteen_to_twenty_four"],
                  data["grp"], data["grp_twenty_five_plus"],
                  data["grp_sixteen_to_twenty_four"],
                  data["grp_per_spot"], data["grp_per_spot_twenty_five_plus"],
                  data["grp_per_spot_sixteen_to_twenty_four"])
        return params

    def generate_params_fct_mkt_mth_penetration(self, data, country_id, prd_id):
        param = (data["Date"], prd_id[0], country_id[0],
                 data["Region"], data["Penetration"])
        return param
