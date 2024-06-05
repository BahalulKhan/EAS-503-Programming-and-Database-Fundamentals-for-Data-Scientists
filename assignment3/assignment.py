def eas503_ex49(filename):
    # Complete this function to read grades from `filename` and find the minimum
    # student test averages. File has student_name, test1_score, test2_score,
    # test3_score, test4_score, test5_score. This function must use a lambda
    # function and use the min() function to find the student with the minimum
    # test average. The input to the min function should be
    # a list of lines. Ex. ['student1,33,34,35,36,45', 'student2,33,34,35,36,75']
    # input filename
    # output: (lambda_func, line_with_min_student) -- example (lambda_func, 'student1,33,34,35,36,45')

    # BEGIN SOLUTION
    file = open(filename).read().split('\n')
    Students = [ele for ele in file if ele.strip()]
    lambda_func = lambda ele: sum(map(int, ele.split(',')[1:])) / 5
    line_with_min_student = min(Students, key=lambda_func)
    return (lambda_func, line_with_min_student)
    # END SOLUTION


def eas503_ex50(filename):
    # Complete this function to read grades from `filename` and map the test average to letter
    # grades using map and lambda. File has student_name, test1_score, test2_score,
    # test3_score, test4_score, test5_score. This function must use a lambda
    # function and map() function.
    # The input to the map function should be
    # a list of lines. Ex. ['student1,73,74,75,76,75', ...]. Output is a list of strings in the format
    # studentname: Letter Grade -- 'student1: C'
    # input filename
    # output: (lambda_func, list_of_studentname_and_lettergrade) -- example (lambda_func, ['student1: C', ...])

    # Use this average to do the grade mapping. Round the average grade.
    # D = 65<=average<70
    # C = 70<=average<80
    # B = 80<=average<90
    # A = 90<=average
    # Define a function that takes in a number grade and returns the letter grade and use
    # it inside the lambda function.
    # HINT: create a function

    # BEGIN SOLUTION
    file = open(filename).read().split('\n')
    Students = [ele for ele in file if ele.strip()]
    lambda_func = lambda ele: ele.split(',')[0] + ': ' + grade_mapping(sum(map(int, ele.split(',')[1:])) / 5)
    list_of_studentname_and_lettergrade = list(map(lambda_func, Students))
    return (lambda_func, list_of_studentname_and_lettergrade)
def grade_mapping(average):
    rounded_average = round(average)
    if rounded_average >= 90:
        return 'A'
    elif rounded_average >= 80:
        return 'B'
    elif rounded_average >= 70:
        return 'C'  
    elif rounded_average >= 65:
        return 'D'
    else:
        return 'F'
    # END SOLUTION


def eas503_ex51(filename):
    # Complete this function to sort a list of dictionary by 'test3'
    # return the lambda function and the sorted list of dictionaries
    # Use the following code to read JSON file

    import json
    with open(filename) as infile:
        grades = json.load(infile)

    # BEGIN SOLUTION
    lambda_func = lambda ele: int(ele['test3'])
    sorted_list = sorted(grades, key=lambda_func)
    return (lambda_func, sorted_list)
    # END SOLUTION


def eas503_ex52(lst):
    # Complete this function to use list comprehension to return all values from `lst`
    # that are a multiple of 3 or 4. Just complete the list comprehension below.
    # input: `lst` of numbers
    # output: a list of numbers

    # BEGIN SOLUTION
    # complete the following line!
    numbers = [ele for ele in lst if (ele % 3 == 0 or ele % 4 == 0)]
    return numbers
    # END SOLUTION


def eas503_ex53(lst):
    # Complete this function to use list comprehension to multiple all numbers
    # in the list by 3 if it is even or 5 if its odd
    # input: `lst` of numbers
    # output: a list of numbers

    # BEGIN SOLUTION
    # complete the following line!
    numbers = [(ele * 3) if (ele % 2 == 0) else (ele * 5) for ele in lst]
    return numbers
    # END SOLUTION


def eas503_ex54(input_dict, test_value):
    # Complete this function to find all the keys in a dictionary that map to the input value.
    # input1: input_dict (dict)
    # input2: test_value
    # output: list of keys

    # BEGIN SOLUTION
    list_of_keys = []
    for key, value in input_dict.items():
        if value == test_value:
            list_of_keys.append(key)
    return list_of_keys
    # END SOLUTION
