import sqlite3, random, datetime

con = sqlite3.connect('base.db')
c = con.cursor()

c.execute('''
          SELECT count(name) FROM sqlite_master
          ''')
if c.fetchall()[0][0] == 0:
    c.execute('''
            CREATE TABLE IF NOT EXISTS 
            (userId INTEGER PRIMARY KEY, age INTEGER NOT NULL)
            ''')
    c.execute('''
            CREATE TABLE IF NOT EXISTS Items
            (itemId INTEGER PRIMARY KEY, price INTEGER NOT NULL)
            ''')
    c.execute('''
            CREATE TABLE IF NOT EXISTS Purchases
            (purchaseId INTEGER PRIMARY KEY, 
            userId INTEGER NOT NULL,
            itemId INTEGER NOT NULL,
            date DATETIME NOT NULL,
            FOREIGN KEY (userId) REFERENCES Customers(userId),
            FOREIGN KEY (itemId) REFERENCES Items(itemId))
            ''')
    con.commit()

# c.execute("insert into Purchases values (1,1,1)")

    customers = []
    for i in range(1, 501):
        customers.append((i, random.randint(18, 70)))
    items = []
    for i in range(1, 201):
        items.append((i, random.randint(5, 1000)))
    purchases = []
    for i in range(1, 1001):
        purchases.append((i, random.randint(1, 500), random.randint(1, 200), datetime.datetime(2019+random.randint(0,3), random.randint(1, 12), random.randint(1, 28), random.randint(0, 23), random.randint(0, 59), 0)))
    c.executemany("insert into Customers values (?, ?)", customers)
    c.executemany("insert into Items values (?, ?)", items)
    c.executemany("insert into Purchases values (?, ?, ?, ?)", purchases)
    con.commit()

# 1. Посчитать сумму, которую в среднем в месяц тратят пользователи в возрастном диапазоне от 18 до 25 лет включительно.
def avg_avg(age0, age1):
    c.execute('''
            SELECT avg(avgPrice) from
            (SELECT avg(i.price) as avgPrice
            FROM ((Purchases p
            INNER JOIN Items i on i.itemId =  p.itemId)
            INNER JOIN Customers c on c.userId = p.userId)
            WHERE c.age between ? and ?
            GROUP by STRFTIME('%Y-%m', p.date))     
            ''', [age0, age1])
    return c.fetchall()[0][0]
# 2. В каком месяце и на какую сумму фиксируется самая большая выручка от пользователей в возрастном диапазоне 35+
c.execute('''
		  SELECT SUM(i.price), STRFTIME('%m', p.date) 
          FROM ((Purchases p
		  INNER JOIN Items i on i.itemId =  p.itemId)
		  INNER JOIN Customers c on c.userId = p.userId)
          WHERE
          c.age >= 35
 		  GROUP by STRFTIME('%Y-%m', p.date)
		  ORDER by sum(i.price) DESC
		  LIMIT 1
          ''')
print(c.fetchall())
# 3. Топ-n товаров по выручке за 2020 год (их itemId)
def top_n(year, n):
    c.execute('''
            SELECT p.itemId
            FROM ((Purchases p
            INNER JOIN Items i on i.itemId =  p.itemId)
            INNER JOIN Customers c on c.userId = p.userId)
            WHERE
            STRFTIME('%Y', p.date) = ?
            GROUP by p.itemId
            ORDER by SUM(i.price) DESC
            LIMIT ?
            ''', [str(year), n])
    return(c.fetchall())
# c.execute('''
#         SELECT p.itemId
#         FROM ((Purchases p
#         INNER JOIN Items i on i.itemId =  p.itemId)
#         INNER JOIN Customers c on c.userId = p.userId)
#         WHERE
#         STRFTIME('%Y', p.date) = '2021'
#         GROUP by p.itemId
#         ORDER by sum(i.price) DESC
#         LIMIT 1
#         ''' )
# print(c.fetchall())


print(avg_avg(50, 60))
# 3. Топ-n товаров по выручке за 2020 год (их itemId)
print(top_n(2020, 3))
# 4. Какой товар внес наибольшую вклад в вурочку за последний год.
print(top_n(datetime.datetime.today().year-1, 1))
con.close()
