### Utility Functions
import pandas as pd
import sqlite3
from sqlite3 import Error

def create_connection(db_file, delete_db=False):
    import os
    if delete_db and os.path.exists(db_file):
        os.remove(db_file)

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = 1")
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql, drop_table_name=None):
    
    if drop_table_name: # You can optionally pass drop_table_name to drop the table. 
        try:
            c = conn.cursor()
            c.execute("""DROP TABLE IF EXISTS %s""" % (drop_table_name))
        except Error as e:
            print(e)
    
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        
def execute_sql_statement(sql_statement, conn):
    cur = conn.cursor()
    cur.execute(sql_statement)

    rows = cur.fetchall()

    return rows

def step1_create_region_table(data_filename, normalized_database_filename):
    # Inputs: Name of the data and normalized database filename
    # Output: None
    
    ### BEGIN SOLUTION
    createregiontable="""CREATE TABLE [Region]( 
    [RegionID] Integer not null primary key,
    [Region] Text not null
    );"""
    normalized_conn=create_connection(normalized_database_filename)
    create_table(normalized_conn,createregiontable)
    with open(data_filename, 'r') as file:
        region=[]
        for i, line in enumerate(file):
            if i == 0:
                continue
            headervalues = line.strip().split('\t')
            region.append(headervalues[4])
        Uniqueregion=[]
        for i in range(0,len(region)):
            if region[i] not in Uniqueregion:
                Uniqueregion.append(region[i])
        sortedregion=sorted(Uniqueregion)
    def insert_region(conn, values):
        sql = ''' INSERT INTO Region(Region)
                VALUES(?) '''
        cur = conn.cursor()
        cur.executemany(sql, values)
        conn.commit()
        return cur.lastrowid

    region_data = [(row,) for row in sortedregion]
    insert_region(normalized_conn, region_data)
    ### END SOLUTION

def step2_create_region_to_regionid_dictionary(normalized_database_filename):
    
    
    ### BEGIN SOLUTION
    normalized_conn=create_connection(normalized_database_filename)
    selectregion="SELECT RegionID,Region FROM Region"
    rows=execute_sql_statement(selectregion,normalized_conn)
    regiondict={}
    for row in rows:
        region_id = row[0]
        region_name = row[1]
        regiondict[region_name] = region_id
    return regiondict


    ### END SOLUTION


def step3_create_country_table(data_filename, normalized_database_filename):
    # Inputs: Name of the data and normalized database filename
    # Output: None
    
    ### BEGIN SOLUTION
    createcountry="""CREATE TABLE [Country](
  [CountryID] Integer not null Primary key,
  [Country] Text not null,
  [RegionID] Integer not null ,
  FOREIGN KEY ([RegionID]) REFERENCES [Region]([RegionID])
  );"""
    normalized_conn=create_connection(normalized_database_filename)
    create_table(normalized_conn,createcountry)
    with open(data_filename, 'r') as file:
        countrylist=[]
        for i, line in enumerate(file):
            if i == 0:
                continue
            headervalues = line.strip().split('\t')
            countrylist.append((headervalues[3],headervalues[4]))
        uniquelist=[]
        for i in countrylist:
            if i not in uniquelist:
                uniquelist.append(i)
        Updatedlist=[]
        regiondict=step2_create_region_to_regionid_dictionary(normalized_database_filename)
        for i in uniquelist:
            Updatedlist.append((i[0],regiondict[i[1]]))
        sortedcountrylist=sorted(Updatedlist)
    def insert_country(conn, values):
        sql = ''' INSERT INTO Country(Country,RegionID)
                VALUES(?,?) '''
        cur = conn.cursor()
        cur.executemany(sql, values)
        conn.commit()
        return cur.lastrowid
    country_data = [(row[0], row[1]) for row in sortedcountrylist]
    insert_country(normalized_conn, country_data)

                
    
    ### END SOLUTION


def step4_create_country_to_countryid_dictionary(normalized_database_filename):
    
    
    ### BEGIN SOLUTION
    normalized_conn=create_connection(normalized_database_filename)
    selectcountry="SELECT CountryID,Country FROM Country"
    rows=execute_sql_statement(selectcountry,normalized_conn)
    countrydict={}
    for row in rows:
        country_id = row[0]
        country_name = row[1]
        countrydict[country_name] = country_id
    return countrydict

    ### END SOLUTION
        
        
def step5_create_customer_table(data_filename, normalized_database_filename):

    ### BEGIN SOLUTION
    createcustomer="""CREATE TABLE[Customer](
                        [CustomerID] integer not null Primary Key,
                        [FirstName] Text not null,
                        [LastName] Text not null,
                        [Address] Text not null,
                        [City] Text not null,
                        [CountryID] integer not null,
                        FOREIGN KEY ([CountryID]) REFERENCES [Country]([CountryID])
   ); """
    normalized_conn=create_connection(normalized_database_filename)
    create_table(normalized_conn,createcustomer)
    with open(data_filename, 'r') as file:
        customerlist=[]
        for i, line in enumerate(file):
            if i == 0:
                continue
            headervalues = line.strip().split('\t')
            name=headervalues[0].split(" ")
            customerlist.append((name[0], " ".join(name[1:]), headervalues[1], headervalues[2], headervalues[3]))
        Updatedcustomerlist=[]
        countrydict=step4_create_country_to_countryid_dictionary(normalized_database_filename)
        for i in customerlist:
            Updatedcustomerlist.append((i[0],i[1],i[2],i[3],countrydict[i[4]]))
        sortedcustomerlist=sorted(Updatedcustomerlist)
    def insert_customer(conn, values):
            sql = ''' INSERT INTO Customer(FirstName,LastName,Address,City,CountryID)
                    VALUES(?,?,?,?,?) '''
            cur = conn.cursor()
            cur.executemany(sql, values)
            conn.commit()
            return cur.lastrowid
    customer_data = [(row[0], row[1], row[2], row[3], row[4]) for row in sortedcustomerlist]
    insert_customer(normalized_conn, customer_data)
    
        
        
    ### END SOLUTION


def step6_create_customer_to_customerid_dictionary(normalized_database_filename):
    
    
    ### BEGIN SOLUTION
    normalized_conn=create_connection(normalized_database_filename)
    selectcustomer="SELECT CustomerID,FirstName || ' ' || LastName As Name FROM Customer"
    rows=execute_sql_statement(selectcustomer,normalized_conn)
    customerdict={}
    for row in rows:
        customer_id = row[0]
        customer_name = row[1]
        customerdict[customer_name] = customer_id
    return customerdict
    ### END SOLUTION
        
def step7_create_productcategory_table(data_filename, normalized_database_filename):
    # Inputs: Name of the data and normalized database filename
    # Output: None

    
    ### BEGIN SOLUTION
    createproductcategory="""CREATE TABLE[ProductCategory](
  [ProductCategoryID] integer not null Primary Key,
  [ProductCategory] Text not null,
  [ProductCategoryDescription] Text not null
  );"""
    normalized_conn=create_connection(normalized_database_filename)
    create_table(normalized_conn,createproductcategory)
    with open(data_filename,'r') as file:
        productcategory=[]
        productdescription=[]
        for i,line in enumerate(file):
            if i==0:
                continue
            headervalues = line.strip().split('\t')
            productcategory=headervalues[6].split(";")
            productdescription=headervalues[7].split(";")
            productcategorydesc=list(zip(productcategory,productdescription))
        Uniqueproductcategorydesc=[]
        for ele in productcategorydesc:
            if ele not in Uniqueproductcategorydesc:
                Uniqueproductcategorydesc.append(ele)
        Sorteduniqueprocatdesc=sorted(Uniqueproductcategorydesc)
    def insert_productcategory(conn, values):
            sql = ''' INSERT INTO ProductCategory(ProductCategory,ProductcategoryDescription)
                    VALUES(?,?) '''
            cur = conn.cursor()
            cur.executemany(sql, values)
            conn.commit()
            return cur.lastrowid
    productcategory_data = [(row[0], row[1]) for row in Sorteduniqueprocatdesc ]
    insert_productcategory(normalized_conn, productcategory_data)


    ### END SOLUTION

def step8_create_productcategory_to_productcategoryid_dictionary(normalized_database_filename):
    
    
    ### BEGIN SOLUTION
    normalized_conn=create_connection(normalized_database_filename)
    selectproductcategory="SELECT ProductCategoryID,ProductCategory FROM ProductCategory"
    rows=execute_sql_statement(selectproductcategory,normalized_conn)
    productcategorydict={}
    for row in rows:
        productcategory_id = row[0]
        productcategory_name = row[1]
        productcategorydict[productcategory_name] = productcategory_id
    return productcategorydict
    ### END SOLUTION
        

def step9_create_product_table(data_filename, normalized_database_filename):
    # Inputs: Name of the data and normalized database filename
    # Output: None

    
    ### BEGIN SOLUTION
    createproduct="""CREATE TABLE [Product](
  [ProductID] integer not null Primary key,
  [ProductName] Text not null,
  [ProductUnitPrice] Real not null,
  [ProductCategoryID] integer not null,
  FOREIGN KEY ([ProductCategoryID]) REFERENCES [ProductCategory]([ProductCategoryID])
  );"""
    normalized_conn=create_connection(normalized_database_filename)
    create_table(normalized_conn,createproduct)
    with open('data.csv','r') as file:
        productname=[]
        productcategory=[]
        productunitprice=[]
        for i,line in enumerate(file):
            if i==0:
                continue
            if i==1:
                headervalues = line.strip().split('\t')
                productname=headervalues[5].split(";")
                productcategory=headervalues[6].split(";")
                productunitprice=headervalues[8].split(";")
                productdata=list(zip(productname,productunitprice,productcategory))
        Uniqueproducts=[]
        for ele in productdata:
            if ele not in Uniqueproducts:
                Uniqueproducts.append(ele)
        productcategorydict=step8_create_productcategory_to_productcategoryid_dictionary(normalized_database_filename)
        Updateproducts=[]
        for i in Uniqueproducts:
            Updateproducts.append((i[0],i[1],productcategorydict[i[2]]))
        sortedproductsdata=sorted(Updateproducts)
    def insert_products(conn, values):
            sql = ''' INSERT INTO Product(ProductName,ProductUnitPrice,ProductCategoryID)
                    VALUES(?,?,?) '''
            cur = conn.cursor()
            cur.executemany(sql, values)
            conn.commit()
            return cur.lastrowid
    product_data = [(row[0], row[1],row[2]) for row in sortedproductsdata ]
    insert_products(normalized_conn, product_data)
        
    
    ### END SOLUTION


def step10_create_product_to_productid_dictionary(normalized_database_filename):
    
    ### BEGIN SOLUTION
    normalized_conn=create_connection(normalized_database_filename)
    selectproduct="SELECT ProductID,ProductName FROM Product"
    rows=execute_sql_statement(selectproduct,normalized_conn)
    productdict={}
    for row in rows:
        product_id = row[0]
        product_name = row[1]
        productdict[product_name] = product_id
    return productdict
    ### END SOLUTION
        

def step11_create_orderdetail_table(data_filename, normalized_database_filename):
    # Inputs: Name of the data and normalized database filename
    # Output: None

    
    ### BEGIN SOLUTION
    import datetime

    createorderdetail="""CREATE TABLE [OrderDetail](
  [OrderID] integer not null Primary Key,
  [CustomerID] integer not null,
  [ProductID] integer not null,
  [OrderDate] integer not null,
  [QuantityOrdered] integer not null,
   FOREIGN KEY ([CustomerID]) REFERENCES [Customer]([CustomerID]),
   FOREIGN KEY ([ProductID]) REFERENCES [Product]([ProductID])
  );"""
    normalized_conn=create_connection(normalized_database_filename)
    create_table(normalized_conn,createorderdetail)
    with open('data.csv', 'r') as file:
        orderdetail = []
        for i, line in enumerate(file):
            if not line.strip() or i==0:
                continue
            headervalues = line.strip().split('\t')
            customername = headervalues[0]
            productname = headervalues[5].split(";")
            orderdate = headervalues[10].split(";")
            quantityordered = headervalues[9].split(";")
            zipped=list(zip(productname,orderdate,quantityordered))
            for x in zipped:
                orderdetail.append((customername,)+x[0:3])
        sortedorderdetail=orderdetail
        custdict= step6_create_customer_to_customerid_dictionary(normalized_database_filename)
        productdict= step10_create_product_to_productid_dictionary(normalized_database_filename)
        Updateorderdetail=[]
        for ele in sortedorderdetail:
            Updateorderdetail.append((custdict[ele[0]],productdict[ele[1]],datetime.datetime.strptime(ele[2], '%Y%m%d').strftime('%Y-%m-%d'),ele[3]))
    def insert_orderdetail(conn, values):
        sql = ''' INSERT INTO OrderDetail(CustomerID,ProductID,OrderDate,QuantityOrdered)
                VALUES(?,?,?,?) '''
        cur = conn.cursor()
        cur.executemany(sql, values)
        conn.commit()
        return cur.lastrowid
    orderdetail_data = [(row[0],row[1],row[2],row[3]) for row in Updateorderdetail ]
    insert_orderdetail(normalized_conn, orderdetail_data)
        
    
    ### END SOLUTION


def ex1(conn, CustomerName):
    
    # Simply, you are fetching all the rows for a given CustomerName. 
    # Write an SQL statement that SELECTs From the OrderDetail table and joins with the Customer and Product table.
    # Pull out the following columns. 
    # Name -- concatenation of FirstName and LastName
    # ProductName
    # OrderDate
    # ProductUnitPrice
    # QuantityOrdered
    # Total -- which is calculated from multiplying ProductUnitPrice with QuantityOrdered -- round to two decimal places
    # HINT: USE customer_to_customerid_dict to map customer name to customer id and then use where clause with CustomerID
    
    ### BEGIN SOLUTION

    Custname=step6_create_customer_to_customerid_dictionary('normalized.db')
    Customerid=Custname[CustomerName]
    sql_statement = """ SELECT Customer.FirstName || ' ' || Customer.LastName As Name,Product.ProductName,
    OrderDetail.OrderDate,Product.ProductUnitPrice,OrderDetail.QuantityOrdered,
    round(Product.ProductUnitPrice*OrderDetail.QuantityOrdered,2) As Total
                        FROM OrderDetail
                            INNER JOIN Product ON Product.ProductID=OrderDetail.ProductID
                            INNER JOIN Customer ON Customer.CustomerID=OrderDetail.CustomerID
                        WHERE Customer.CustomerID = '{}'
    
    """.format(Customerid)
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement

def ex2(conn, CustomerName):
    
    # Simply, you are summing the total for a given CustomerName. 
    # Write an SQL statement that SELECTs From the OrderDetail table and joins with the Customer and Product table.
    # Pull out the following columns. 
    # Name -- concatenation of FirstName and LastName
    # Total -- which is calculated from multiplying ProductUnitPrice with QuantityOrdered -- sum first and then round to two decimal places
    # HINT: USE customer_to_customerid_dict to map customer name to customer id and then use where clause with CustomerID
    
    ### BEGIN SOLUTION
    Custname=step6_create_customer_to_customerid_dictionary('normalized.db')
    Customerid=Custname[CustomerName]
    sql_statement = """ SELECT Customer.FirstName || ' ' || Customer.LastName As Name,round(SUM(Product.ProductUnitPrice*OrderDetail.QuantityOrdered),2) As Total
                        FROM OrderDetail
                            INNER JOIN Product ON Product.ProductID=OrderDetail.ProductID
                            INNER JOIN Customer ON Customer.CustomerID=OrderDetail.CustomerID
                        WHERE Customer.CustomerID = '{}'
    
    """.format(Customerid)
    
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement

def ex3(conn):
    
    # Simply, find the total for all the customers
    # Write an SQL statement that SELECTs From the OrderDetail table and joins with the Customer and Product table.
    # Pull out the following columns. 
    # Name -- concatenation of FirstName and LastName
    # Total -- which is calculated from multiplying ProductUnitPrice with QuantityOrdered -- sum first and then round to two decimal places
    # ORDER BY Total Descending 
    ### BEGIN SOLUTION
    sql_statement = """ SELECT Customer.FirstName || ' ' || Customer.LastName As Name,round(SUM(Product.ProductUnitPrice*OrderDetail.QuantityOrdered),2) As Total
                        FROM OrderDetail
                            INNER JOIN Product ON Product.ProductID=OrderDetail.ProductID
                            INNER JOIN Customer ON Customer.CustomerID=OrderDetail.CustomerID
                        GROUP BY Name
                        ORDER BY Total DESC
                        
    
    """
    
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement

def ex4(conn):
    
    # Simply, find the total for all the region
    # Write an SQL statement that SELECTs From the OrderDetail table and joins with the Customer, Product, Country, and 
    # Region tables.
    # Pull out the following columns. 
    # Region
    # Total -- which is calculated from multiplying ProductUnitPrice with QuantityOrdered -- sum first and then round to two decimal places
    # ORDER BY Total Descending 
    ### BEGIN SOLUTION

    sql_statement = """ SELECT Region.Region,round(SUM(Product.ProductUnitPrice*OrderDetail.QuantityOrdered),2) As Total
                        FROM OrderDetail
                            INNER JOIN Country ON Country.CountryID=Customer.CountryID
                            INNER JOIN Region ON Region.RegionID= Country.RegionID
                            INNER JOIN Product ON Product.ProductID=OrderDetail.ProductID
                            INNER JOIN Customer ON Customer.CustomerID=OrderDetail.CustomerID
                        GROUP BY Region.Region
                        ORDER BY Total DESC
                        
    
    """
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement

def ex5(conn):
    
     # Simply, find the total for all the countries
    # Write an SQL statement that SELECTs From the OrderDetail table and joins with the Customer, Product, and Country table.
    # Pull out the following columns. 
    # Country
    # CountryTotal -- which is calculated from multiplying ProductUnitPrice with QuantityOrdered -- sum first and then round
    # ORDER BY Total Descending 
    ### BEGIN SOLUTION

    sql_statement = """ SELECT Country.Country,round(SUM(Product.ProductUnitPrice*OrderDetail.QuantityOrdered)) As CountryTotal
                        FROM OrderDetail
                            INNER JOIN Country ON Country.CountryID=Customer.CountryID
                            INNER JOIN Product ON Product.ProductID=OrderDetail.ProductID
                            INNER JOIN Customer ON Customer.CustomerID=OrderDetail.CustomerID
                            GROUP BY Country.Country
                            ORDER BY CountryTotal DESC
    """
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement


def ex6(conn):
    
    # Rank the countries within a region based on order total
    # Output Columns: Region, Country, CountryTotal, CountryRegionalRank
    # Hint: Round the the total
    # Hint: Sort ASC by Region
    ### BEGIN SOLUTION

    sql_statement ="""SELECT  Region,Country,CountryTotal,RANK() OVER (PARTITION BY Region ORDER BY CountryTotal DESC) AS CountryRegionalRank
                        FROM (SELECT Region.Region,Country.Country,ROUND(SUM(Product.ProductUnitPrice*OrderDetail.QuantityOrdered)) AS CountryTotal
                            FROM OrderDetail
                                INNER JOIN Customer ON Customer.CustomerID = OrderDetail.CustomerID
                                INNER JOIN Product ON Product.ProductID = OrderDetail.ProductID
                                INNER JOIN Country ON Country.CountryID = Customer.CountryID
                                INNER JOIN Region ON Region.RegionID = Country.RegionID
                            GROUP BY Region.Region,Country.Country
                            ) subquery
                        ORDER BY Region ASC,CountryTotal DESC"""
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement



def ex7(conn):
    
   # Rank the countries within a region based on order total, BUT only select the TOP country, meaning rank = 1!
    # Output Columns: Region, Country, CountryTotal, CountryRegionalRank
    # Hint: Round the the total
    # Hint: Sort ASC by Region
    # HINT: Use "WITH"
    ### BEGIN SOLUTION

    sql_statement = """WITH RegionalOrderTotals AS (
                            SELECT Region.Region,Country.Country,ROUND(SUM(Product.ProductUnitPrice*OrderDetail.QuantityOrdered)) AS CountryTotal,RANK() OVER (PARTITION BY Region.Region ORDER BY SUM(Product.ProductUnitPrice*OrderDetail.QuantityOrdered) DESC) AS CountryRegionalRank
                            FROM OrderDetail
                                INNER JOIN Customer ON Customer.CustomerID = OrderDetail.CustomerID
                                INNER JOIN Product ON Product.ProductID = OrderDetail.ProductID
                                INNER JOIN Country ON Country.CountryID = Customer.CountryID
                                INNER JOIN Region ON Region.RegionID = Country.RegionID
                            GROUP BY Region.Region,Country.Country
                        )
                        SELECT  Region,Country,CountryTotal,CountryRegionalRank
                        FROM RegionalOrderTotals
                        WHERE CountryRegionalRank = 1
                      """
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement

def ex8(conn):
    
    # Sum customer sales by Quarter and year
    # Output Columns: Quarter,Year,CustomerID,Total
    # HINT: Use "WITH"
    # Hint: Round the the total
    # HINT: YOU MUST CAST YEAR TO TYPE INTEGER!!!!
    ### BEGIN SOLUTION

    sql_statement = """WITH SalesByQuarter AS (
                        SELECT Customer.CustomerID,CAST(strftime('%m', OrderDetail.OrderDate) AS INTEGER) AS Month,CAST(strftime('%Y', OrderDetail.OrderDate) AS INTEGER) AS Year,
                        CASE 
                            WHEN CAST(strftime('%m', OrderDetail.OrderDate) AS INTEGER) IN (1, 2, 3) THEN 'Q1'
                            WHEN CAST(strftime('%m', OrderDetail.OrderDate) AS INTEGER) IN (4, 5, 6) THEN 'Q2'
                            WHEN CAST(strftime('%m', OrderDetail.OrderDate) AS INTEGER) IN (7, 8, 9) THEN 'Q3'
                            WHEN CAST(strftime('%m', OrderDetail.OrderDate) AS INTEGER) IN (10, 11, 12) THEN 'Q4'
                        END AS Quarter,
                        ROUND(SUM(Product.ProductUnitPrice * OrderDetail.QuantityOrdered)) AS Total
                        FROM OrderDetail
                            INNER JOIN Customer ON Customer.CustomerID = OrderDetail.CustomerID
                            INNER JOIN Product ON Product.ProductID = OrderDetail.ProductID
                        GROUP BY Customer.CustomerID, Year,Quarter
                )

                SELECT Quarter,Year,CustomerID,SUM(Total) AS Total
                FROM SalesByQuarter
                GROUP BY Quarter, Year,CustomerID
                ORDER BY Year,Quarter;

                    """
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement

def ex9(conn):
    
    # Rank the customer sales by Quarter and year, but only select the top 5 customers!
    # Output Columns: Quarter, Year, CustomerID, Total
    # HINT: Use "WITH"
    # Hint: Round the the total
    # HINT: YOU MUST CAST YEAR TO TYPE INTEGER!!!!
    # HINT: You can have multiple CTE tables;
    # WITH table1 AS (), table2 AS ()
    ### BEGIN SOLUTION

    sql_statement = """WITH SalesByQuarter AS (
                                SELECT Customer.CustomerID,CAST(strftime('%m', OrderDetail.OrderDate) AS INTEGER) AS Month,CAST(strftime('%Y', OrderDetail.OrderDate) AS INTEGER) AS Year,
                                CASE 
                                    WHEN CAST(strftime('%m', OrderDetail.OrderDate) AS INTEGER) IN (1, 2, 3) THEN 'Q1'
                                    WHEN CAST(strftime('%m', OrderDetail.OrderDate) AS INTEGER) IN (4, 5, 6) THEN 'Q2'
                                    WHEN CAST(strftime('%m', OrderDetail.OrderDate) AS INTEGER) IN (7, 8, 9) THEN 'Q3'
                                    WHEN CAST(strftime('%m', OrderDetail.OrderDate) AS INTEGER) IN (10, 11, 12) THEN 'Q4'
                                END AS Quarter,
                                ROUND(SUM(Product.ProductUnitPrice * OrderDetail.QuantityOrdered)) AS Total
                                FROM OrderDetail
                                    INNER JOIN Customer ON Customer.CustomerID = OrderDetail.CustomerID
                                    INNER JOIN Product ON Product.ProductID = OrderDetail.ProductID
                                GROUP BY Customer.CustomerID,Year,Quarter
                    ),
                    RankedSalesByQuarter AS (
                            SELECT Quarter,Year,CustomerID,Total,RANK() OVER(PARTITION BY Quarter, Year ORDER BY Total DESC) AS CustomerRank
                            FROM SalesByQuarter
                            )
                        SELECT Quarter, Year, CustomerID, Total,CustomerRank
                        FROM RankedSalesByQuarter
                        WHERE CustomerRank <=5
                        ORDER BY Year, Quarter, CustomerRank;

                    """
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement

def ex10(conn):
    
    # Rank the monthly sales
    # Output Columns: Quarter, Year, CustomerID, Total
    # HINT: Use "WITH"
    # Hint: Round the the total
    ### BEGIN SOLUTION

    sql_statement = """
                        WITH SalesByMonth AS (
                            SELECT STRFTIME('%m', OrderDetail.OrderDate) AS MonthNumber,
                                CASE 
                                    WHEN STRFTIME('%m', OrderDetail.OrderDate) = '01' THEN 'January'
                                    WHEN STRFTIME('%m', OrderDetail.OrderDate) = '02' THEN 'February'
                                    WHEN STRFTIME('%m', OrderDetail.OrderDate) = '03' THEN 'March'
                                    WHEN STRFTIME('%m', OrderDetail.OrderDate) = '04' THEN 'April'
                                    WHEN STRFTIME('%m', OrderDetail.OrderDate) = '05' THEN 'May'
                                    WHEN STRFTIME('%m', OrderDetail.OrderDate) = '06' THEN 'June'
                                    WHEN STRFTIME('%m', OrderDetail.OrderDate) = '07' THEN 'July'
                                    WHEN STRFTIME('%m', OrderDetail.OrderDate) = '08' THEN 'August'
                                    WHEN STRFTIME('%m', OrderDetail.OrderDate) = '09' THEN 'September'
                                    WHEN STRFTIME('%m', OrderDetail.OrderDate) = '10' THEN 'October'
                                    WHEN STRFTIME('%m', OrderDetail.OrderDate) = '11' THEN 'November'
                                    WHEN STRFTIME('%m', OrderDetail.OrderDate) = '12' THEN 'December'
                                END AS Month,
                                SUM(ROUND(Product.ProductUnitPrice * OrderDetail.QuantityOrdered)) AS Total
                            FROM OrderDetail
                                INNER JOIN Product ON Product.ProductID = OrderDetail.ProductID
                            GROUP BY MonthNumber, Month
                            ), 
                            RankedSalesByMonth AS (
                                SELECT Month, Total, RANK() OVER (ORDER BY Total DESC) AS TotalRank
                                FROM SalesByMonth
                            )
                            SELECT  Month, Total, TotalRank
                            FROM RankedSalesByMonth
                            ORDER BY TotalRank
"""
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement

def ex11(conn):
    
    # Find the MaxDaysWithoutOrder for each customer 
    # Output Columns: 
    # CustomerID,
    # FirstName,
    # LastName,
    # Country,
    # OrderDate, 
    # PreviousOrderDate,
    # MaxDaysWithoutOrder
    # order by MaxDaysWithoutOrder desc
    # HINT: Use "WITH"; I created two CTE tables
    # HINT: Use Lag

    ### BEGIN SOLUTION

    sql_statement = """WITH CustomerOrderDates AS (
                                    SELECT OrderDetail.CustomerID,OrderDetail.OrderDate,LAG(OrderDetail.OrderDate) OVER (PARTITION BY OrderDetail.CustomerID ORDER BY OrderDetail.OrderDate) AS PreviousOrderDate
                                    FROM OrderDetail
                                    ),
                                    CustomerMaxDaysWithoutOrder AS (
                                    SELECT Customer.CustomerID,Customer.FirstName,Customer.LastName,Country.Country,CustomerOrderDates.OrderDate,CustomerOrderDates.PreviousOrderDate,MAX(julianday(CustomerOrderDates.OrderDate) - julianday(CustomerOrderDates.PreviousOrderDate)) AS MaxDaysWithoutOrder
                                    FROM Customer
                                    JOIN Country ON Customer.CountryID = Country.CountryID
                                    JOIN CustomerOrderDates ON Customer.CustomerID = CustomerOrderDates.CustomerID
                                    GROUP BY Customer.CustomerID
                                    )
                                SELECT CustomerID,FirstName,LastName,Country,OrderDate,PreviousOrderDate,MaxDaysWithoutOrder
                                FROM CustomerMaxDaysWithoutOrder
                                ORDER BY MaxDaysWithoutOrder DESC, CustomerID DESC;
                                    """
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement