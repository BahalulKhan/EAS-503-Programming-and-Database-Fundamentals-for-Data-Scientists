def eas503_ex27(month, day):

    # The year is divided into four season: spring, summer, fall (or autumn) and winter.
    # While the exact dates that the seasons change vary a little bit from year to
    # year because of the way that the calender is constructed, we will use the following
    # dates for this exercise:

    # Season  -- First Day
    # Spring  -- March 20
    # Summer  -- June 21
    # Fall  -- September 22
    # Winter    -- December 21

    # Complete this function which takes in as inputs a month and day. It should
    # output the season.
    # input 1: month -- str
    # input 2: day -- int

    # output: month -- str (Spring, Summer, Fall, Winter)

    # BEGIN SOLUTION
    
    if month in ('March','April','May'):
        return f'Spring'
    elif ({month} == 'March') and ({day} > 19):
        return f'Spring'
    elif ({month} == 'June') and ({day} < 21):
        return f'Spring'
    elif month in ('June','July','August','September'):
        return f'Summer'
    elif ({month} == 'June') and ({day} > 20):
        return f'Summer'
    elif ({month} == 'September') and ({day} < 22):
        return f'Summer'
    elif month in ('September','October','November','December'):
        return f'Fall'
    elif ({month} == 'September') and ({day} > 21):
        return f'Fall'
    elif ({month} == 'December') and ({day} < 20):
        return f'Fall'
    else:
        return f'Winter'
    # END SOLUTION


def eas503_ex28(year):
    # Complete this function to check if year is a leap year
    # Input: year
    # Output: True or False (Boolean)

    # BEGIN SOLUTION
    if (year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False

    # END SOLUTION


def eas503_ex29(month, day, year):
    # Complete this function to check if a data is valid, given month, day, and year.
    # For example, 5/24/1962 is valid, but 9/31/2000 is not
    # Inputs: month, day, year
    # Output: True or False (Boolean)
    # IMPORTANT: Use the function ex28() to determine if year is leap year

    # BEGIN SOLUTION
    if (month in [1 , 3 , 5 , 7 , 8 , 10 , 12]):
        if(day <= 31):
            return True
        else:
            return False
    elif(month in [4 , 6 , 9 , 11]):
        if(day <= 30):
            return True
        else:
            return False
    elif(month in [2]):
        if(eas503_ex28(year) == True):
            if(day <= 29):
                return True
        else:
            if(day == 29):
                return False
    # END SOLUTION


def eas503_ex30(month, day, year):
    # Complete this function to calculate the day_number given month, day, and year.
    # Information: The days of the year are often numbered from 1 through 365 (or 366).
    # This number can be computed in three steps using int arithmetic:
    # (a) - day_num = 31 * (month - 1) + day
    # (b) - if the month is after February subtract (4*(month)+23)//10
    # (c) - if it's a leap year and after February 29, add 1
    # Hint: First verify the input date is valid, return False if it is not valid; use is_date_valid
    # IMPORTANT: use the functions you wrote previous, namely, ex28 and ex29.
    # Inputs: month, day, year
    # Output: the day number or False (boolean) if the date is invalid.

    # BEGIN SOLUTION
    day_num = 31 * (month - 1) + day
    b = (4*(month)+23)//10
    c = day_num - b
    d = c + 1
    if(eas503_ex29(month, day, year) == True):
        if(eas503_ex28(year) == True):
            if(month > 2):
                return d
            else:
                return day_num
        elif(month > 2):
            return c
        else:
            return day_num
    else:
        return False

    # END SOLUTION


def eas503_ex31(plate):

    # In a particular jurisdiction, older license plates consist of three uppercase
    # letters followed by three digits. When all of the license plates following
    # that pattern had been used, the format was changed to four digits followed by
    # three uppercase letters.

    # Complete this function whose only input is a license plate and its output
    # is: 1) Older/Valid 2) Newer/Valid 3) Invalid
    # input: plate (str)
    # output: 'Older/Valid' or 'Newer/Valid' or 'Invalid'
    # HINT: Use the comparator operators (>=, <=)!

    # BEGIN SOLUTION
    if len(plate) == 6:
        if plate[0:2].isalpha() and plate[0:2].isupper():
            if plate[3:5].isdigit():
                return 'Older/Valid'
            else:
                return 'Invalid'
        else:
            return 'Invalid'
    elif len(plate) == 7:
        if plate[0:3].isdigit():
            if plate[4:6].isalpha() and plate[4:6].isupper():
                return 'Newer/Valid'
            else:
                return 'Invalid'
        else:
            return 'Invalid'
    else:
        return 'Invalid'
    # END SOLUTION


def eas503_ex32(date):

    # A magic date is a date where the day multiplied by the month is equal
    # to the two digit year. For example, June 10, 1960 is a magic date because
    # June is the sixth month, and 6 times 10 is 60, which is equal to the two
    # digit year. Complete this function to determine whether or not a date is
    # a magic date.

    # input: date (str -- month/day/year) -- e.g., 06/01/2022 -- will have leading zero before month and day
    # output: True or False (bool)
    # Hint: use string indexing to extract the month, day, and year from the date string

    # BEGIN SOLUTION
    month, day, year = date.split('/')
    magicdate = int(month) * int(day)
    year = int(year) % 100
    if magicdate == year:
        return True
    else:
        return False
    # END SOLUTION

def eas503_ex33(password):
    # In this exercise you will complete this function to determine whether or not
    # a password is good. We will define a good password to be a one that is at least
    # 8 characters long and contains at least one uppercase letter, at least one lowercase
    # letter, at least one number, and at least one of the following special characters (!, @, #, $, ^).
    # This function should return True if the password
    # passed to it as its only parameter is good. Otherwise it should return False.
    #
    # input: password (str)
    # output: True or False (bool)
    # BEGIN SOLUTION
    special_characters = ['!' , '@' , '#' , '$' , '^']
    if (len(password) >= 8):
        if any(x.isalpha() for x in password) and any(x.isupper() for x in password) and any(x.islower() for x in password) and any(x.isdigit() for x in password) and any(x in special_characters for x in password):
            return True
        else:
            return False
    else:
        return False

    # END SOLUTION


def eas503_ex34(sentence):
    # Complete this function to calculate the average
    # word length in a sentence
    # Input: sentence
    # Output: average word length in sentence
    # Hint: count punctuations with whatever word they are `touching`
    # Hint: round the average to two decimal places

    # BEGIN SOLUTION
    wordcount = len(sentence.split())
    length = sum(not chr.isspace() for chr in sentence)
    average = length / wordcount
    return round(average , 2)
    # END SOLUTION


def eas503_ex35(filename):
    # Complete this function to count the number of lines, words, and chars in a file.
    # Input: filename
    # Output: a tuple with line count, word count, and char count -- in this order

    # BEGIN SOLUTION
    file = open(filename, 'rt')
    line_count = 0
    word_count = 0
    char_count = 0
    for count in file:
        line_count += 1
        word_count += len(count.split())
        char_count += len(count.strip(' '))
    return (line_count, word_count, char_count)
    # END SOLUTION


def eas503_ex36(apr):
    # Complete this function to use a while loop to determine how long it takes for an investment
    # to double at a given interest rate. The input to this function, apr, is the annualized interest rate
    # and the output is the number of years it takes an investment to double. Note: The amount of the initial
    # investment (principal) does not matter; you can use $1.
    # Hint: principal is the amount of money being invested.
    # apr is the annual percentage rate expressed as a decimal number.
    # Relationship: value after one year is given by principal * (1+ apr)

    # BEGIN SOLUTION
    principal = 1
    years = 0
    value = principal
    while value <= principal * 2 :
        value = value * (1 + float(apr))
        years = years + 1
    return years
    # END SOLUTION


def eas503_ex37(n):
    # Complete this function to return the number of steps taken to reach 1 in
    # the Collatz sequence (https://en.wikipedia.org/wiki/Collatz_conjecture) given n

    # BEGIN SOLUTION
    count = 0
    while n != 1:
        count += 1
        if n % 2 == 0:
            n = (n / 2)
        else:
            n = (3 * n + 1)
    return count
    # END SOLUTION


def eas503_ex38(n):
    # A positive whole number > 2 is prime if no number between 2 and sqrt(n)
    # (include) evenly divides n. Write a program that accepts a value of n as
    # input and determine if the value is prime. If n is not prime, your program should
    # return False (boolean) as soon as it finds a value that evenly divides n.
    # Hint: if number is 2, return False

    import math

    # BEGIN SOLUTION
    n = abs(n)
    i = 2
    Flag = 'prime'
    while i <= math.sqrt(n):
        if n % i == 0:
            Flag = 'not prime'
        i += 1
    if n == 2:
        return False
    elif Flag == 'prime':
        return True
    else:
        return False
    # END SOLUTION


def eas503_ex39(n):
    # Complete this function to return all the primes as a list less than or equal to n
    # Input: n
    # Output: a list of numbers
    # hint use ex6

    # BEGIN SOLUTION
    a = [True] * (n + 1)
    primes = []
    for i in range(2, n + 1):
       if a[i]:
          primes.append(i)
          for j in range(i, n + 1, i):
             a[j] = False
    primes.pop(0)
    return primes
    # END SOLUTION


def eas503_ex40(m, n):
    # Complete this function to determine the greatest common divisor (GCD).
    # The GCD of two values can be computed using Euclid's algorithm. Starting with the values
    # m and n, we repeatedly apply the formula: n, m = m, n%m until m is 0. At this point, n is the GCD
    # of the original m and n.
    # Inputs: m and n which are both natural numbers
    # Output: gcd

    # BEGIN SOLUTION
    while m:
        n, m = m, n%m
    return n
    # END SOLUTION


def eas503_ex41(filename):
    # Complete this function to read grades from a file and determine the student with the highest average
    # test grades and the lowest average test grades.
    # Input: filename
    # Output: a tuple containing four elements: name of student with highest average, their average,
    # name of the student with the lowest test grade, and their average. Example ('Student1', 99.50, 'Student5', 65.50)
    # Hint: Round to two decimal places

    # BEGIN SOLUTION
    file = open(filename).read().split('\n')
    lst=[]
    for scores in file:
        scoresplit = (scores.split(','))
        total = 0
        for element in scoresplit:
            if isinstance(element, int) or element.isdigit():
                total += int(element)
        average = round(total / 25, 2)
        lst.append(average)
    lst.pop()
    lowest_test_grade = min(lst)
    highest_test_grade = max(lst)
        
    file1 = open(filename).read().split('\n')
    lst1=[]
    for scores1 in file1:
        scoresplit1 = (scores1.split(','))
        total1 = 0
        for element1 in scoresplit1:
            if isinstance(element1, int) or element1.isdigit():
                total1 += int(element1)
        average1 = round(total1 / 25, 2)
        if(lowest_test_grade == average1):
            last = scoresplit1[0]
            last_avg = average1
        elif(highest_test_grade == average1):
            topper = scoresplit1[0]
            topper_avg = average1
    return (topper, topper_avg, last, last_avg)
    # END SOLUTION


def eas503_ex42(data, num_outliers):
    # When analyzing data collected as a part of a science experiment it
    # may be desirable to remove the most extreme values before performing
    # other calculations. Complete this function which takes a list of
    # values and an non-negative integer, num_outliers, as its parameters.
    # The function should create a new copy of the list with the num_outliers
    # largest elements and the num_outliers smallest elements removed.
    # Then it should return teh new copy of the list as the function's only
    # result. The order of the elements in the returned list does not have to
    # match the order of the elements in the original list.
    # input1: data (list)
    # input2: num_outliers (int)

    # output: list

    # BEGIN SOLUTION
    data.sort()
    data = data[num_outliers:-num_outliers]
    return data
    # END SOLUTION


def eas503_ex43(words):
    # Complete this function to remove duplicates from the words list using a loop
    # input: words (list)
    # output: a list without duplicates
    # MUST USE loop and NOT set!
    # Preserve order

    # BEGIN SOLUTION
    new_list = []
    for word in words:
        if word not in new_list:
            new_list.append(word)
    return new_list
    # END SOLUTION


def eas503_ex44(n):
    # A proper divisor of a  positive integer, n, is a positive integer less than n which divides
    # evenly into n. Complete this function to compute all the proper divisors of a positive
    # integer. The integer is passed to this function as the only parameter. The function will
    # return a list of containing all of the proper divisors as its only result.

    # input: n (int)
    # output: list

    # BEGIN SOLUTION
    lst = []
    for i in range(1,n):
        if(n%i==0):
            lst.append(i)
    return (lst)
    # END SOLUTION


def eas503_ex45(n):
    # An integer, n, is said to be perfect when the sum of all of the proper divisors
    # of n is equal to n. For example, 28 is a perfect number because its proper divisors
    # are 1, 2, 4, 7, and 14 = 28
    # Complete this function to determine if a the number a perfect number or not.
    # input: n (int)
    # output: True or False (bool)

    # BEGIN SOLUTION
    lst = []
    for i in range(1,n):
        if(n%i==0):
            lst.append(i)
    sum1 = 0
    sum1 = sum(lst)
    if(n == sum1):
        return True
    else:
        return False
    # END SOLUTION


def eas503_ex46(points):
    # Complete this function to determine the best line.
    # https://www.varsitytutors.com/hotmath/hotmath_help/topics/line-of-best-fit
    # input: points (list of tuples contain x, y values)
    # output: (m, b) # round both values to two decimal places

    # BEGIN SOLUTION
    alst = []
    blst = []
    for i in range (0,10):
        a = points[i][0]
        alst.append(a)
        b = points[i][1]
        blst.append(b)
    X = sum(alst) / len(alst)
    Y = sum(blst) / len(blst)
    elst = []
    flst = []
    for i in range (0,10):
        c = points[i][0]
        d = points[i][1]
        e = (c - X) * (d - Y)
        g = round(e,2)
        elst.append(g)
        f = pow((c - X),2)
        h = round(f,2)
        flst.append(h)
    E = sum(elst)
    F = round(sum(flst),2)
    m = E / F
    i = round(m,2)
    n = Y - (m * X)
    l = round(n,2)
    return (i,l)
    # END SOLUTION


def eas503_ex47(title, header, data, filename):
    # This problem is hard.
    # Open up ex15_*_solution.txt and look at the output based on the input parameters, which
    # can be found in the test_assignment4.py file
    # Function inputs: 
    # title -- title of the table -- a string
    # header -- header of the table  -- a tuple
    # data -- rows of data, which is a tuple of tuples
    # filename -- name of file to write the table to
    # Your job is to create the table in the file and write it to `filename`
    # Note that you need to dynamically figure out the width of each column based on 
    # maximum possible length based on the header and data. This is what makes this problem hard. 
    # Once you have determined the maximum length of each column, make sure to pad it with 1 space
    # to the right and left. Center align all the values. 
    # OUTPUT: you are writing the table to a file

    # BEGIN SOLUTION
    lst = []
    for name in header:
        lst.append(len(name))
    data_length = len(data)
    count = 0
    while(data_length > count):
        for name in range(len(data[count])):
            num_length = len(str(data[count][name]))
            if(lst[name] < num_length):
                lst[name] = num_length
        count = count + 1
    line = '-' * (sum(lst) + 2 * len(lst) + len(lst) + 1)
    title_column = '|' + f'{title:^{sum(lst) + 2*len(lst) + len(lst) - 1}}' + '|'
    line_seperator = ''
    row_seperator = ''
    for x in range(len(lst)):
        line_seperator = line_seperator + '+' + '-' * (lst[x]+2)
    count = 0
    while(data_length > count):
        for name in range(len(data[count])):
            row_seperator = row_seperator + '|' + ' ' + f'{data[count][name]:^{lst[name]}}' + ' '
        if(count != len(data) - 1):
            row_seperator = row_seperator + '|' + '\n'
        else:
            row_seperator = row_seperator + '|'
        count = count + 1
    header_seperator = ''
    for name in range(len(header)):
        header_seperator += '|' + ' ' + f'{header[name]:^{lst[name]}}' + ' '
    header_seperator += '|'
    file_content = line + '\n' + title_column + '\n' + line_seperator + '+' + '\n' + header_seperator + '\n' + line_seperator + '+' + '\n' + row_seperator + '\n' + line_seperator + '+'
    with open(filename, 'w') as file:
        file.write(file_content)
    # END SOLUTION

def eas503_ex48(filename):
    """
    In this problem you will read data from a file and perform a simple mathematical operation on each data point. 
    Each line is supposed to contain a floating point number.
    But what you will observe is that some lines might have erroneous entries. 
    You need to ignore those lines (Hint: Use Exception handling).

    The idea is to implement a function which reads in a file and computes the median 
    of the numbers and returns the output. You may use the inbuilt function sort when computing the median.

    DO NOT USE ANY INBUILT OR OTHER FUNCTION TO DIRECTLY COMPUTE MEDIAN

    """
    ### BEGIN SOLUTION
    file = open(filename).readlines()
    res = []
    lst = []
    for ele in file:
        try:
            b = float(ele)
            lst.append(b)
        except ValueError:
            res.append(ele)
    n = len(lst)
    lst.sort()
    if(n == 0):
        return f'The file does not have any valid number to compute the median'
    else:
        if n % 2 == 0:
            median1 = lst[n//2]
            median2 = lst[n//2 - 1]
            median = (median1 + median2)/2
        else:
            median = lst[n//2]
    return median
    ### END SOLUTION