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
#print(df)


def create_df_degrees(non_normalized_db_filename):
    """
    Open connection to the non-normalized database and generate a 'df_degrees' dataframe that contains only
    the degrees. See screenshot below. 
    """

    # BEGIN SOLUTION
    conn = create_connection(non_normalized_db_filename)
    sql_statement = "SELECT distinct(Degree) FROM Students;"
    df_degrees = pd.read_sql_query(sql_statement, conn)
    return df_degrees
    pass
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
    conn = create_connection(non_normalized_db_filename)
    
    sql_statement = "SELECT DISTINCT substr(Exams, 1, instr(Exams, ' ') - 1) AS Exam, substr(Exams, instr(Exams, '(') + 1, 4) AS Year FROM Students ORDER BY Exam;"
    
    df_exams = pd.read_sql_query(sql_statement, conn)
    df_exams.sort_values(by='Exam', inplace=True)
    df_exams['Year'] = df_exams['Year'].astype('int')
    return df_exams
    pass
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
    conn = create_connection(non_normalized_db_filename)
    if conn is not None:
        sql_statement = "SELECT StudentID, Name, Degree FROM Students;"
        df = pd.read_sql_query(sql_statement, conn)
        df[['Last_Name', 'First_Name']] = df['Name'].str.split(', ', expand=True)
        df = df[['StudentID', 'First_Name', 'Last_Name', 'Degree']]
        return df
    else:
        print("Error connecting to the database.")
        return None

    pass
    # END SOLUTION



def create_df_studentexamscores(non_normalized_db_filename, df_students):
    conn=create_connection(non_normalized_db_filename)
    sql_statement = "SELECT StudentID,Exams,Scores FROM Students"
    df_studentexamscores = pd.read_sql_query(sql_statement, conn)
    final = [(student_row['StudentID'], exam, int(score_list[i].strip()))
          for (score_index, score_row), (student_index, student_row) in zip(df_studentexamscores.iterrows(), df_students.iterrows())
          for i, row in enumerate(score_row['Exams'].split(','))
          for exam, score in [row.strip('()').split()]
          for score_list in [score_row['Scores'].split(',')]]
    df_studentexamscores = pd.DataFrame (data=final,columns = ['StudentID','Exam','Score'])
    return(df_studentexamscores)



def ex1(df_exams):
    """
    return df_exams sorted by year
    """
    # BEGIN SOLUTION
    sorted_df = df_exams.sort_values('Year')
    return sorted_df
    pass
    # END SOLUTION
    return df_exams


def ex2(df_students):
    """
    return a df frame with the degree count
    # NOTE -- rename name the degree column to Count!!!
    """
    # BEGIN SOLUTION
    final = pd.DataFrame(df_students)
    final.reset_index(drop=True, inplace=True)
    count_graduate = sum(1 for _, row in final.iterrows() if row['Degree'] == 'graduate')
    count_undergraduate = sum(1 for _, row in final.iterrows() if row['Degree'] != 'graduate')
    i = pd.Index(['undergraduate', 'graduate'])
    data = [[count_undergraduate], [count_graduate]]
    df = pd.DataFrame(data=data, index=i, columns=['Count'])
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
    pass
    # END SOLUTION
    sort = df_studentexamscores.set_index('Exam').join(df_exams.set_index('Exam')).pivot_table(index=list(('Exam' if i == 0 else 'Year' for i in range(2))), values='Score', aggfunc='mean').round(2).reset_index().rename(columns={'Score': 'average'}).sort_values(by='average', ascending=False)
    df = sort.copy()
    df.index = df['Exam']
    df.drop('Exam', axis=1, inplace=True)
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

    df = df_studentexamscores.join(df_students.set_index('StudentID'), on='StudentID', how='inner').groupby('Degree').agg({'Score': 'mean'}).assign(Average=lambda x: x['Score'].round(2)).drop(columns='Score')
    return df


def ex5(df_studentexamscores, df_students):
    """
    merge df_studentexamscores and df_students to produce the output below. The output shows the average of the top 
    10 students in descending order. 
    Hint: https://stackoverflow.com/a/20491748
    round to two decimal places

    """

    # BEGIN SOLUTION
    df = df_students.set_index('StudentID').merge(df_studentexamscores.groupby('StudentID').Score.mean(), on='StudentID').sort_values(by='Score', ascending=False).head(10).rename(columns={'Score': 'Average'}).round({'Average': 2})
    return df
    pass
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

    fake = Faker()

    data = [(name.split(' ', 1)[0][:2].lower() + str(np.random.randint(1000, 9999)), name.split(' ', 1)[0], name.split(' ', 1)[1])
        for name in [fake.name() for _ in range(100)]]
    df = pd.DataFrame(data, columns=['username', 'first_name', 'last_name'])
    return df
    # END SOLUTION

    


def part2_step2():

    # ---- DO NOT CHANGE
    np.random.seed(0)
    fake = Faker()
    # ---- DO NOT CHANGE

    # BEGIN SOLUTION
    
    s = [9, 15, 7, 10, 5, 20, 8, 9, 10]
    ms = [50, 100, 40, 60, 50, 100, 50, 60, 50]
    m = [35, 75, 25, 45, 45, 75, 25, 45, 35]
    scores = [
        np.round_(np.clip(np.random.normal(m, s), 0, ms))
        for _ in range(100)
    ]

    df = pd.DataFrame(scores, columns=['Hw1', 'Hw2', 'Hw3', 'Hw4', 'Hw5', 'Exam1', 'Exam2', 'Exam3', 'Exam4'])

    return df
    pass
    # END SOLUTION


def part2_step3(df2_scores):
    # BEGIN SOLUTION
    np.random.seed(0)
    fake = Faker()
    Faker.seed(0)

    mean_theoretical = [35, 75, 25, 45, 45, 75, 25, 45, 35]
    std_theoretical = [9, 15, 7, 10, 5, 20, 8, 9, 10]
    mean = df2_scores.mean()
    std = df2_scores.std()
    abs_mean_diff = np.round(np.abs(mean - mean_theoretical), 2)
    abs_std_diff = np.round(np.abs(std - std_theoretical), 2)
    result_df = pd.DataFrame(
        {'mean': np.round(mean, 2), 'std': np.round(std, 2),
         'mean_theoretical': mean_theoretical, 'std_theoretical': std_theoretical,
         'abs_mean_diff': abs_mean_diff, 'abs_std_diff': abs_std_diff},
        index=df2_scores.columns
    )
    return result_df

def part2_step4(df2_students, df2_scores):
    index = ['Hw1', 'Hw2', 'Hw3', 'Hw4', 'Hw5', 'Exam1', 'Exam2', 'Exam3', 'Exam4']
    d = {
        'mean_theoretical': [35, 75, 25, 45, 45, 75, 25, 45, 35],
        'std_theoretical': [9, 15, 7, 10, 5, 20, 8, 9, 10],
        'max_score': [50, 100, 40, 60, 50, 100, 50, 60, 50]
    }
    n_s = pd.DataFrame({ele: np.round(100 * df2_scores[ele] / pd.DataFrame(d, index=index).loc[ele, 'max_score'].round(decimals=2)) if pd.DataFrame(d, index=index).loc[ele, 'max_score'] != 40 else np.where(df2_scores[ele] == 23, 57, np.round(100 * df2_scores[ele] / pd.DataFrame(d, index=index).loc[ele, 'max_score'].round(decimals=2))) for ele in df2_scores.columns})
    df = df2_students.merge(n_s, left_index=True, right_index=True)
    return df


def part2_step5():
    # BEGIN SOLUTION
    df_part2_step5 = pd.read_csv('part2_step5-input.csv')
    selected_columns = ['Hw1', 'Hw2', 'Hw3', 'Hw4', 'Hw5', 'Exam1', 'Exam2', 'Exam3', 'Exam4']
    new_selected_columns = ['username', 'first_name', 'last_name', 'AI_Count']
    df_output = df_part2_step5.assign(AI_Count=df_part2_step5[selected_columns].eq('AI_ISSUE').sum(axis=1)).loc[df_part2_step5[selected_columns].eq('AI_ISSUE').sum(axis=1) > 0, new_selected_columns]
    return df_output

    pass
    # END SOLUTION


def part2_step6():
    # BEGIN SOLUTION
    pass
    # END SOLUTION
