import sqlite3
import datetime

class Database:
    def __init__(self,db):
        self.con=sqlite3.connect(db)
        self.cur=self.con.cursor()

        Sql='''
                CREATE TABLE IF NOT EXISTS Items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name VARCHAR(100),
            price DECIMAL(10, 2)
            );'''

        sql1='''CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_date DATE,
            total_amount DECIMAL(10, 2)
            );'''

        sql2='''CREATE TABLE IF NOT EXISTS Order_Items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INT,
            item_id INT,
            item_name VARCHAR(100),
            quantity INT,
            price DECIMAL(10,2),
            total DECIMAL(10,2)
        );'''

        sql3='''CREATE TABLE IF NOT EXISTS Payments (
            payment_id INTEGER PRIMARY KEY,
            order_id INT,
            payment_date DATE,
            payment_amount DECIMAL(10, 2),
            FOREIGN KEY (order_id) REFERENCES Orders(order_id)
        );'''
        self.cur.execute(Sql)
        self.cur.execute(sql1)
        self.cur.execute(sql2)
        self.cur.execute(sql3)

        self.con.commit()

    def insert_item(self,item_name,price):
            self.cur.execute('insert into Items values(NULL,?,?)',(item_name,price))
            self.con.commit()
    
    def get_item(self,id):
        self.cur.execute('select item_id,item_name,price  from items where item_id=?',(id,))
        result=self.cur.fetchall()
        #print(result)
        return result
    def get_items(self):
        self.cur.execute('select * from items')
        rows=self.cur.fetchall()
        #print(rows)
        return rows
        
    def insert_order_item(self,item_id,itemName,ItemPrice,ItemQuantity,subtotal):
        order_id=0
        self.cur.execute('insert into Order_Items VALUES(NULL,?,?,?,?,?,?) ',(order_id,item_id,itemName,ItemPrice,ItemQuantity,subtotal))
        self.con.commit()

    def get_ordered_items(self):
        self.cur.execute('select item_name,quantity,price,total from Order_items where order_id=0')
        rows=self.cur.fetchall()
        #print(rows)
        return rows

    def get_total(self):
        self.cur.execute('SELECT sum(total) as total from Order_Items WHERE order_id=0')
        gtotal=self.cur.fetchone()
        #print(gtotal)
        return gtotal
    
    def insert_order(self,total_amt):
        # Get the current date and time as a Python datetime object
        current_datetime = datetime.datetime.now()

        # Extract the date portion from the datetime object
        current_date = current_datetime.date()

        # Convert the date object to a string in 'YYYY-MM-DD' format
        date_str = current_date.strftime('%Y-%m-%d')

        

        # Insert the data into the database
        self.cur.execute('INSERT INTO orders VALUES (NULL, ?, ?)', (date_str, total_amt))

        # Commit the transaction
        self.con.commit()

        last_inserted_id=self.cur.lastrowid

        self.cur.execute('UPDATE Order_Items SET order_id=? WHERE order_id=0',(last_inserted_id,))
        self.con.commit()


        
        

        

#do=Database("Restaurent.db")
#do.insert_item("Idly",7.50)
#do.get_total()