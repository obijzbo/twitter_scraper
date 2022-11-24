import mysql.connector as mysql
import pymysql
from sqlalchemy import create_engine
import pandas as pd
import json
import w3lib.html
from settings.config import DATABASE_NAME, DB_USER_NAME, DB_PASSWORD, DB_HOST_NAME, DB_TABLE_NAME, ROOT_PATH, DATA_PATH, INFO_PATH

class DB:
    def __init__(self):
        self.db_name = DATABASE_NAME
        self.user_name = DB_USER_NAME
        self.password = DB_PASSWORD
        self.host_name = DB_HOST_NAME
        self.table_name = DB_TABLE_NAME
        self.column_names = []
        self.df = pd.DataFrame()
        self.run()


    def run(self):
        self.connect_db()
        self.create_df()
        self.add_column()
        self.process_df()
        self.save_to_db()


    def connect_db(self):
        self.mydb = mysql.connect(db=self.db_name, user=self.user_name,
                                  password=self.password, host=self.host_name)
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name} (company_name LONGTEXT);""")
        self.engine = create_engine(f"mysql+pymysql://{self.user_name}:{self.password}@{self.host_name}/{self.db_name}")


    def create_df(self):
        file_name = f"{ROOT_PATH}/{DATA_PATH}/{INFO_PATH}/data.json"
        with open(file_name, 'r') as file:
            data = json.load(file)

        self.df = pd.DataFrame.from_dict(data)
        self.df.drop_duplicates()


    def add_column(self):
        self.column_names = list(self.df.columns)
        self.column_names = sorted(self.column_names)
        for column in self.column_names:
            sql_statement = f"""alter table {self.table_name}
                            add column {column} LONGTEXT;"""
            try:
                self.mycursor.execute(sql_statement)
            except Exception as e:
                print(e)

    def process_df(self):
        for column in self.column_names:
            for i in self.df[column]:
                text = self.clean_text(i)
                self.df[column] = self.df[column].replace([i], text)


    def clean_text(self, text):
        text = w3lib.html.remove_tags(text)
        text = w3lib.html.replace_escape_chars(text, ('\n', '\t', '\r'), " ")
        return text


    def save_to_db(self):
        sql_statement = f"drop table if exists {self.table_name}"
        self.mycursor.execute(sql_statement)
        self.df.to_sql(self.table_name, con=self.engine, index=False, schema=self.db_name, if_exists='append', chunksize=500)