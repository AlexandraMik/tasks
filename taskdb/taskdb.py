import sqlite3, random, datetime

con = sqlite3.connect('base.db')
c = con.cursor()

# c.execute('''
#           CREATE TABLE IF NOT EXISTS Customers
#           (userId INTEGER PRIMARY KEY, age INTEGER NOT NULL)
#           ''')
# c.execute('''
#           CREATE TABLE IF NOT EXISTS Items
#           (itemId INTEGER PRIMARY KEY, price INTEGER NOT NULL)
#           ''')
# c.execute('''
#           CREATE TABLE IF NOT EXISTS Purchases
#           (purchaseId INTEGER PRIMARY KEY, 
#           userId INTEGER NOT NULL,
#           itemId INTEGER NOT NULL,
#           date DATETIME NOT NULL,
#           FOREIGN KEY (userId) REFERENCES Customers(userId),
#           FOREIGN KEY (itemId) REFERENCES Items(itemId))
#           ''')
# con.commit()

# # c.execute("insert into Purchases values (1,1,1)")

# customers = []
# for i in range(1, 501):
#     customers.append((i, random.randint(18, 70)))
# items = []
# for i in range(1, 201):
#     items.append((i, random.randint(5, 1000)))
# purchases = []
# for i in range(1, 1001):
#     purchases.append((i, random.randint(1, 500), random.randint(1, 200), datetime.datetime(2019+random.randint(0,3), random.randint(1, 12), random.randint(1, 28), random.randint(0, 23), random.randint(0, 59), 0)))
# c.executemany("insert into Customers values (?, ?)", customers)
# c.executemany("insert into Items values (?, ?)", items)
# c.executemany("insert into Purchases values (?, ?, ?, ?)", purchases)
# con.commit().

# 1. Посчитать сумму, которую в среднем в месяц тратят пользователи в возрастном диапазоне от 18 до 25 лет включительно.
c.execute('''
          SELECT AVG(avgMonthPrice) FROM
		  (SELECT avg(i.price) AS avgMonthPrice
          FROM 
          Purchases p,
          Customers c, 
          Items i
          WHERE
          p.userId = c.userId and 
          p.itemId = i.itemId and
          c.age between 18 and 25
 		  GROUP by STRFTIME('%Y-%m', p.date))
          ''')
print(c.fetchall())
# 2. В каком месяце и на какую сумму фиксируется самая большая выручка от пользователей в возрастном диапазоне 35+
c.execute('''
          SELECT MAX(sumMonthPrice), m FROM
		  (SELECT SUM(i.price) AS sumMonthPrice, STRFTIME('%m', p.date) as m
          FROM 
          Purchases p,
          Customers c, 
          Items i
          WHERE
          p.userId = c.userId and 
          p.itemId = i.itemId and
          c.age >= 35
 		  GROUP by STRFTIME('%Y-%m', p.date))
          ''')
print(c.fetchall())
# 3. Топ-3 товаров по выручке за 2020 год (их itemId)
c.execute('''
          SELECT ItemId from(
		  SELECT SUM(i.price) AS sumPrice, p.itemId as ItemId
          FROM 
          Purchases p,
          Customers c, 
          Items i
          WHERE
          p.userId = c.userId and 
          p.itemId = i.itemId and
          STRFTIME('%Y', p.date) = '2020'
 		  GROUP by p.itemId
		  ORDER by sumPrice DESC
		  LIMIT 3)
          ''')
print(c.fetchall())
# 4. Какой товар внес наибольшую вклад в вурочку за последний год.
c.execute('''
          SELECT ItemId from(
		  SELECT SUM(i.price) AS sumPrice, p.itemId as ItemId
          FROM 
          Purchases p,
          Customers c, 
          Items i
          WHERE
          p.userId = c.userId and 
          p.itemId = i.itemId and
          STRFTIME('%Y', p.date) = '2022'
 		  GROUP by p.itemId
		  ORDER by sumPrice DESC
		  LIMIT 1)
          ''')
print(c.fetchall())
con.close()
