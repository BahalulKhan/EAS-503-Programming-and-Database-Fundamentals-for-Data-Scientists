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
    conn_normalized    = create_connection(normalized_database_filename)
    cur_conn_normalized    = conn_normalized.cursor()
    create_region_table = """CREATE TABLE [REGION] ([RegionID] Integer NOT NULL PRIMARY KEY AUTOINCREMENT,[Region] Text not null ); """
    rows = open(data_filename).readlines()
    unique_region = []
    i = 1
    while i < len(rows):
        values = rows[i].strip().split('\t')
        region = values[4]
        if region not in unique_region:
            unique_region.append(region)
        i += 1
    unique_region.sort()
    Output = []
    i = 0
    while i < len(unique_region):
        Output.append([i+1, unique_region[i]])
        i += 1
    insert_statement = """INSERT INTO REGION ([RegionID], [Region]) VALUES (?,?);"""
    with conn_normalized:
        create_table(conn_normalized, create_region_table)
        cur_conn_normalized.executemany(insert_statement,Output)
    ### END SOLUTION

def step2_create_region_to_regionid_dictionary(normalized_database_filename):
    
    
    ### BEGIN SOLUTION
    conn_normalized    = create_connection(normalized_database_filename)
    select_statement = "Select RegionID,Region From Region"
    region_rows = execute_sql_statement(select_statement, conn_normalized)
    regionid_dictionary = {}
    i = 0
    while i < len(region_rows):
        regionid, region = region_rows[i]
        regionid_dictionary[region] = regionid
        i += 1
    return regionid_dictionary
    ### END SOLUTION


def step3_create_country_table(data_filename, normalized_database_filename):
    # Inputs: Name of the data and normalized database filename
    # Output: None
    
    ### BEGIN SOLUTION
    conn_normalized    = create_connection(normalized_database_filename)
    cur_conn_normalized    = conn_normalized.cursor()
    create_country_table = "CREATE TABLE COUNTRY ( [CountryID] Integer NOT NULL Primary Key, [Country] Text NOT NULL, [RegionID] Integer NOT NULL, FOREIGN KEY(RegionID) REFERENCES REGION(RegionID));"
    create_table(conn_normalized,create_country_table)
    with open(data_filename, 'r') as file:
        line = file.readlines()
        country_rows = {}
        count = 0
        while count < len(line)-1:
            row_value = line[count+1].split('\t')
            country = row_value[3]
            region = row_value[4].strip()
            country_rows[country] = region
            count += 1
        region_dict = step2_create_region_to_regionid_dictionary(normalized_database_filename)
        country_items = sorted(country_rows.items())
        Output = []
        count = 0
        i = 0
        while i < len(country_items):
            country, region = country_items[i]
            if region in region_dict.keys():
                region_id = region_dict[region]
                count += 1
                Output.append([count, country, region_id])
            i += 1
    insert_statement = "INSERT INTO COUNTRY VALUES (?,?,?);"
    with conn_normalized:
        cur_conn_normalized.executemany(insert_statement,Output)
    ### END SOLUTION


def step4_create_country_to_countryid_dictionary(normalized_database_filename):
    
    
    ### BEGIN SOLUTION
    conn_normalized    = create_connection(normalized_database_filename)
    select_statement = "Select CountryID,Country,RegionID From country"
    country_rows = execute_sql_statement(select_statement, conn_normalized)
    countryid_dictionary = {}
    while len(country_rows) > 0:
        row = country_rows.pop(0)
        countryid_dictionary[row[1]] = row[0]
    return countryid_dictionary
    ### END SOLUTION
        
        
def step5_create_customer_table(data_filename, normalized_database_filename):

    ### BEGIN SOLUTION
    conn_normalized    = create_connection(normalized_database_filename)
    cur_conn_normalized    = conn_normalized.cursor()
    create_customer_table = "CREATE TABLE customer ( [CustomerID] Integer NOT NULL Primary Key, [FirstName] Text NOT NULL, [LastName] Text, [Address] Text, [City] Text, [CountryID] Integer NOT NULL);"
    create_table(conn_normalized,create_customer_table)
    country_rows = {}
    keys = list(country_rows.keys())
    i = 0
    while i < len(keys):
        country_rows[keys[i]] = []
        i += 1
    country_rows = step4_create_country_to_countryid_dictionary('normalized.db')
    Output = []
    customer_id = 1
    data_lines = [line.strip().split('\t') for line in open(data_filename)]
    sorted_lines = sorted(data_lines[1:], key=lambda ele: (ele[0].split(' ', 1)[0], ele[0].split(' ', 1)[1]))
    i = 0
    while i < len(sorted_lines):
        line = sorted_lines[i]
        customer_list = line[0].split(' ', 1)
        customer_row = [customer_id + i, customer_list[0], customer_list[1], line[1], line[2], country_rows.get(line[3])]
        Output.append(customer_row)
        i += 1
    insert_statement = "INSERT INTO customer VALUES (?,?,?,?,?,?);"
    with conn_normalized:
        cur_conn_normalized.executemany(insert_statement,Output)
    ### END SOLUTION


def step6_create_customer_to_customerid_dictionary(normalized_database_filename):
    
    
    ### BEGIN SOLUTION
    conn_normalized    = create_connection(normalized_database_filename)
    select_statement = "Select FirstName || ' ' || LastName AS fullname, CustomerID From customer"
    customer_rows = execute_sql_statement(select_statement, conn_normalized)  
    customerid_dictionary = {}
    i = 0
    while i < len(customer_rows):
        ele = customer_rows[i]
        customerid_dictionary[ele[0]] = ele[1]
        i += 1
    return customerid_dictionary
    ### END SOLUTION
        
def step7_create_productcategory_table(data_filename, normalized_database_filename):
    # Inputs: Name of the data and normalized database filename
    # Output: None

    
    ### BEGIN SOLUTION
    conn_normalized    = create_connection(normalized_database_filename)
    cur_conn_normalized    = conn_normalized.cursor()
    create_productcategory_table = "CREATE TABLE ProductCategory ( [ProductCategoryID] Integer NOT NULL Primary Key, [ProductCategory] Text NOT NULL, [ProductCategoryDescription] Text NOT NULL);"
    create_table(conn_normalized,create_productcategory_table)
    lines = open(data_filename).readlines()
    length = len(lines)
    Output = []
    i = 1
    while i < length:
        header_values = lines[i].split('\t')
        product_category = header_values[6]
        product_description = header_values[7]
        splitted_categories = product_category.split(';')
        splitted_descriptions = product_description.split(';')
        i = 0
        while i < len(splitted_categories):
            category = splitted_categories[i]
            descriptions = splitted_descriptions[i]
            found = False
            j = 0
            while j < len(Output):
                if Output[j][0] == category:
                    found = True
                    break
                j += 1
            if not found:
                Output.append([category, descriptions])
            i += 1
        i += 1
    i = 0
    while i < len(Output):
        j = i + 1
        while j < len(Output):
            if Output[i][0] > Output[j][0]:
                Output[i], Output[j] = Output[j], Output[i]
            j += 1
        i += 1
    i = 0
    while i < len(Output):
        item = Output[i]
        item.insert(0, i + 1)
        i += 1
    insert_statement = "INSERT INTO ProductCategory VALUES (?,?,?);"
    with conn_normalized:
        cur_conn_normalized.executemany(insert_statement,Output)
    ### END SOLUTION

def step8_create_productcategory_to_productcategoryid_dictionary(normalized_database_filename):
    
    
    ### BEGIN SOLUTION
    conn_normalized    = create_connection(normalized_database_filename)
    select_statement = "Select ProductCategory,ProductCategoryID from ProductCategory"
    ProductCategory_rows = execute_sql_statement(select_statement, conn_normalized)  
    productcategoryid_dictionary = {}
    i = 0
    while i < len(ProductCategory_rows):
        ele = ProductCategory_rows[i]
        productcategoryid_dictionary[ele[0]] = ele[1]
        i += 1
    return productcategoryid_dictionary
    ### END SOLUTION
        

def step9_create_product_table(data_filename, normalized_database_filename):
    # Inputs: Name of the data and normalized database filename
    # Output: None

    
    ### BEGIN SOLUTION
    conn_normalized    = create_connection(normalized_database_filename)
    cur_conn_normalized    = conn_normalized.cursor()
    create_product_table = "CREATE TABLE Product ([ProductID] Interger NOT NULL Primary key, [ProductName] Text NOT NULL, [ProductUnitPrice] Real NOT NULL, [ProductCategoryID] Integer NOT NULL, FOREIGN KEY(ProductCategoryID) REFERENCES ProductCategory(ProductCategoryID));"
    create_table(conn_normalized,create_product_table)
    product_rows = step8_create_productcategory_to_productcategoryid_dictionary(normalized_database_filename)
    ProductID = 1
    with open(data_filename, 'r') as file:
        values = file.readlines()[1:]
        products = []
        mid_op = set()
        line_index = 0
        while line_index < len(values):
            line = values[line_index]
            cols = line.strip().split('\t')
            product_names = cols[5].split(';')
            product_prices = [round(float(price), 2) for price in cols[8].split(';')]
            product_categories = cols[6].split(';')
            name_index = 0
            while name_index < len(product_names):
                name = product_names[name_index]
                price = product_prices[name_index]
                category = product_categories[name_index]
                if category in product_rows and name not in mid_op:
                    products.append([ProductID, name, price, product_rows[category]])
                    mid_op.add(name)
                name_index += 1
            line_index += 1
        sorted_products = sorted(products, key=lambda p: p[1])
        Output = []
        i = 0
        while i < len(sorted_products):
            product = sorted_products[i]
            product_id = ProductID + i
            row = [product_id, product[1], str(product[2]), product[3]]
            Output.append(row)
            i += 1
    insert_statement = "INSERT INTO Product VALUES (?,?,?,?);"
    with conn_normalized:
        cur_conn_normalized.executemany(insert_statement,Output)
    ### END SOLUTION


def step10_create_product_to_productid_dictionary(normalized_database_filename):
    
    ### BEGIN SOLUTION
    conn_normalized = create_connection(normalized_database_filename)
    select_statement = "Select ProductName,ProductID from Product"
    Product_rows = execute_sql_statement(select_statement, conn_normalized)  
    productid_dictionary = {}
    i = 0
    while i < len(Product_rows):
        productid_dictionary[Product_rows[i][0]] = Product_rows[i][1]
        i += 1
    return productid_dictionary
    ### END SOLUTION
        

def step11_create_orderdetail_table(data_filename, normalized_database_filename):
    # Inputs: Name of the data and normalized database filename
    # Output: None

    
    ### BEGIN SOLUTION
    import datetime
    conn_normalized    = create_connection(normalized_database_filename)
    cur_conn_normalized    = conn_normalized.cursor()
    create_orderdetail_table = "CREATE TABLE OrderDetail ([OrderID] Integer NOT NULL Primary Key, [CustomerID] Integer NOT NULL, [ProductID] Integer NOT NULL, [OrderDate] Integer NOT NULL, [QuantityOrdered] Integer NOT NULL);"
    create_table(conn_normalized,create_orderdetail_table)
    product_dict = step10_create_product_to_productid_dictionary(normalized_database_filename)
    customer_dict = step6_create_customer_to_customerid_dictionary(normalized_database_filename)
    header_values = open(data_filename).readlines()
    OrderID = 1
    Output = []
    ele = 1
    while ele < len(header_values):
        rows = header_values[ele].split('\t')
        index = 0
        while index < len(rows):
            if index == 0:
                Customername = rows[index]
            elif index == 5:
                ProductID = rows[index]
            elif index == 9:
                QuantityOrdered = rows[index]
            elif index == 10:
                OrderDate = rows[index]
            index += 1
        index = 0
        ProductIDs = ProductID.split(';')
        QuantityOrdereds = QuantityOrdered.split(';')
        OrderDates = OrderDate.split(';')
        while index < len(ProductIDs):
            ProductID_inner = ProductIDs[index]
            QuantityOrdered_inner = QuantityOrdereds[index]
            OrderDate_inner = OrderDates[index]
            order_date = OrderDate_inner.strip()[0:4] + '-' + OrderDate_inner.strip()[4:6] + '-' + OrderDate_inner.strip()[6:8]
            temp_list = []
            temp_list.append(OrderID)
            temp_list.append(customer_dict[Customername])
            temp_list.append(product_dict[ProductID_inner])
            temp_list.append(order_date)
            temp_list.append(int(QuantityOrdered_inner))
            Output.append(temp_list)
            OrderID += 1
            index += 1
        ele += 1
    index = 0
    new_output = []
    while index < len(Output):
        row = Output[index]
        temp_list = [index + 1] + row[1:]
        new_output.append(temp_list)
        index += 1
    Output = new_output
    insert_statement = "INSERT INTO OrderDetail VALUES (?,?,?,?,?);"
    with conn_normalized:
        cur_conn_normalized.executemany(insert_statement,Output)
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
    customerid_dict=step6_create_customer_to_customerid_dictionary('normalized.db')
    customer_name = []
    keys = list(customerid_dict.keys())
    values = list(customerid_dict.values())
    i = 0
    while i < len(keys):
        if keys[i] == CustomerName:
            customer_name.append(values[i])
            break
        i += 1
    customer_name = customer_name[0]
    sql_statement = f"""
                    SELECT customer.FirstName || ' ' || customer.LastName AS Name,
                        product_detail.ProductName,
                        order_detail.OrderDate,
                        product_detail.ProductUnitPrice,
                        order_detail.QuantityOrdered,
                        round(product_detail.ProductUnitPrice*order_detail.QuantityOrdered, 2) AS Total
						FROM OrderDetail order_detail
							JOIN Product product_detail ON order_detail.ProductID = product_detail.ProductID
							JOIN Customer customer ON order_detail.CustomerID = customer.CustomerID
						WHERE customer.CustomerID = '{customer_name}'
						"""
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
    customerid_dict=step6_create_customer_to_customerid_dictionary('normalized.db')
    customer_name = []
    keys = list(customerid_dict.keys())
    values = list(customerid_dict.values())
    i = 0
    while i < len(keys):
        if keys[i] == CustomerName:
            customer_name.append(values[i])
            break
        i += 1
    customer_name = customer_name[0]
    sql_statement = f"""
                    SELECT customer.FirstName || ' ' || customer.LastName AS Name,
                        round(sum(product_detail.ProductUnitPrice*order_detail.QuantityOrdered),2) AS Total 
                        From OrderDetail order_detail 
						    JOIN Product product_detail ON order_detail.ProductID = product_detail.ProductID 
						    JOIN Customer customer ON order_detail.CustomerID = customer.CustomerID 
                        where customer.CustomerID = '{customer_name}' 
                        GROUP BY Name;
                        """
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
    sql_statement = """SELECT customer.FirstName || ' ' || customer.LastName AS Name,
						round(sum(product_detail.ProductUnitPrice*order_detail.QuantityOrdered),2) AS Total 
						from OrderDetail order_detail 
							JOIN Product product_detail ON order_detail.ProductID = product_detail.ProductID 
							JOIN Customer customer ON order_detail.CustomerID = customer.CustomerID  
						GROUP BY Name ORDER BY Total DESC;
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

    sql_statement = """SELECT region.Region, 
						round(sum(product_detail.ProductUnitPrice*order_detail.QuantityOrdered),2) AS Total 
						From OrderDetail order_detail 
							JOIN Product product_detail ON order_detail.ProductID = product_detail.ProductID 
							JOIN Customer customer ON order_detail.CustomerID = customer.CustomerID 
							JOIN Country country ON  customer.CountryID = country.CountryID 
							JOIN Region region ON region.RegionID = country.RegionID 
						GROUP BY Region ORDER BY Total DESC;    
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

    sql_statement = """SELECT country.Country, 
						round(sum(product_detail.ProductUnitPrice*order_detail.QuantityOrdered)) AS CountryTotal 
						From OrderDetail order_detail
							JOIN Product product_detail ON order_detail.ProductID = product_detail.ProductID 
							JOIN Customer customer ON order_detail.CustomerID = customer.CustomerID 
							JOIN Country country ON  customer.CountryID = country.CountryID   
						GROUP BY Country ORDER BY CountryTotal DESC;
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

    sql_statement = """SELECT region.Region, country.Country, 
						round(sum(product_detail.ProductUnitPrice*order_detail.QuantityOrdered)) AS CountryTotal, 
						RANK() OVER(PARTITION BY region.Region ORDER BY sum(product_detail.ProductUnitPrice*order_detail.QuantityOrdered) DESC) AS CountryRegionalRank 
						From OrderDetail order_detail 
							JOIN Product product_detail ON order_detail.ProductID = product_detail.ProductID 
							JOIN Customer customer ON order_detail.CustomerID = customer.CustomerID 
							JOIN Country country ON  customer.CountryID = country.CountryID 
							JOIN Region region ON region.RegionID = country.RegionID 
						GROUP BY Country ORDER BY region.Region ASC, CountryTotal DESC;     
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

    sql_statement = """ Select * From (Select region.Region, country.Country, 
						round(sum(product_detail.ProductUnitPrice*order_detail.QuantityOrdered)) AS CountryTotal, 
						RANK() OVER(PARTITION BY region.Region ORDER BY sum(product_detail.ProductUnitPrice*order_detail.QuantityOrdered) DESC) AS CountryRegionalRank 
						From OrderDetail order_detail 
							JOIN Product product_detail ON order_detail.ProductID = product_detail.ProductID 
							JOIN Customer customer ON order_detail.CustomerID = customer.CustomerID 
							JOIN Country country ON  customer.CountryID = country.CountryID 
							JOIN Region region ON region.RegionID = country.RegionID
						GROUP BY Country ORDER BY region.Region ASC, CountryTotal DESC) 
						WHERE CountryRegionalRank = 1;    
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
                                WHEN SUBSTR(OrderDate, 6, 2) IN ('01', '02', '03') THEN 'Q1'
                                WHEN SUBSTR(OrderDate, 6, 2) IN ('04', '05', '06') THEN 'Q2'
                                WHEN SUBSTR(OrderDate, 6, 2) IN ('07', '08', '09') THEN 'Q3'
                                ELSE 'Q4'
                            END AS Quarter,
                            CAST(strftime('%Y', OrderDate) AS INTEGER) AS Year,
                            Customer.CustomerID,
                            ROUND(SUM(ProductUnitPrice * QuantityOrdered)) AS Total
                            FROM OrderDetail
                                JOIN Customer ON Customer.CustomerID = OrderDetail.CustomerID
                                JOIN Product ON Product.ProductID = OrderDetail.ProductID
                            GROUP BY 
                                Customer.CustomerID, Year, Quarter
                            ORDER BY 
                                Year, Quarter, Customer.CustomerID;
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

    sql_statement = """SELECT * FROM ( 
                            SELECT 
                                Quarter, 
                                Year, 
                                CustomerID, 
                                Total, 
                                ROW_NUMBER() OVER(PARTITION BY Year, Quarter ORDER BY Year, Quarter ASC) AS CustomerRank 
                            FROM (
                                    SELECT
                                        CASE 
                                            WHEN CAST(substr(order_detail.OrderDate, 6, 2) AS INTEGER) BETWEEN 1 AND 3 THEN 'Q1'
                                            WHEN CAST(substr(order_detail.OrderDate, 6, 2) AS INTEGER) BETWEEN 4 AND 6 THEN 'Q2'
                                            WHEN CAST(substr(order_detail.OrderDate, 6, 2) AS INTEGER) BETWEEN 7 AND 9 THEN 'Q3'
                                            WHEN CAST(substr(order_detail.OrderDate, 6, 2) AS INTEGER) BETWEEN 10 AND 12 THEN 'Q4'
                                        END AS Quarter, 
                                        CAST(substr(order_detail.OrderDate, 1, 4) AS INTEGER) AS Year, 
                                        customer.CustomerID, 
                                        ROUND(SUM(product_detail.ProductUnitPrice*order_detail.QuantityOrdered)) AS Total
                                    FROM 
                                        OrderDetail order_detail 
                                        JOIN customer customer ON customer.CustomerID = order_detail.CustomerID 
                                        JOIN Product product_detail ON product_detail.ProductID = order_detail.ProductID 
                                    GROUP BY 
                                        customer.CustomerID,
                                        Year,
                                        Quarter
                                    ORDER BY 
                                        Year,
                                        Total DESC 
                                ) AS table1
                        ) AS table2
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

    sql_statement = """WITH salesmonth AS (
                            SELECT CASE substr(order_detail.OrderDate, 6, 2)
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
                            SUM(ROUND(product_detail.ProductUnitPrice*order_detail.QuantityOrdered)) as Total 
                            FROM OrderDetail order_detail 
                                JOIN customer customer ON customer.CustomerID = order_detail.CustomerID 
                                JOIN Product product_detail ON product_detail.ProductID = order_detail.ProductID
                            GROUP BY Month
                        )
                        SELECT Month, Total, 
                            RANK() OVER(ORDER BY Total DESC) TotalRank 
                        FROM salesmonth 
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