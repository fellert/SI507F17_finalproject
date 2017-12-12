import psycopg2
import psycopg2.extras

# CONNECTS TO DATABASE CALLED FELLERT_SI507FINAL
conn = psycopg2.connect("dbname='FELLERT_SI507FINAL' user=''")
cur = conn.cursor()

# CREATES COMPANY, INFO, RATINGS, AND TARGETS TABLES
# THIS IS ONLY RUN ONCE - AT THE VERY BEGINNING, IF THERE IS NO CACHE
# THE COMPANY TABLE (MORE SPECIFICALLY THE NAME OF THE COMPANY) ACTS AS THE
# FOREIGN KEY, CONNECTING TO THE OTHER THREE TABLES
def create_tables():
    cur.execute("DROP TABLE IF EXISTS Targets")
    cur.execute("DROP TABLE IF EXISTS Info")
    cur.execute("DROP TABLE IF EXISTS Ratings")
    cur.execute("DROP TABLE IF EXISTS Company")
    commands = (
        """
        CREATE TABLE Company (
            ID SERIAL PRIMARY KEY,
            Name VARCHAR(128) UNIQUE
        )
        """,
        """
        CREATE TABLE Targets (
            ID SERIAL PRIMARY KEY,
            Stock_ID INTEGER REFERENCES Company(ID) ON DELETE CASCADE,
            Median DECIMAL(7,2),
            High DECIMAL(7,2),
            Low DECIMAL(7,2)
        )
        """,
        """
        CREATE TABLE Info (
            ID SERIAL PRIMARY KEY,
            Stock_ID INTEGER REFERENCES Company(ID) ON DELETE CASCADE,
            Price DECIMAL(7,2),
            Volume VARCHAR(32),
            Consensus VARCHAR(32),
            Dividend_yield VARCHAR(8)
        )
        """,
        """
        CREATE TABLE Ratings (
            ID SERIAL PRIMARY KEY,
            Stock_ID INTEGER REFERENCES Company(ID) ON DELETE CASCADE,
            Buy INTEGER,
            Outperform INTEGER,
            Hold INTEGER,
            Underperform INTEGER,
            Sell INTEGER,
            No_Opinion INTEGER
        )
        """
    )
    for command in commands:
        cur.execute(command)

# RUNS EVERY TIME THERE IS A NEW TICKER NOT IN THE CACHE
def insert_stock(stock):
    stock_name = stock.name
    price = float(stock.price)
    targets = stock.targets
    volume = stock.volume
    mean = stock.mean
    ratings = stock.ratings
    dividend = stock.dividend
    cur.execute("INSERT INTO Company (Name) VALUES (%s) RETURNING ID", (stock_name,))
    result = cur.fetchone()
    stock_id = result[0]
    cur.execute("INSERT INTO Info (stock_id,price,volume,consensus,dividend_yield) \
                 VALUES (%s,%s,"'%s'",%s,%s)", (stock_id,price,volume,mean,dividend))
    cur.execute("INSERT INTO Targets (stock_id, median, high, low) \
                 VALUES (%s,%s,%s,%s)", (stock_id,targets[0],targets[1],targets[2]))
    cur.execute("INSERT INTO Ratings (stock_id,buy,outperform,hold,underperform,sell,no_opinion) \
                 VALUES (%s,%s,%s,%s,%s,%s,%s)", (stock_id,
                                                  ratings["BUY"],
                                                  ratings["OUTPERFORM"],
                                                  ratings["HOLD"],
                                                  ratings["UNDERPERFORM"],
                                                  ratings["SELL"],
                                                  ratings["No Opinion"])
                )
    conn.commit()

# RUNS EVERY TIME THE TIMESTAMP HAS EXPIRED 
def update_stock(stock):
    price = float(stock.price)
    targets = stock.targets
    volume = stock.volume
    mean = stock.mean
    ratings = stock.ratings
    cur.execute("UPDATE Info SET price = %s, volume = %s, consensus = %s \
                 WHERE Info.stock_id = (SELECT Company.id from Company WHERE Company.name = %s)",
                (price,volume,mean,stock.name))
    cur.execute("UPDATE Targets SET median = %s, high = %s, low = %s \
                 WHERE Targets.stock_id = (SELECT Company.id from Company WHERE Company.name = %s)",
                 (targets[0],targets[1],targets[2],stock.name))
    cur.execute("UPDATE Ratings SET buy = %s, outperform = %s, hold = %s, \
                 underperform = %s, sell = %s, no_opinion = %s \
                 WHERE Ratings.stock_id = (SELECT Company.id from Company WHERE Company.name = %s)",
                 (ratings["BUY"],ratings["OUTPERFORM"],ratings["HOLD"],
                  ratings["UNDERPERFORM"],ratings["SELL"],ratings["No Opinion"],stock.name)
                )
    conn.commit()
