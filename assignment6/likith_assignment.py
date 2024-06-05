import pandas as pd
import sqlite3
from sqlite3 import Error

conn_orders = sqlite3.connect("orders.db")
cur = conn_orders.cursor()

# sql_statement = "select * from customers;"
# df = pd.read_sql_query(sql_statement, conn_orders)
# display(df)

# sql_statement = "select * from orders;"
# df = pd.read_sql_query(sql_statement, conn_orders)
# display(df)

# sql_statement = "select * from vendors;"
# df = pd.read_sql_query(sql_statement, conn_orders)
# display(df)

# sql_statement = "select * from products;"
# df = pd.read_sql_query(sql_statement, conn_orders)
# display(df)

# sql_statement = "select * from orderitems;"
# df = pd.read_sql_query(sql_statement, conn_orders)
# display(df)

# sql_statement = "select * from productnotes;"
# df = pd.read_sql_query(sql_statement, conn_orders)
# display(df)


def ex1():
    # Write an SQL statement that SELECTs all rows from the `customers` table
    # output columns: cust_name, cust_email

    ### BEGIN SOLUTION
    sql_statement = "select cust_name, cust_email from customers"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement


def ex2():
    # Write an SQL statement that SELECTs all rows from the `products` table
    # output columns: vend_id

    ### BEGIN SOLUTION
    sql_statement = "select vend_id from products"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement


def ex3():
    # Write an SQL statement that SELECTs distinct rows for vend_id from the `products` table
    # output columns: vend_id

    ### BEGIN SOLUTION
    sql_statement = "select distinct(vend_id) from products"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement


def ex4():
    # Write an SQL statement that SELECTs the first five rows from the `products` table
    # output columns: prod_name

    ### BEGIN SOLUTION
    sql_statement = "select prod_name from products LIMIT  5"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement


def ex5():
    # Write an SQL statement that SELECTs 4 rows starting from row 3 from `products` table
    # output columns: prod_name

    ### BEGIN SOLUTION
    sql_statement = "select prod_name from products LIMIT 4 OFFSET 3"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement


def ex6():
    # Write an SQL statement that SELECTs all rows from `products` table and sorts by prod_name
    # output columns: prod_name

    ### BEGIN SOLUTION
    sql_statement = "SELECT prod_name from products ORDER BY prod_name "
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement


def ex7():
    # Write an SQL statement that SELECTs all rows from `products` table and sorts by prod_price and then prod_name 
    # output columns: prod_id, prod_price, prod_name

    ### BEGIN SOLUTION
    sql_statement = "SELECT prod_id, prod_price, prod_name from products ORDER BY prod_price , prod_name "
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement


def ex8():
    # Write an SQL statement that SELECTs all rows from `products` table and sorts by prod_price (descending order)
    # and then prod_name 
    # output columns: prod_id, prod_price, prod_name

    ### BEGIN SOLUTION
    sql_statement = "SELECT prod_id, prod_price, prod_name from products ORDER BY prod_price DESC , prod_name  "
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement


def ex9():
    # Write an SQL statement that SELECTs all rows from `products` table where the price of product is 2.50
    # output columns: prod_id, prod_price, prod_name

    ### BEGIN SOLUTION
    sql_statement = "SELECT prod_id, prod_price, prod_name from products WHERE prod_price = 2.50 "
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement

def ex10():
    # Write an SQL statement that SELECTs all rows from `products` table where the name of product is Oil can
    # output columns: prod_id, prod_price, prod_name

    ### BEGIN SOLUTION
    sql_statement = "SELECT prod_id, prod_price, prod_name from products WHERE prod_name = 'Oil can' "
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement


def ex11():
    # Write an SQL statement that SELECTs all rows from `products` table where the price of product is 
    # less than or equal to 10
    # output columns: prod_id, prod_price, prod_name

    ### BEGIN SOLUTION
    sql_statement = "SELECT prod_id, prod_price, prod_name from products WHERE prod_price <  10 or prod_price =  10 " 
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement


def ex12():
    # Write an SQL statement that SELECTs all rows from `products` table where the vendor id is not equal to 1003
    # output columns: vend_id, prod_name

    ### BEGIN SOLUTION
    sql_statement = "SELECT vend_id, prod_name from products WHERE vend_id != 1003  "
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement

def ex13():
    # Write an SQL statement that SELECTs all rows from `products` table where the product prices are between 5 and 10
    # output columns: prod_name, prod_price

    ### BEGIN SOLUTION
    sql_statement = "SELECT prod_name, prod_price from products WHERE prod_price BETWEEN 5 AND 10 "
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement


def ex14():
    # Write an SQL statement that SELECTs all rows from the `customers` table where the customer email is empty
    # output columns: cust_id, cust_name

    ### BEGIN SOLUTION
    sql_statement = "SELECT cust_id, cust_name from  customers WHERE cust_email IS NULL"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement


def ex15():
    # Write an SQL statement that SELECTs all rows from the `products` table where the vender id is 1003 and
    # the price is less than or equal to 10. 
    # output columns: vend_id, prod_id, prod_price, prod_name

    ### BEGIN SOLUTION
    sql_statement = "SELECT vend_id, prod_id, prod_price, prod_name FROM products WHERE vend_id = 1003 AND prod_price <  10 or prod_price =  10 "
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement

def ex16():
    # Write an SQL statement that SELECTs all rows from the `products` table where the vender id is 1002 or 1003 and
    # the price is greater than or equal to 5. 
    # output columns: vend_id, prod_id, prod_price, prod_name

    ### BEGIN SOLUTION
    sql_statement = "SELECT vend_id, prod_id, prod_price, prod_name FROM products WHERE (vend_id  =  1002  OR  vend_id  =  1003) AND prod_price >=  5 "
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement

def ex17():
    # Write an SQL statement that SELECTs all rows from the `products` table where the vender id is 1002 or 1003 or 1005.
    # Use the IN operator for this!
    # output columns: vend_id, prod_id, prod_price, prod_name

    ### BEGIN SOLUTION
    sql_statement = "SELECT vend_id, prod_id, prod_price, prod_name FROM products WHERE vend_id  IN (1002 , 1003 , 1005)"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement


def ex18():
    # Write an SQL statement that SELECTs all rows from the `products` table where the vender id is NOT 1002 or 1003.
    # Use the NOT IN operator for this!
    # output columns: vend_id, prod_id, prod_price, prod_name

    ### BEGIN SOLUTION
    sql_statement = "SELECT vend_id, prod_id, prod_price, prod_name FROM products WHERE vend_id  NOT IN (1002 , 1003 )"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement

def ex19():
    # Write an SQL statement that SELECTs all rows from the `products` table where the product name starts with 'jet'
    # output columns: prod_id, prod_price, prod_name

    ### BEGIN SOLUTION
    sql_statement = "SELECT prod_id, prod_price, prod_name FROM products WHERE prod_name LIKE '%jet%' "
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement

def ex20():
    # Write an SQL statement that SELECTs all rows from the `products` table where the product name ends with 'anvil'
    # output columns: prod_id, prod_price, prod_name

    ### BEGIN SOLUTION
    sql_statement = "SELECT prod_id, prod_price, prod_name FROM products WHERE prod_name LIKE '%anvil' "
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement

def ex21():
    # Write an SQL statement that SELECTs all rows from the `vendors` table. Concatenate vendor name and vendor country
    # as vend_title. Order by vend_title. Leave space in between -- example `ACME (USA)`
    # output columns: vend_title

    ### BEGIN SOLUTION 
    sql_statement = "SELECT vend_name ||  ' ' || '(' || vend_country || ')' as vend_title FROM vendors ORDER BY   vend_title"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement


def ex22():
    # Write an SQL statement that SELECTs all rows from the `orderitems` table where order number is 20005. 
    # Display an extra calculated column called `expanded_price` that is the result of quantity multiplied by item_price.
    # Round the value to two decimal places. 
    # output columns: prod_id, quantity, item_price, expanded_price

    ### BEGIN SOLUTION
    sql_statement = "SELECT prod_id, quantity, item_price, round((quantity  * item_price ) , 2) as expanded_price   FROM orderitems WHERE order_num = 20005 "
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement

def ex23():
    # Write an SQL statement that SELECTs all rows from the `orders` table where the order date is between 
    # 2005-09-13 and 2005-10-04
    # output columns: order_num, order_date
    # https://www.sqlitetutorial.net/sqlite-date-functions/sqlite-date-function/
    
    ### BEGIN SOLUTION
    sql_statement = "Select order_num, order_date from orders WHERE order_date BETWEEN '2005-09-13' AND '2005-10-04'"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement

def ex24():
    # Write an SQL statement that calculates the average price of all rows in the `products` table. 
    # Call the average column avg_price
    # output columns: avg_price

    ### BEGIN SOLUTION
    # output columns: avg_price
    sql_statement = "select avg(prod_price) as avg_price from products "
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement


def ex25():
    # Write an SQL statement that calculates the average price of all rows in the `products` table 
    # where the vendor id is 1003 . Call the average column avg_price
    # output columns: avg_price

    ### BEGIN SOLUTION
    sql_statement ="select avg(prod_price) as avg_price from products  where vend_id = 1003 " 
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement



def ex26():
    # Write an SQL statement that counts the number of customers in the `customers` table 
    # Call the count column num_cust
    # output columns: num_cust

    ### BEGIN SOLUTION
    sql_statement = "select count(cust_id) as num_cust from customers"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement

def ex27():
    # Write an SQL statement that calculates the max price in the `products` table 
    # Call the max column max_price. Round the value to two decimal places. 
    # output columns: max_price

    ### BEGIN SOLUTION
    sql_statement = "Select ROUND(MAX(prod_price), 2) AS max_price from products"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement

def ex28():
    # Write an SQL statement that calculates the min price in the `products` table 
    # Call the min column min_price. Round the value to two decimal places. 
    # output columns: min_price

    ### BEGIN SOLUTION
    sql_statement = "Select ROUND(MIN(prod_price), 2) AS min_price from products"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement

def ex29():
    # Write an SQL statement that sums the quantity in the `orderitems` table where order number is 20005. 
    # Call the sum column items_ordered
    # output columns: items_ordered

    ### BEGIN SOLUTION
    sql_statement = "SELECT SUM(quantity) AS items_ordered FROM orderitems WHERE order_num = 20005"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn_orders)
    # display(df)
    return sql_statement


#---------------------------------------------------------------------------------------------------------------------------------------------#

# You cannot use Pandas! I will deduct points after manual check if you use Pandas. You CANNOT use the 'csv' module to read the file

# Hint: Ensure to strip all strings so there is no space in them

# DO NOT use StudentID from the non_normalized table. Let the normalized table automatically handle StudentID. 


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


def create_table(conn, create_table_sql):
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

# conn_non_normalized = create_connection('non_normalized.db')
# sql_statement = "select * from Students;"
# df = pd.read_sql_query(sql_statement, conn_non_normalized)
# display(df)


def normalize_database(non_normalized_db_filename):
#     Normalize 'non_normalized.db'
#     Call the normalized database 'normalized.db'
#     Function Output: No outputs
#     Requirements:
#     Create four tables
#     Degrees table has one column:
#         [Degree] column is the primary key
    
#     Exams table has two columns:
#         [Exam] column is the primary key column
#         [Year] column stores the exam year
    
#     Students table has four columns:
#         [StudentID] primary key column 
#         [First_Name] stores first name
#         [Last_Name] stores last name
#         [Degree] foreign key to Degrees table
        
#     StudentExamScores table has four columns:
#         [PK] primary key column,
#         [StudentID] foreign key to Students table,
#         [Exam] foreign key to Exams table ,
#         [Score] exam score

    
    ### BEGIN SOLUTION
    create_non_normalized    = create_connection(non_normalized_db_filename)
    create_non_normalized_1  = create_connection('normalized.db', True)
    cursor_non_normalized    = create_non_normalized.cursor()
    cursor_normalized        = create_non_normalized_1.cursor()

###################################################################################
    create_degree_table = """CREATE TABLE [DEGREES] (
    [DEGREE] TEXT NOT NULL PRIMARY KEY
    ); 
    """
    
###################################################################################
    create_exam_table = """CREATE TABLE [EXAMS] (
    [exam] TEXT  NOT NULL PRIMARY KEY,
    [year] integer not null
    ); 
    """
    
###################################################################################
    create_student_table = """CREATE TABLE [STUDENTS] (
    [StudentID]  INTEGER  NOT NULL PRIMARY KEY,
    [FIRST_NAME] text not null,
    [LAST_NAME] text not null,
    [DEGREE] text not null,
    FOREIGN KEY(DEGREE) REFERENCES DEGREES(DEGREE)
    );
    """
   
###################################################################################
    create_studentexamsscores_table = """CREATE TABLE [STUDENTEXAMSCORES] (
    [PK] INTEGER NOT NULL PRIMARY KEY,
    [STUDENTID] integer not null,
    [EXAM] text not null,
    [SCORE] integer not null,
    FOREIGN KEY(STUDENTID) REFERENCES STUDENTS(STUDENTID),
    FOREIGN KEY(EXAM) REFERENCES EXAMS(EXAM)
    );
    """
###################################################################################

    def create_insert_degrees (create_non_normalized, values):
        sql = ''' INSERT INTO Degrees(degree)
                  VALUES(?) '''
        cursor_non_normalized    = create_non_normalized.cursor()
        cursor_non_normalized.execute(sql, values)
        return cursor_non_normalized.lastrowid
    
#################################################################################### 
    
    def insert_exam_values(exams, years):
        create_non_normalized_1 = ...
        for e, exam in enumerate(exams):
            create_insert_exam(create_non_normalized_1, (exam, years[e],))

###################################################################################

    def create_insert_exam(create_non_normalized, values):
        sql = ''' INSERT INTO Exams(exam, year)
                  VALUES(?, ?) '''
        cursor_non_normalized    = create_non_normalized.cursor()
        cursor_non_normalized.execute(sql, values)
        return cursor_non_normalized.lastrowid
    
###################################################################################

    def create_insert_students(create_non_normalized, values):
        sql = ''' INSERT INTO Students(First_Name, Last_Name, Degree)
                  VALUES(?, ?, ?) '''
        cursor_non_normalized    = create_non_normalized.cursor()
        cursor_non_normalized.execute(sql, values)
        return cursor_non_normalized.lastrowid
    
###################################################################################
    def insert_studentexamscores(create_non_normalized, values):
        sql = ''' INSERT INTO StudentExamScores(StudentId, Exam, Score)
                  VALUES(?, ?, ?) '''
        cursor_non_normalized    = create_non_normalized.cursor()
        cursor_non_normalized.execute(sql, values)
        return cursor_non_normalized.lastrowid

###################################################################################

    create_degrees = "SELECT DISTINCT degree from students"
    create_rows = execute_sql_statement(create_degrees, create_non_normalized)
    degrees = [i[0].strip() for i in create_rows]

###################################################################################

    create_exams = "SELECT DISTINCT exams FROM students"
    create_rows = execute_sql_statement(create_exams, create_non_normalized)
    create_exam_column = []
    create_year_column = []
    for ele in create_rows:
        create_exam = [i.strip() for elee in ele for i in elee.split(',')]
        for i in create_exam:
            exam, year = i.split()[0], i.split()[1].lstrip('(').rstrip(')')
            if exam not in create_exam_column:
                create_exam_column.append(exam)
                create_year_column.append(year)


################################################################################## 

    create_students = "SELECT StudentId,Name,Degree FROM students"
    create_rows     = execute_sql_statement(create_students, create_non_normalized)
    first_name      = [ele[1].strip().split(',')[1].strip() for ele in create_rows]
    last_name       = [ele[1].strip().split(',')[0].strip() for ele in create_rows]
    degree          = [ele[2].strip() for ele in create_rows]

##################################################################################

    create_scores = "SELECT StudentId,Exams,Scores FROM students"
    create_rows = execute_sql_statement(create_scores, create_non_normalized)
    studentid = []
    studentexam = []
    studentscore = []
    _ = [(studentid.append(id),studentexam.append(exam[j].strip().split(' ')[0].strip()),
        studentscore.append(int(score[j].strip()))
    )for id, ex, sc in create_rows for j in range(len(ex.strip().split(',')))
    for exam, score in [(ex.strip().split(','), sc.strip().split(','))]]

###################################################################################


    create_table(create_non_normalized_1, create_degree_table)

    create_table(create_non_normalized_1, create_exam_table)

    create_table(create_non_normalized_1, create_student_table)

    create_table(create_non_normalized_1, create_studentexamsscores_table)


###################################################################################

    with create_non_normalized_1:
        [(create_insert_degrees(create_non_normalized_1, (ele, ))) for ele in degrees]
   
    with create_non_normalized_1:
        [(create_insert_exam(create_non_normalized_1, (create_exam_column[ele], create_year_column[ele],))) for ele in range(len(create_exam_column))]

    with create_non_normalized_1:
        [create_insert_students(create_non_normalized_1, (first_name[ele], last_name[ele], degree[ele], )) for ele in range(len(first_name))]
    
    with create_non_normalized_1:
        [insert_studentexamscores(create_non_normalized_1, (studentid[ele], studentexam[ele], studentscore[ele], )) for ele in range(len(studentid))]
  

##################################################################################
    ### END SOLUTION
        
    
# normalize_database('non_normalized.db')
# conn_normalized = create_connection('normalized.db')

def ex30(conn):
    # Write an SQL statement that SELECTs all rows from the `Exams` table and sort the exams by Year
    # output columns: exam, year
    
    ### BEGIN SOLUTION
    sql_statement = "select exam as Exam, year as Year from Exams ORDER BY year, exam;"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn)
    # display(df)
    return sql_statement


def ex31(conn):
    # Write an SQL statement that SELECTs all rows from the `Degrees` table and sort the degrees by name
    # output columns: degree
    
    ### BEGIN SOLUTION
    sql_statement = "select Degree as Degree from Degrees ORDER BY Degree;"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn)
    # display(df)
    return sql_statement


def ex32(conn):
    # Write an SQL statement that counts the numbers of gradate and undergraduate students
    # output columns: degree, count_degree
    
    ### BEGIN SOLUTION
    sql_statement = "select Degree as Degree, count(Degree) as count_degree from Students GROUP BY Degree;"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn)
    # display(df)
    return sql_statement


def ex33(conn):
    # Write an SQL statement that calculates the exam averages for exams; sort by average in descending order.
    # output columns: exam, year, average
    # round to two decimal places
    
    
    ### BEGIN SOLUTION
    sql_statement = "select Exams.exam as Exam, Exams.year as Year, round(avg(StudentExamScores.score),2) as average from StudentExamScores inner join Exams on Exams.exam = StudentExamScores.exam group by Exams.exam order by average DESC"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn)
    # display(df)
    return sql_statement


def ex34(conn):
    # Write an SQL statement that calculates the exam averages for degrees; sort by average in descending order.
    # output columns: degree, average 
    # round to two decimal places
    
    ### BEGIN SOLUTION
    sql_statement = "select Degrees.degree as Degree, round(avg(StudentExamScores.score),2) as average from StudentExamScores inner join Students on Students.StudentID = StudentExamScores.StudentID inner join Exams on Exams.exam = StudentExamScores.exam inner join Degrees on Degrees.degree = Students.degree group by Degrees.degree order by average DESC"
    ### END SOLUTION
    # df = pd.read_sql_query(sql_statement, conn)
    # display(df)
    return sql_statement

def ex35(conn):
    # Write an SQL statement that calculates the exam averages for students; sort by average in descending order. Show only top 10 students
    # output columns: first_name, last_name, degree, average
    # round to two decimal places
    # Order by average in descending order
    # Warning two of the students have the same average!!!
    
    ### BEGIN SOLUTION
    sql_statement = "select Students.First_Name as First_Name, Students.Last_Name as Last_Name, Degrees.degree as Degree, round(avg(StudentExamScores.score),2) as average from StudentExamScores inner join Students on Students.StudentID = StudentExamScores.StudentID inner join Degrees on Degrees.degree = Students.degree group by Students.StudentID order by average DESC limit 10"
    ### END SOLUTION 
    # df = pd.read_sql_query(sql_statement, conn)
    # display(df)
    return sql_statement