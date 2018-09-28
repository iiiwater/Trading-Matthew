# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 21:43:44 2018

@author: CHAO DU
"""

import quandl
import pandas as pd
import datetime
import zipfile
import os
import numpy as np
import csv
import sqlite3
from sqlite3 import Error

os.chdir("C:\\Users\\CHAO DU\\Desktop\\python\\Trading-Matthew-master")
quandl.ApiConfig.api_key="ZKWjVGUk-dp4sWoz5buP"
MSFT_data = quandl.get("EOD/MSFT", start_date="2018-07-23", end_date="2018-08-10")
#data.iloc[0:5,4:6]

class StockPrice:
    def __init__(self):
        #original csv
        self.stock_list = []
        #names
        #self.full_list = []
        #current date for unzip the file and read csv
        self.current_date = '20180811'
        #last close date
        self.close_date = '20180810'
        self.stock_mat = []    

#    def get_list_names(self):
#        # get the names of the stock data
#        df = pd.read_csv('ticker_list.csv')
#        stock_name_list = df['Ticker']
#        for i in stock_name_list:
#            self.full_list.append('EOD/'+i.replace('.','_')+'.4')
        
    def get_stock_prices(self):
        # read csv for data
        self.stock_list = pd.read_csv('EOD_20180913.csv')
        self.stock_list.columns = [u'Name', u'Date', u'Open', u'High', u'Low', u'Close',u'Volume',u'Dividend',u'Split',u'Adj_Open',u'Adj_High',u'Adj_Low',u'Adj_Close',u'Adj_Volume']

        
    def get_stock_matrix(self):
        #align trading date
        #close price only

        self.stock_mat = self.stock_list.pivot(index=u'Date',columns=u'Name',values=u'Close')
               
    def update_data_csv(self):
        #download data, extract zip file
        quandl.bulkdownload("EOD")        
        now = datetime.datetime.now()
        self.current_date = now.strftime("%Y%m%d")
        zip_ref = zipfile.ZipFile('EOD.zip', 'r')
        zip_ref.extractall()
        zip_ref.close()
        
        #update close date
        temp = quandl.get("EOD/MSFT", start_date=self.days_ago(10))
        self.close_date = str(temp.index.values[-1])[:10]

    def days_ago(self, d):
        #today is August 13, 10 days ago means August 3
        date = datetime.datetime.today() - datetime.timedelta(days=d)
        return date.strftime("%Y-%m-%d")
        
        
class InitialPortfolio:
    def __init__(self, asset_value, stocks):
        self.asset_value = asset_value
        self.stocks = stocks
        self.stock_mat = self.stocks.stock_mat
        self.stocks_liq = None
        self.stocks_liq_mat = None
        self.top5 = None
        self.top5_price = None
        self.current_holding=[0,0,0,0,0]
        self.current_date = '2018-08-11'
        self.close_date = '2018-08-10'
        self.start_date = datetime.date(2017,8,25)
        self.current_port = None
        self.database = "pythonsqlite.db"
        self.sql_create_assets_table = """ CREATE TABLE IF NOT EXISTS assets (
                                            id integer PRIMARY KEY,
                                            asset_value interger  NOT NULL,
                                            total_shares float NOT NULL,
                                            begin_date text,
                                            end_date text
                                        ); """
     
        self.sql_create_stocks_table = """CREATE TABLE IF NOT EXISTS stocks (
                                        id integer PRIMARY KEY,
                                        Stock_name text NOT NULL,
                                        price float NOT NULL,
                                        asset_id interger NOT NULL,
                                        shares float NOT NULL,
                                        begin_date text NOT NULL,
                                        end_date text NOT NULL,
                                        FOREIGN KEY (asset_id) REFERENCES assets (id)
                                    );"""
        self.conn=sqlite3.connect("pythonsqlite.db")

        
#    def get_initial_portfolio(self):
#        # Select the Initial Portfolio Based on the growth rate of last month
#        temp = self.stocks.stock_list.groupby(u'Name').tail(21)       
#        temp = temp[(temp[u'Date'] > self.days_ago(35))]
#        start_val = temp.groupby(u'Name').nth(0)[u'Close']
#        end_val = temp.groupby(u'Name').nth(19)[u'Close']
#        inc_val = (end_val - start_val) / start_val 
#        inc_val = inc_val.sort_values(ascending=False)
#        self.top5 = inc_val.head(5)
#        
#        for i in range(5):
#            self.top5_price.append(end_val[self.top5.index.values[i]])
#            
#        for i in range(5):
#            self.current_holding[i] = self.asset_value/5/self.top5_price[i]
    def get_initial_portfolio(self):
        stock_sym = self.stock_mat.columns#get columns from the pivot table
        startdate = self.start_date.strftime("%Y-%m-%d")
        earlier_date = self.days_ago(28, self.start_date)
        sub_mat = self.stock_mat.loc[earlier_date:startdate].values
        mon_grow = (sub_mat[-1,:] - sub_mat[0,:]) / sub_mat[0,:]
        rank = np.argsort(-mon_grow)
        return_list = []
        for i in range(5):
            col = rank[i]
            price = sub_mat[-1,col]
            return_list.append([stock_sym[col], price, mon_grow[col], self.asset_value/5/price])
        self.current_port = return_list

        self.my_df = pd.DataFrame(return_list,columns=['stock_name','price','monthly_growth','shares'])
        self.my_df.to_csv('current_holding.csv', index=False, header=False)
    

            #"create sqlite database"
                
    def create_table(self,create_table_Sql):
        try:
            self.c = self.conn.cursor()
            self.c.execute(create_table_Sql)
        except Error as e:
            print(e)
        
        
        
    def create_current_assets(self,asset):
    
        sql = ''' INSERT INTO assets(asset_value,total_shares,begin_date,end_date)
                  VALUES(?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, asset)
        return cur.lastrowid    
    
    def create_stock_select(self,stocks_select):
     
        sql = ''' INSERT INTO stocks(stock_name,price,asset_id,shares,begin_date,end_date)
                  VALUES(?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, stocks_select)
        return cur.lastrowid        
    
    def main(self):
     
        # create a database connection

        if self.conn is not None:
            # create projects table
            self.create_table( self.sql_create_assets_table)
            # create tasks table
            self.create_table( self.sql_create_stocks_table)
        else:
            print("Error! cannot create the database connection.")
     
        # create a database connection
        with self.conn:
    
            assets = (sum(self.my_df['price'][:5]*self.my_df['shares'][:5]),sum(self.my_df['shares'][:5]),self.days_ago(28, self.start_date),self.start_date);
            assets_id = self.create_current_assets(assets)
     
            # stocks
            for i in range(5):
                self.create_stock_select((self.my_df['stock_name'][i],self.my_df['price'][i],assets_id,self.my_df['shares'][i],self.days_ago(28, self.start_date),self.start_date))
            
                    
    def days_ago(self, d, startdate=None):
        #today is August 13, 10 days ago means August 3
        if startdate==None:
            date = datetime.datetime.today() - datetime.timedelta(days=d)
        else:
            date = startdate - datetime.timedelta(days=d)
        return date.strftime("%Y-%m-%d")
        
    def get_liquid(self):
        liquid_list = pd.read_csv('liquidtickers.csv').values.reshape([-1]).tolist()
        self.stocks_liq = self.stocks.stock_list.loc[self.stocks.stock_list['Name'].isin(liquid_list)]
        self.stocks_liq_mat = self.stocks_liq.pivot(index=u'Date',columns=u'Name',values=u'Close')

    def get_initial_liq_portfolio(self):
        stock_sym = self.stock_liq_mat.columns
        startdate = self.start_date.strftime("%Y-%m-%d")
        earlier_date = self.days_ago(28, self.start_date).strftime("%Y-%m-%d")
        sub_mat = self.stock_liq_mat.loc[earlier_date:startdate].values
        mon_grow = (sub_mat[-1,:] - sub_mat[0,:]) / sub_mat[0,:]
        rank = np.argsort(-mon_grow)
        return_list = []
        for i in range(5):
            col = rank[i]
            price = sub_mat[-1,col]
            return_list.append([stock_sym[col], price, mon_grow[col], self.asset_value/5/price])
        self.current_port = return_list

        my_df = pd.DataFrame(return_list)
        my_df.to_csv('current_holding.csv', index=False, header=False)
        

    
class ConsecDayTrading:
    def __init__(self,stocks):
        self.conn=sqlite3.connect("pythonsqlite.db")
        self.c=self.conn.cursor()
        self.last_holding = pd.read_sql_query("select * from stocks where asset_id=(select max(id) from assets);",self.conn)
        self.stocks = stocks
        self.stock_mat = self.stocks.stock_mat
        self.stocks_liq = None
        self.stocks_liq_mat = None
        
        self.current_date = datetime.date(2017,10,19)
        self.current_price = self.stock_mat.loc[self.current_date.strftime("%Y-%m-%d")]
        self.current_av = 0
        self.current_port = None

    
    def get_current_av(self):
        self.last_holding_names = [i for i in self.last_holding['Stock_name']]
        self.prices = self.current_price.loc[self.last_holding_names]
        self.current_av = (self.prices * self.last_holding.values[:,4]).sum()
        

    def get_liquid(self):
        
        liquid_list = pd.read_csv('liquidtickers.csv').values.reshape([-1]).tolist()
        self.stocks_liq = self.stocks.stock_list.loc[self.stocks.stock_list['Name'].isin(liquid_list)]
        self.stocks_liq_mat = self.stocks_liq.pivot(index=u'Date',columns=u'Name',values=u'Close')


    def days_ago(self, d, startdate=None):
        #today is August 13, 10 days ago means August 3
        if startdate==None:
            date = datetime.datetime.today() - datetime.timedelta(days=d)
        else:
            date = startdate - datetime.timedelta(days=d)
        return date.strftime("%Y-%m-%d")
        
    def get_current_portfolio(self):
        stock_sym = self.stock_mat.columns
        startdate = self.current_date.strftime("%Y-%m-%d")
        earlier_date = self.days_ago(28, self.current_date)
        sub_mat = self.stock_mat.loc[earlier_date:startdate].values
        mon_grow = (sub_mat[-1,:] - sub_mat[0,:]) / sub_mat[0,:]
        rank = np.argsort(-mon_grow)
        return_list = []
        for i in range(5):
            col = rank[i]
            price = sub_mat[-1,col]
            return_list.append([stock_sym[col], price, mon_grow[col], self.current_av/5/price])
        self.current_port = return_list

        self.my_df = pd.DataFrame(return_list,columns=['stock_name','price','monthly_growth','shares'])
        self.my_df.to_csv('current_holding.csv', index=False, header=False)

    def create_table(self,create_table_Sql):
        try:
            self.c = self.conn.cursor()
            self.c.execute(create_table_Sql)
        except Error as e:
            print(e)
        
        
        
    def create_current_assets(self,asset):
    
        sql = ''' INSERT INTO assets(asset_value,total_shares,begin_date,end_date)
                  VALUES(?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, asset)
        return cur.lastrowid    
    
    def create_stock_select(self,stocks_select):
     
        sql = ''' INSERT INTO stocks(stock_name,price,asset_id,shares,begin_date,end_date)
                  VALUES(?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, stocks_select)
        return cur.lastrowid        
    
    def main(self):
     

     
        # create a database connection
        with self.conn:
    
            assets = (sum(self.my_df['price'][:5]*self.my_df['shares'][:5]),sum(self.my_df['shares'][:5]),self.days_ago(28, self.current_date),self.current_date);
            assets_id = self.create_current_assets(assets)
     
            # stocks
            for i in range(5):
                self.create_stock_select((self.my_df['stock_name'][i],self.my_df['price'][i],assets_id,self.my_df['shares'][i],self.days_ago(28, self.current_date),self.current_date))
            

    def get_current_liq_portfolio(self):
        stock_sym = self.stock_liq_mat.columns
        startdate = self.current_date.strftime("%Y-%m-%d")
        earlier_date = self.days_ago(28, self.current_date).strftime("%Y-%m-%d")
        sub_mat = self.stock_liq_mat.loc[earlier_date:startdate].values
        mon_grow = (sub_mat[-1,:] - sub_mat[0,:]) / sub_mat[0,:]
        rank = np.argsort(-mon_grow)
        return_list = []
        for i in range(5):
            col = rank[i]
            price = sub_mat[-1,col]
            return_list.append([stock_sym[col], price, mon_grow[col], self.current_av/5/price])
        self.current_port = return_list

        my_df = pd.DataFrame(return_list)
        my_df.to_csv('current_holding.csv', index=False, header=False)


    







#check the database
conn=conn=sqlite3.connect('pythonsqlite.db')
c=conn.cursor()
assets=pd.read_sql_query('select * from assets;',conn)
stocks_lists=pd.read_sql_query('select * from stocks;',conn)

stocks = StockPrice()
stocks.update_data_csv()
stocks.get_stock_prices()
stocks.get_stock_matrix()



starting = InitialPortfolio(100000, stocks)
starting.get_initial_portfolio()
starting.get_liquid()
starting.main()


consecdtrading=ConsecDayTrading(stocks)
consecdtrading.get_current_av()
consecdtrading.get_current_portfolio()
consecdtrading.main()





#port = InitialPortfolio(100000)
#port.get_stock_prices()
#port.get_initial_portfolio()

#data = quandl.get(["EOD/MSFT.4", "EOD/AAPL.4"], start_date="2018-07-23", end_date="2018-08-10")

