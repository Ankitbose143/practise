import pandas as pd
df = pd.read_excel('C:\\Users\\ankit.bose\\Documents\\bk.xlsx', sheet_name = 'Sheet1')
# print(pd.pivot_table(df, values=df.Result, aggfunc='count', fill_value=0))
# print(pd.pivot_table(df, index=df.Date, columns=df.Result, values=df['Count'], aggfunc='count'))
# df['Count1'] = df.groupby([df.ser,df.Date])[df.Result].count()
# print(,df['Count2'],df.groupby(df.ser)[df['Count']].count())
df = pd.crosstab([df.ser,df.Date], [df.Result], values=df['Count'],aggfunc=['count','sum', 'mean'])
# print("====df",df)

# df = pd.crosstab([df.ser,df.Date], [df.Result], values=df['Result'],aggfunc='mean')
# df = pd.crosstab([df.ser,df.Date], df.Result, values=df['Count'],aggfunc='mean')
# print("=====df123",df)
print(df.fillna(0))
# print(pd.crosstab(df['Result'], rownames=['Result'], colnames=['Result', 'Count']))
# tr = pd.cross