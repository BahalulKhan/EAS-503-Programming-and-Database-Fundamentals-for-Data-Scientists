import sqlite3

import numpy as np
import pandas as pd
from faker import Faker


def create_connection(db_file, delete_db=False):
    import os
    if delete_db and os.path.exists(db_file):
        os.remove(db_file)

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = 1")
    except sqlite3.Error as e:
        print(e)

    return conn


conn = create_connection('non_normalized.db')
sql_statement = "select * from Students;"
df = pd.read_sql_query(sql_statement, conn)
print(df)


def create_df_degrees(non_normalized_db_filename):
    """
    Open connection to the non-normalized database and generate a 'df_degrees' dataframe that contains only
    the degrees. See screenshot below. 
    """

    # BEGIN SOLUTION
    conn_non_normalized = create_connection(non_normalized_db_filename)
    sql_statement = "SELECT DISTINCT Degree from Students;"
    df_degrees = pd.read_sql_query(sql_statement,conn_non_normalized)
    return df_degrees
    # END SOLUTION


def create_df_exams(non_normalized_db_filename):
    """
    Open connection to the non-normalized database and generate a 'df_exams' dataframe that contains only
    the exams. See screenshot below. Sort by exam!
    hints:
    # https://stackoverflow.com/a/16476974
    # https://stackoverflow.com/a/36108422
    """

    # BEGIN SOLUTION
    conn_non_normalized=create_connection(non_normalized_db_filename)
    sql_statement = "SELECT Exams From Students;"
    df=pd.read_sql_query(sql_statement,conn_non_normalized)
    df_exams = df["Exams"].str.split(",", expand=True)
    df_exams = df_exams.stack().reset_index(level=1, drop=True).to_frame(name="Exam")
    df_exams["Year"] = df_exams["Exam"].str.split("(", expand=True)[1].str.rstrip(")")
    df_exams["Year"] = pd.to_numeric(df_exams["Year"])
    df_exams["Exam"] = df_exams["Exam"].str.split("(", n=1).str[0]
    df_exams["Exam"] = df_exams["Exam"].str.strip()
    df_exams = df_exams[~df_exams["Exam"].isnull()]
    df_exams = df_exams.drop_duplicates().sort_values("Exam", ignore_index=True)
    return df_exams
    # END SOLUTION


def create_df_students(non_normalized_db_filename):
    """
    Open connection to the non-normalized database and generate a 'df_students' dataframe that contains the student
    first name, last name, and degree. You will need to add another StudentID column to do pandas merge.
    See screenshot below. 
    You can use the original StudentID from the table. 
    hint: use .split on the column name!
    """

    # BEGIN SOLUTION
    conn_non_normalized=create_connection(non_normalized_db_filename)
    sql_statement = "SELECT StudentID, Name, Degree FROM Students;"
    df=pd.read_sql_query(sql_statement,conn_non_normalized)
    df[['Last_Name', 'First_Name']] = df['Name'].str.extract(r'^([^,]+),\s*(.*)$')
    df = df[['StudentID', 'First_Name', 'Last_Name', 'Degree']]
    return df
    # END SOLUTION


def create_df_studentexamscores(non_normalized_db_filename, df_students):
    """
    Open connection to the non-normalized database and generate a 'df_studentexamscores' dataframe that 
    contains StudentID, exam and score
    See screenshot below. 
    """

    # BEGIN SOLUTION
    import re


    conn_non_normalized=create_connection(non_normalized_db_filename)
    sql_statement = "SELECT Exams,Scores From Students;"
    df=pd.read_sql_query(sql_statement,conn_non_normalized)
    Output = []
    index = 0
    while index < len(df):
        row = df.iloc[index]
        exams = [re.search(r'\b(\w+)\b', s.strip()).group(1) for s in row['Exams'].split(',')]
        scores = [int(score.strip()) for score in row['Scores'].split(',')]
        i = 0
        while i < len(exams):
            Output.append((index + 1, exams[i], scores[i]))
            i += 1
        index += 1
    df_studentexamscores = pd.DataFrame(Output, columns=['StudentID', 'Exam', 'Score'])
    return  df_studentexamscores
    # END SOLUTION


def ex1(df_exams):
    """
    return df_exams sorted by year
    """
    # BEGIN SOLUTION
    return df_exams.sort_values('Year')
    # END SOLUTION
    return df_exams


def ex2(df_students):
    """
    return a df frame with the degree count
    # NOTE -- rename name the degree column to Count!!!
    """
    # BEGIN SOLUTION
    Output = df_students.copy()
    Output = pd.DataFrame(Output.values, columns=Output.columns)
    graduate_students = Output[Output['Degree'] == 'graduate'].shape[0]
    undergraduate_students = Output[Output['Degree'] != 'graduate'].shape[0]
    Stu_count = [[undergraduate_students], [graduate_students]]
    df = pd.DataFrame(data=Stu_count, index=['undergraduate', 'graduate'], columns=['Count'])
    # END SOLUTION
    return df


def ex3(df_studentexamscores, df_exams):
    """
    return a datafram that merges df_studentexamscores and df_exams and finds the average of the exams. Sort
    the average in descending order. See screenshot below of the output. You have to fix up the column/index names.
    Hints:
    # https://stackoverflow.com/a/45451905
    # https://stackoverflow.com/a/11346337
    # round to two decimal places
    """

    # BEGIN SOLUTION
    df_merged = df_studentexamscores.merge(df_exams, on='Exam')
    df_grouped = df_merged.groupby(['Exam', 'Year']).mean()
    df_pivot = pd.DataFrame(df_grouped['Score'].round(2))
    df_pivot.columns = ['average']
    df_pivot.reset_index(inplace=True)
    df_pivot.sort_values(by='average', ascending=False, inplace=True)
    df = df_pivot[['Exam', 'Year', 'average']].copy()
    df.set_index('Exam', inplace=True)
    df = df[['Year', 'average']]
    # END SOLUTION
    return df


def ex4(df_studentexamscores, df_students):
    """
    return a datafram that merges df_studentexamscores and df_exams and finds the average of the degrees. Sort
    the average in descending order. See screenshot below of the output. You have to fix up the column/index names.
    Hints:
    # https://stackoverflow.com/a/45451905
    # https://stackoverflow.com/a/11346337
    # round to two decimal places
    """
    
    # BEGIN SOLUTION
    df_merged = df_studentexamscores.merge(df_students[['StudentID', 'Degree']], on='StudentID')
    df_grouped = df_merged.groupby('Degree')['Score'].agg('mean')
    df = pd.DataFrame({'Average': df_grouped}).round(2)
    # END SOLUTION
    return df


def ex5(df_studentexamscores, df_students):
    """
    merge df_studentexamscores and df_students to produce the output below. The output shows the average of the top 
    10 students in descending order. 
    Hint: https://stackoverflow.com/a/20491748
    round to two decimal places

    """
    # BEGIN SOLUTION
    df_grouped = df_studentexamscores.pivot_table(index='StudentID', values='Score', aggfunc='mean')
    df_merged = df_students.set_index('StudentID').join(df_grouped, on='StudentID')
    df_sorted = df_merged.sort_values('Score', ascending=False)
    df_top10 = df_sorted.head(10)
    df_top10_renamed = df_top10.rename(columns={'Score': 'Average'})
    df = df_top10_renamed.round({'Average': 2})
    return df
    # END SOLUTION


# DO NOT MODIFY THIS CELL OR THE SEED

# THIS CELL IMPORTS ALL THE LIBRARIES YOU NEED!!!


np.random.seed(0)
fake = Faker()
Faker.seed(0)


def part2_step1():

    # ---- DO NOT CHANGE
    np.random.seed(0)
    fake = Faker()
    Faker.seed(0)
    # ---- DO NOT CHANGE

    # BEGIN SOLUTION
    Output = []
    counter = 0
    while counter < 100:
        name_details = fake.name()
        first_name = name_details.split(" ", 1)[0]
        last_name = name_details.split(" ", 1)[1]
        username = first_name[:2].lower() + str(np.random.randint(1000, 9999))
        Output.append((username, first_name, last_name))
        counter += 1
    df = pd.DataFrame(Output, columns=['username', 'first_name', 'last_name'])
    return df
    
    # END SOLUTION
    

def part2_step2():

    # ---- DO NOT CHANGE
    np.random.seed(0)
    # ---- DO NOT CHANGE

    # BEGIN SOLUTION
    std_max_mean = [
            (9, 50, 35),
            (15, 100, 75),
            (7, 40, 25),
            (10, 60, 45),
            (5, 50, 45),
            (20, 100, 75),
            (8, 50, 25),
            (9, 60, 45),
            (10, 50, 35)
        ]
    scores = []
    counter = 0
    while counter < 100:
        score = []
        for std, max_score, mean in std_max_mean:
            score.append(np.round_(np.clip(np.random.normal(mean, std), 0, max_score)))
        scores.append(score)
        counter += 1
    column_names = ['Hw1', 'Hw2', 'Hw3', 'Hw4', 'Hw5', 'Exam1', 'Exam2', 'Exam3', 'Exam4']
    df = pd.DataFrame(scores, columns=column_names)
    return df
    # END SOLUTION


def part2_step3(df2_scores):
    # BEGIN SOLUTION
    mean_theoretical = [35, 75, 25, 45, 45, 75, 25, 45, 35]
    std_theoretical = [9, 15, 7, 10, 5, 20, 8, 9, 10]
    mean_values = []
    std_values = []
    abs_mean_diff = []
    abs_std_diff = []
    columns = df2_scores.columns
    num_columns = len(columns)
    i = 0
    while i < num_columns:
        column_mean = df2_scores[columns[i]].mean()
        column_std = df2_scores[columns[i]].std()
        mean_values.append(round(column_mean, 2))
        std_values.append(round(column_std, 2))
        mean_diff = abs(column_mean - mean_theoretical[i])
        std_diff = abs(column_std - std_theoretical[i])
        abs_mean_diff.append(round(mean_diff, 2))
        abs_std_diff.append(round(std_diff, 2))
        i += 1
    df = pd.DataFrame({
        'mean': mean_values,
        'std': std_values,
        'mean_theoretical': mean_theoretical,
        'std_theoretical': std_theoretical,
        'abs_mean_diff': abs_mean_diff,
        'abs_std_diff': abs_std_diff
    }, index=columns)
    return df
    # END SOLUTION


import pandas as pd

def part2_step4(df2_students, df2_scores):
    # Define the maximum scores for each assignment/exam
    max_score = {
        'Hw1': 50,
        'Hw2': 100,
        'Hw3': 40,
        'Hw4': 60,
        'Hw5': 50,
        'Exam1': 100,
        'Exam2': 50,
        'Exam3': 60,
        'Exam4': 50
    }
    scaled_scores = df2_scores.divide(list(max_score.values())).multiply(100).round()
    column_names = ['Hw1', 'Hw2', 'Hw3', 'Hw4', 'Hw5', 'Exam1', 'Exam2', 'Exam3', 'Exam4']
    column_order = ['username', 'first_name', 'last_name'] + column_names
    df_combined = pd.DataFrame()
    df_combined[column_order[:3]] = df2_students[column_order[:3]]
    df_combined[column_names] = scaled_scores[column_names]
    return df_combined
    # END SOLUTION


def part2_step5():
    # BEGIN SOLUTION
    import pandas as pd
    df = pd.read_csv('part2_step5-input.csv')
    df['AI_Count'] = df.apply(lambda row: row.tolist().count('AI_ISSUE'), axis=1)
    df_filtered = df[df['AI_Count'] > 0]
    df = df_filtered[['username', 'first_name', 'last_name', 'AI_Count']]
    df = df.reset_index(drop=True)
    return df
    # END SOLUTION


def part2_step6():
    # BEGIN SOLUTION
    df = pd.read_csv('part2_step5-input.csv')
    df.replace('AI_ISSUE', 0, inplace=True)
    Hw = ['Hw1', 'Hw2', 'Hw3', 'Hw4', 'Hw5']
    Exam = ['Exam1', 'Exam2', 'Exam3', 'Exam4']
    df[Hw] = df[Hw].astype(float)
    df[Hw] = df[Hw].apply(lambda Hw_marks: Hw_marks.fillna(round(Hw_marks.mean())), axis=1)
    df[Exam] = df[Exam].astype(float)
    df[Exam] = df[Exam].apply(lambda Exam_marks: Exam_marks.fillna(round(Exam_marks.mean())), axis=1)
    Hw_weightage = [0.05] * len(Hw)
    Exam_weightage = [0.2, 0.2, 0.2, 0.15]
    hw_grade = df[Hw].multiply(Hw_weightage, axis=1)
    exam_grade = df[Exam].multiply(Exam_weightage, axis=1)
    df['Grade'] = (hw_grade.apply(lambda row: row.sum(), axis=1) + exam_grade.apply(lambda row: row.sum(), axis=1)).round()
    df['LetterGrade'] = ''
    for index, row in df.iterrows():
        grade = row['Grade']
        if grade >= 80:
            df.at[index, 'LetterGrade'] = 'A'
        elif grade >= 70:
            df.at[index, 'LetterGrade'] = 'B'
        elif grade >= 50:
            df.at[index, 'LetterGrade'] = 'C'
        elif grade >= 40:
            df.at[index, 'LetterGrade'] = 'D'
        else:
            df.at[index, 'LetterGrade'] = 'F'
    numeric_columns = [col for col in df.columns if df[col].dtype in ['int64', 'float64']]
    mean_row = df[numeric_columns].apply(lambda x: round(x.mean()), axis=0)
    mean_row.name = 'mean'
    std_row = df[numeric_columns].apply(lambda x: round(x.std()), axis=0)
    std_row.name = 'std'
    df.loc['mean'] = mean_row
    df.loc['std'] = std_row
    return df
    # END SOLUTION
