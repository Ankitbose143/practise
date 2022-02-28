# import pyodbc
# # pyodbc.pooling = False


# class Database:
#     def __init__(self):

#         self.cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};\
#                                    Server=starboysqldbdev.4841a7c7c0dd.database.windows.net;\
#                                    Database=starboy;\
#                                    Trusted_Connection=no;\
#                                    UID=pgsqlmiadmin;\
#                                    PWD=K9[[f*XN.-^`bVS2;'
#                                    )
#         # self.cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};\
#         #                            Server=dataserver.gramener.com;\
#         #                            Database=starboy;\
#         #                            Trusted_Connection=no;\
#         #                            UID=starboy;\
#         #                            PWD=Just24373!;'
#         #                            )
#         self.cnxn.autocommit = True
#         self.cursor = self.cnxn.cursor()
#         # self.cursor.fast_executemany = False

#     def insert_many(self, query, params):
#         try:
#             self.cursor.executemany(query, params)
#             # self.cursor.commit()
#         except Exception as e:
#             print(query)
#             print(params)
#             print(e)

#     def select(self, query, params):
#         rows = []
#         try:
#             self.cursor.execute(query, params)
#             rows = self.cursor.fetchone()
#         except Exception as e:
#             print(query)
#             print(params)
#             print(e)
#         finally:
#             return rows

#     def close(self):
#         self.cursor.close()
#         self.cnxn.close()
