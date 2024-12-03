import sqlite3
from typing import Optional, List
from datetime import date
from pathlib import Path


class Sales:
    def __init__(self, ID: int, amount: float, salesDate: str, region: str):
        self.ID = ID
        self.amount = amount
        self.salesDate = salesDate
        self.region = region


class Region:
    def __init__(self, code: str, name: str):
        self.code = code
        self.name = name


# -------------- Data Access (SQLite) --------------------------
class SQLiteDBAccess:
    SQLITEDBPATH = Path(__file__).parent.parent / 'p01_db'

    def __init__(self):
        self._sqlite_sales_db = 'sales_db.sqlite'
        self._dbpath_sqlite_sales_db = SQLiteDBAccess.SQLITEDBPATH / self._sqlite_sales_db

    def connect(self) -> sqlite3.Connection:
        '''Connect to the SQLite database and return the connection object.'''
        try:
            connection = sqlite3.connect(self._dbpath_sqlite_sales_db)
            return connection
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def retrieve_sales_by_date_region(self, sales_date: date, region_code: str) -> Optional[Sales]:
        '''Retrieve ID, amount, salesDate, and region field from Sales table for the records
        that have the given salesDate and region values.'''
        
        query = '''
            SELECT ID, amount, salesDate, region
            FROM Sales
            WHERE salesDate = ? AND region = ?
        '''
        
        connection = self.connect()
        if not connection:
            return None
        
        cursor = connection.cursor()
        try:
            cursor.execute(query, (sales_date, region_code))
            result = cursor.fetchone() 
            if result:
                return Sales(id=result[0], amount=result[1], sales_date=result[2], region=result[3])
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error retrieving sales data: {e}")
            return None
        finally:
            connection.close()

    def update_sales(self, sales: Sales) -> None:
        '''Update amount, salesDate, and region fields of Sales table for the record with the given ID value.'''
        
        query = '''
            UPDATE Sales
            SET amount = ?, salesDate = ?, region = ?
            WHERE ID = ?
        '''
        
        connection = self.connect()
        if not connection:
            return
        
        cursor = connection.cursor()
        try:
            cursor.execute(query, (sales.amount, sales.salesDate, sales.region, sales.ID))
            connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating sales data: {e}")
        finally:
            connection.close()

    def retrieve_regions(self) -> List[Region]:
        '''Retrieve region code and name from Region table.'''
        
        query = '''SELECT code, name FROM Region'''
        
        connection = self.connect()
        if not connection:
            return []
        
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            return [Region(code=row[0], name=row[1]) for row in rows]
        except sqlite3.Error as e:
            print(f"Error retrieving regions: {e}")
            return []
        finally:
            connection.close()
