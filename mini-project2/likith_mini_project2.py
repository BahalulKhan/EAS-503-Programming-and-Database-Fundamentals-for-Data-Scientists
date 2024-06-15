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
    
    create_non_normalized    = create_connection(normalized_database_filename)
    cursor_non_normalized    = create_non_normalized.cursor()
    data                     = data_filename 
    create_region_table = """CREATE TABLE [REGION] (
    [RegionID] Integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    [Region] Text not null ); """
    insert_statement = """INSERT INTO REGION ([RegionID], [Region]) VALUES (?,?);"""
    
##############################################    

    with open(data, 'r') as f:
        rows = f.readlines()
    input = sorted(set(map(lambda row: row.split('\t')[4], rows[1:])))
    final = [(i+1, input[i]) for i in range(len(input))]

##############################################
    # with create_non_normalized:
    #     create_table(create_non_normalized, create_region_table)
    #     _ = [cursor_non_normalized.execute(insert_statement, ele) for ele in final]
    # ### END SOLUTION
    with create_non_normalized:
        create_table(create_non_normalized, create_region_table, "REGION")
        cursor_non_normalized.executemany("""INSERT INTO REGION ([RegionID], [Region]) VALUES (?,?);""",final)

def step2_create_region_to_regionid_dictionary(normalized_database_filename):
    
    
    ### BEGIN SOLUTION
    create_non_normalized    = create_connection(normalized_database_filename)
    cursor_non_normalized    = create_non_normalized.cursor()
    sql_statement = "Select RegionID,Region From Region"
    region_rows = execute_sql_statement(sql_statement, create_non_normalized)
    final_2 = {}
    for i in region_rows:
        final_2[i[1]] = i[0]
    return final_2
    ### END SOLUTION


def step3_create_country_table(data_filename, normalized_database_filename):
    # Inputs: Name of the data and normalized database filename
    # Output: None
    
    ### BEGIN SOLUTION
    create_non_normalized    = create_connection(normalized_database_filename)
    cursor_non_normalized    = create_non_normalized.cursor()
    data                     = data_filename 
    create_country_table = "CREATE TABLE COUNTRY ( [CountryID] Integer NOT NULL Primary Key, [Country] Text NOT NULL, [RegionID] Integer NOT NULL, FOREIGN KEY(RegionID) REFERENCES REGION(RegionID));"
    create_table(create_non_normalized,create_country_table, "COUNTRY")
    insert_statement = "INSERT INTO COUNTRY VALUES (?,?,?);"

############################################################################################  
    from collections import defaultdict
    with open(data, 'r') as f:
        rows = f.readlines()
        country_rows = defaultdict(list)
        country_rows = {ele.split('\t')[3]: ele.split('\t')[4] for ele in rows[1:]}
        region_rows = step2_create_region_to_regionid_dictionary(normalized_database_filename)
        final = [[ele+1, ele1, region_rows[ele2]] for ele, (ele1, ele2) in enumerate(sorted(country_rows.items())) if ele2 in region_rows.keys()]
    with create_non_normalized:
        cursor_non_normalized.executemany(insert_statement,final)
    ### END SOLUTION


def step4_create_country_to_countryid_dictionary(normalized_database_filename):
    
    
    ### BEGIN SOLUTION
    create_non_normalized    = create_connection(normalized_database_filename)
    cursor_non_normalized    = create_non_normalized.cursor()
    sql_statement = "Select CountryID,Country,RegionID From country"
    region_rows = execute_sql_statement(sql_statement, create_non_normalized)
    final_3 = {}
    for i in region_rows:
        final_3[i[1]] = i[0]
    return final_3
    pass

    ### END SOLUTION
        
        
def step5_create_customer_table(data_filename, normalized_database_filename):

    create_non_normalized    = create_connection(normalized_database_filename)
    cursor_non_normalized    = create_non_normalized.cursor()
    data                     = data_filename 
    create_customer_table = "CREATE TABLE customer ( [CustomerID] Integer NOT NULL Primary Key, [FirstName] Text NOT NULL, [LastName] Text, [Address] Text, [City] Text, [CountryID] Integer NOT NULL);"
    create_table(create_non_normalized,create_customer_table,"customer")
    insert_statement = "INSERT INTO customer VALUES (?,?,?,?,?,?);"

    from collections import defaultdict
    country_rows = defaultdict(list)
    country_rows = step4_create_country_to_countryid_dictionary('normalized.db')

    with open(data, 'r') as f:
        rows = f.readlines()
    lenght = len(rows)
    final = []
    CustomerID = 1
    final = [[CustomerID+i, *ele[1:]] for i, ele in enumerate(sorted([[CustomerID, *(ele[0].split(' ', 1)), ele[1], ele[2], country_rows.get(ele[3])] for CustomerID, ele in enumerate([line.strip().split('\t') for line in open(data)], 1)][1:], key=lambda ele1: (ele1[1], ele1[2])))]


    # with create_non_normalized:
    #     create_table(create_non_normalized,create_customer_table)
    #     _ = [cursor_non_normalized.execute(insert_statement, ele) for ele in final]

    with create_non_normalized:
        cursor_non_normalized.executemany(insert_statement,final)
    ### END SOLUTION


def step6_create_customer_to_customerid_dictionary(normalized_database_filename):
    
    
    ### BEGIN SOLUTION
    create_non_normalized = create_connection(normalized_database_filename)
    cursor_non_normalized    = create_non_normalized.cursor()
    sql_statement = "Select FirstName || ' ' || LastName AS fullname, CustomerID From customer"
    region_rows = execute_sql_statement(sql_statement, create_non_normalized)  
    final_4 = {}
    for ele in region_rows:
        final_4[ele[0]] = ele[1]
    return final_4
    pass

    ### END SOLUTION
        
def step7_create_productcategory_table(data_filename, normalized_database_filename):
    # Inputs: Name of the data and normalized database filename
    # Output: None

    
    ### BEGIN SOLUTION
    create_non_normalized    = create_connection(normalized_database_filename)
    cursor_non_normalized    = create_non_normalized.cursor()
    data                     = data_filename 
    create_productcategory_table = "CREATE TABLE ProductCategory ( [ProductCategoryID] Integer NOT NULL Primary Key, [ProductCategory] Text NOT NULL, [ProductCategoryDescription] Text NOT NULL);"
    create_table(create_non_normalized,create_productcategory_table,"ProductCategory")
    insert_statement = "INSERT INTO ProductCategory VALUES (?,?,?);"
    ProductCategoryID =1
    
    with open(data, 'r') as fn:
        lines = fn.readlines()
    lenght = len(lines)
    final ,  mid_op= [] , []
    final = [[ProductCategoryID + ele, *rest] for ele, (ProductCategoryID, *rest) in enumerate(sorted([[ProductCategoryID, ProductCategory, ProductCategoryDescription] for ele in range(1, lenght) for ProductCategory, ProductCategoryDescription in zip(lines[ele].split('\t')[6].split(';'), lines[ele].split('\t')[7].split(';')) if ProductCategory not in mid_op and not mid_op.append(ProductCategory)], key=lambda ele: ele[1]))]
    
    # with create_non_normalized:
    #     _ = [cursor_non_normalized.execute(insert_statement, ele) for ele in final]
    with create_non_normalized:
        cursor_non_normalized.executemany(insert_statement,final)
    pass
   
    ### END SOLUTION

def step8_create_productcategory_to_productcategoryid_dictionary(normalized_database_filename):
    
    
    ### BEGIN SOLUTION
    create_non_normalized = create_connection(normalized_database_filename)
    cursor_non_normalized    = create_non_normalized.cursor()
    sql_statement = "Select ProductCategory,ProductCategoryID from ProductCategory"
    region_rows = execute_sql_statement(sql_statement, create_non_normalized)  
    final_4 = {}
    for ele in region_rows:
        final_4[ele[0]] = ele[1]
    return final_4
    pass

    ### END SOLUTION
        

def step9_create_product_table(data_filename, normalized_database_filename):
    # Inputs: Name of the data and normalized database filename
    # Output: None

    
    ### BEGIN SOLUTION
    create_non_normalized    = create_connection(normalized_database_filename)
    cursor_non_normalized    = create_non_normalized.cursor()
    data                     = data_filename 
    create_product_table = "CREATE TABLE Product ([ProductID] Interger NOT NULL Primary key, [ProductName] Text NOT NULL, [ProductUnitPrice] Real NOT NULL, [ProductCategoryID] Integer NOT NULL, FOREIGN KEY(ProductCategoryID) REFERENCES ProductCategory(ProductCategoryID));"
    create_table(create_non_normalized,create_product_table,"Product")
    
    insert_statement = "INSERT INTO Product VALUES (?,?,?,?);"
    product_rows = step8_create_productcategory_to_productcategoryid_dictionary(normalized_database_filename)
    with open(data, 'r') as fn:
        lines = fn.readlines()
    lenght = len(lines)
    final ,  mid_op= [] , []
    ProductID = 1
    final = [[ProductID + i, *ele[1:]] for i, ele in enumerate(sorted([[ProductID, col1, str(round(float(col2), 2)), product_rows[col3]]for ele in lines[1:]for col1, col2, col3 in zip(ele.split('\t')[5].split(';'), ele.split('\t')[8].split(';'), ele.split('\t')[6].split(';'))if col3 in product_rows and col1 not in mid_op and not mid_op.append(col1)],key=lambda ele: ele[1]))]

    # with create_non_normalized:
    #     _ = [cursor_non_normalized.execute(insert_statement, ele) for ele in final]
    # pass
    with create_non_normalized:
        cursor_non_normalized.executemany(insert_statement,final)
    pass
   
    ### END SOLUTION


def step10_create_product_to_productid_dictionary(normalized_database_filename):
    
    ### BEGIN SOLUTION
    create_non_normalized = create_connection(normalized_database_filename)
    cursor_non_normalized    = create_non_normalized.cursor()
    sql_statement = "Select ProductName,ProductID from Product"
    region_rows = execute_sql_statement(sql_statement, create_non_normalized)  
    final_4 = {}
    for ele in region_rows:
        final_4[ele[0]] = ele[1]
    return final_4
    pass

    ### END SOLUTION
        

def step11_create_orderdetail_table(data_filename, normalized_database_filename):
    # Inputs: Name of the data and normalized database filename
    # Output: None

    
    ### BEGIN SOLUTION
    from datetime import datetime
    strptime = datetime.strptime

    create_non_normalized    = create_connection(normalized_database_filename)
    cursor_non_normalized    = create_non_normalized.cursor()
    data                     = data_filename 

    create_productcategory_table = "CREATE TABLE OrderDetail ([OrderID] Integer NOT NULL Primary Key, [CustomerID] Integer NOT NULL, [ProductID] Integer NOT NULL, [OrderDate] Integer NOT NULL, [QuantityOrdered] Integer NOT NULL);"
    create_table(create_non_normalized,create_productcategory_table,"OrderDetail")
    insert_statement = "INSERT INTO OrderDetail VALUES (?,?,?,?,?);"
    product_rows = step10_create_product_to_productid_dictionary(normalized_database_filename)
    customer_rows = step6_create_customer_to_customerid_dictionary(normalized_database_filename)

    with open(data,'r') as fn:
        lines = fn.readlines()
    OrderID = 1
    final = []
    for ele in range(1,len(lines)):
        rows = lines[ele].split('\t') 
        first_row,ProductID,QuantityOrdered,OrderDate  = rows[0],rows[5],rows[9], rows[10]
        final += [[OrderID, customer_rows[first_row], product_rows[ProductID_inner], strptime(OrderDate_inner.strip(), '%Y%m%d').strftime('%Y-%m-%d'), int(QuantityOrdered_inner)]
               for ProductID_inner, QuantityOrdered_inner, OrderDate_inner in zip(ProductID.split(';'), QuantityOrdered.split(';'), OrderDate.split(';'))
               if first_row in customer_rows and ProductID_inner in product_rows
               if QuantityOrdered_inner.isdigit() and datetime.strptime(OrderDate_inner.strip(), '%Y%m%d')]
 
    final = [[OrderID := i] + row[1:] for i, row in enumerate(final, 1)]

    with create_non_normalized:
        cursor_non_normalized.executemany(insert_statement,final)
    pass
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
    create_non_normalized = conn
    ex1 = step6_create_customer_to_customerid_dictionary('normalized.db')
    selection = [value for key, value in ex1.items() if key == CustomerName][0]
    sql_statement = """
                    SELECT cust.FirstName || " " || cust.LastName AS Name,
                        prod.ProductName,
                        ord.OrderDate,
                        prod.ProductUnitPrice,
                        ord.QuantityOrdered,
                        round(prod.ProductUnitPrice*ord.QuantityOrdered, 2) AS Total
                    FROM OrderDetail ord
                    JOIN Product prod ON ord.ProductID = prod.ProductID
                    JOIN Customer cust ON ord.CustomerID = cust.CustomerID
                    WHERE cust.CustomerID = '%s'
                    """ % selection
    df = pd.read_sql_query(sql_statement, create_non_normalized)
    return sql_statement
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
    ex2 = step6_create_customer_to_customerid_dictionary('normalized.db')
    selection = next(map(lambda x: x[1], filter(lambda x: x[0] == CustomerName, ex2.items())), None)
    sql_statement = """Select cust.FirstName || " " || cust.LastName as Name, round(sum(prod.ProductUnitPrice*ord.QuantityOrdered),2) as Total 
                    From OrderDetail ord 
                    JOIN Product prod ON ord.ProductID = prod.ProductID 
                    JOIN customer cust ON ord.CustomerID = cust.CustomerID 
                    where cust.CustomerID = '%s' 
                    GROUP BY Name;""" % selection  

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
    sql_statement = """Select cust.FirstName || " " || cust.LastName as Name,round(sum(prod.ProductUnitPrice*ord.QuantityOrdered),2) as Total 
                      from OrderDetail ord 
                      JOIN Product prod ON ord.ProductID = prod.ProductID 
                      JOIN customer cust ON ord.CustomerID = cust.CustomerID  
                      group by Name ORDER BY Total desc;
    """
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

    sql_statement = """Select reg.Region, round(sum(prod.ProductUnitPrice*ord.QuantityOrdered),2) as Total 
                    From OrderDetail ord 
                    JOIN Product prod ON ord.ProductID = prod.ProductID 
                    JOIN customer cust ON ord.CustomerID = cust.CustomerID 
                    JOIN Country con ON  cust.CountryID = con.CountryID 
                    JOIN Region reg ON reg.RegionID = con.RegionID 
                    GROUP BY Region ORDER BY Total desc;    
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

    sql_statement = """Select con.Country, round(sum(prod.ProductUnitPrice*ord.QuantityOrdered)) as CountryTotal 
                       from OrderDetail ord
                       JOIN Product prod ON ord.ProductID = prod.ProductID 
                       JOIN customer cust ON ord.CustomerID = cust.CustomerID  
                       JOIN Country con ON  cust.CountryID = con.CountryID 
                       JOIN Region reg ON reg.RegionID = con.RegionID 
                       GROUP BY Country ORDER BY CountryTotal desc;
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

    sql_statement = """Select reg.Region, con.Country, round(sum(prod.ProductUnitPrice*ord.QuantityOrdered)) as CountryTotal, ROW_NUMBER() OVER(PARTITION BY reg.Region order by sum(prod.ProductUnitPrice*ord.QuantityOrdered) desc) CountryRegionalRank 
                       from OrderDetail ord 
                       JOIN Product prod ON ord.ProductID = prod.ProductID 
                       JOIN customer cust ON ord.CustomerID = cust.CustomerID 
                       JOIN Country con ON  cust.CountryID = con.CountryID 
                       JOIN Region reg ON reg.RegionID = con.RegionID 
                       GROUP BY Country ORDER BY reg.Region asc, CountryTotal desc;     
    """
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

    sql_statement = """Select * From (Select reg.Region, con.Country, round(sum(prod.ProductUnitPrice*ord.QuantityOrdered)) as CountryTotal, ROW_NUMBER() OVER(PARTITION BY reg.Region order by sum(prod.ProductUnitPrice*ord.QuantityOrdered) desc) CountryRegionalRank 
                       from OrderDetail ord 
                       JOIN Product prod ON ord.ProductID = prod.ProductID 
                       JOIN customer cust ON ord.CustomerID = cust.CustomerID 
                       JOIN Country con ON  cust.CountryID = con.CountryID 
                       JOIN Region reg ON reg.RegionID = con.RegionID 
                       GROUP BY Country ORDER BY reg.Region asc, CountryTotal desc) 
                       where CountryRegionalRank = 1;    
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

    sql_statement = """SELECT 
    CASE 
        WHEN CAST(substr(OrderDate, 6, 2) AS INTEGER) BETWEEN 1 AND 3 THEN 'Q1'
        WHEN CAST(substr(OrderDate, 6, 2) AS INTEGER) BETWEEN 4 AND 6 THEN 'Q2'
        WHEN CAST(substr(OrderDate, 6, 2) AS INTEGER) BETWEEN 7 AND 9 THEN 'Q3'
        ELSE 'Q4'
    END AS Quarter,
    CAST(strftime('%Y', OrderDate) AS INTEGER) AS Year,
    Customer.CustomerID,
    ROUND(SUM(ProductUnitPrice*QuantityOrdered)) AS Total
FROM 
    OrderDetail
    JOIN Customer ON Customer.CustomerID = OrderDetail.CustomerID
    JOIN Product ON Product.ProductID = OrderDetail.ProductID
GROUP BY 
    Customer.CustomerID, 
    Year, 
    Quarter
ORDER BY 
    Year, 
    Quarter, 
    Customer.CustomerID;


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

    sql_statement = """WITH table1 AS (
    SELECT
        CASE 
            WHEN CAST(substr(ord.OrderDate, 6, 2) AS INTEGER) BETWEEN 1 AND 3 THEN 'Q1'
            WHEN CAST(substr(ord.OrderDate, 6, 2) AS INTEGER) BETWEEN 4 AND 6 THEN 'Q2'
            WHEN CAST(substr(ord.OrderDate, 6, 2) AS INTEGER) BETWEEN 7 AND 9 THEN 'Q3'
            WHEN CAST(substr(ord.OrderDate, 6, 2) AS INTEGER) BETWEEN 10 AND 12 THEN 'Q4'
        END AS Quarter, 
        CAST(substr(ord.OrderDate, 1, 4) AS INTEGER) AS Year, 
        cust.CustomerID, 
        ROUND(SUM(prod.ProductUnitPrice*ord.QuantityOrdered)) AS Total
    FROM 
        OrderDetail ord 
        JOIN customer cust ON cust.CustomerID = ord.CustomerID 
        JOIN Product prod ON prod.ProductID = ord.ProductID 
    GROUP BY 
        cust.CustomerID,
        Year,
        Quarter
    ORDER BY 
        Year,
        Total DESC 
)
SELECT 
    * 
FROM 
    ( 
        SELECT 
            Quarter, 
            Year, 
            CustomerID, 
            Total, 
            ROW_NUMBER() OVER(PARTITION BY Year, Quarter ORDER BY Year, Quarter ASC) AS CustomerRank 
        FROM 
            table1
    ) 
WHERE 
    CustomerRank BETWEEN 1 AND 5;  

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
    SELECT Month, Total, 
       ROW_NUMBER() OVER(ORDER BY Total DESC) TotalRank 
FROM (
    SELECT CASE substr(ord.OrderDate, 6, 2)
        WHEN '01' THEN 'January'
        WHEN '02' THEN 'February'
        WHEN '03' THEN 'March'
        WHEN '04' THEN 'April'
        WHEN '05' THEN 'May'
        WHEN '06' THEN 'June'
        WHEN '07' THEN 'July'
        WHEN '08' THEN 'August'
        WHEN '09' THEN 'September'
        WHEN '10' THEN 'October'
        WHEN '11' THEN 'November'
        WHEN '12' THEN 'December'
    END as Month, 
    SUM(ROUND(prod.ProductUnitPrice*ord.QuantityOrdered)) as Total 
    FROM OrderDetail ord 
    JOIN customer cust ON cust.CustomerID = ord.CustomerID 
    JOIN Product prod ON prod.ProductID = ord.ProductID
    GROUP BY Month
) subquery 
ORDER BY Total DESC;
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

    sql_statement = """
     
    """
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement

