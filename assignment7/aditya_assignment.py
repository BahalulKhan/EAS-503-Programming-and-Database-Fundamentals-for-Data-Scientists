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
    conn=create_connection(non_normalized_db_filename)
    df_degrees=pd.read_sql_query("SELECT DISTINCT Degree from Students",conn)
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
    conn=create_connection(non_normalized_db_filename)
    df=pd.read_sql_query("SELECT Exams From Students",conn)
    df_exams = df["Exams"].str.split(",", expand=True).stack().reset_index(level=1, drop=True).to_frame(name="Exam")
    df_exams["Year"] = df_exams["Exam"].str.extract(r"\((\d{4})\)")
    df_exams["Year"] = pd.to_numeric(df_exams["Year"])
    df_exams["Exam"] = df_exams["Exam"].str.extract(r"^([\w\s]+)")
    df_exams = df_exams.dropna()
    df_exams["Exam"] = df_exams["Exam"].str.strip()
    df_exams = df_exams.drop_duplicates()
    df_exams = df_exams.sort_values("Exam")
    df_exams = df_exams.reset_index(drop=True)
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
    conn=create_connection(non_normalized_db_filename)
    df=pd.read_sql_query("SELECT StudentID,Name,Degree From Students",conn)
    df[['Last_Name', 'First_Name']] = df['Name'].str.split(',', expand=True)
    df['First_Name'] = df['First_Name'].str.strip()
    df['Last_Name'] = df['Last_Name'].str.strip()
    df = df.drop(columns=['Name'])
    df['StudentID'] = pd.to_numeric(df['StudentID'])
    df_students = df[['StudentID', 'First_Name', 'Last_Name', 'Degree']]
    return df_students

    # END SOLUTION


def create_df_studentexamscores(non_normalized_db_filename, df_students):
    """
    Open connection to the non-normalized database and generate a 'df_studentexamscores' dataframe that 
    contains StudentID, exam and score
    See screenshot below. 
    """

    # BEGIN SOLUTION
    conn=create_connection(non_normalized_db_filename)
    df=pd.read_sql_query("SELECT Exams,Scores From Students",conn)

    scoreslist = []

    for index, row in df.iterrows():
        exams = [s.strip().split()[0] for s in row['Exams'].split(',')]
        scores = row['Scores'].split(',')
        for i in range(len(exams)):
            scoreslist.append((index+1, exams[i], int(scores[i])))
    df_studentexamscores = pd.DataFrame(scoreslist, columns=['StudentID', 'Exam', 'Score'])
    return  df_studentexamscores 
    # END SOLUTION


def ex1(df_exams):
    """
    return df_exams sorted by year
    """
    # BEGIN SOLUTION
    return df_exams.sort_values('Year')
    # END SOLUTION


def ex2(df_students):
    """
    return a df frame with the degree count
    # NOTE -- rename name the degree column to Count!!!
    """
    # BEGIN SOLUTION
    count= df_students['Degree'].value_counts().rename('Count')
    df = pd.DataFrame({'Degree': count.index, 'Count': count.values})
    df = df.set_index('Degree')
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

    merged_df = pd.merge(df_studentexamscores, df_exams, on='Exam', how='left')
    df = merged_df.groupby(['Exam','Year']).mean()
    df = df.sort_values(by='Score', ascending=False).round(2)
    df = df.reset_index().rename(columns={'Score': 'average'})
    df = df[['Exam','Year','average']]
    df['Year'] = df['Year'].astype(int)
    df=df.set_index('Exam')
    return df
    # END SOLUTION
    


def ex4(df_studentexamscores, df_students):
    """
    return a datafram that merges df_studentexamscores and df_students and finds the average of the degrees. Sort
    the average in descending order. See screenshot below of the output. You have to fix up the column/index names.
    Hints:
    # https://stackoverflow.com/a/45451905
    # https://stackoverflow.com/a/11346337
    # round to two decimal places
    """

    # BEGIN SOLUTION
    df_merge = pd.merge(df_studentexamscores, df_students, on='StudentID')
    df = df_merge.groupby('Degree')['Score'].mean().reset_index(name='Average')
    df['Average'] = df['Average'].round(2)
    df = df.sort_values('Average', ascending=False).reset_index(drop=True)
    df = df.rename(columns={'Degree': 'Degree', 'Average': 'Average'})
    df=df[['Degree','Average']]
    df=df.set_index('Degree')
    return df
    # END SOLUTION


def ex5(df_studentexamscores, df_students):
    """
    merge df_studentexamscores and df_students to produce the output below. The output shows the average of the top 
    10 students in descending order. 
    Hint: https://stackoverflow.com/a/20491748
    round to two decimal places

    """

    # BEGIN SOLUTION
    df = pd.merge(df_studentexamscores, df_students, on='StudentID')
    df = df.groupby(['First_Name', 'Last_Name', 'Degree'])['Score'].mean().reset_index()
    df = df.rename(columns={'Score': 'Average'})
    df = df.sort_values(['Average', 'Degree'], ascending=[False, False])
    df['Average'] = df['Average'].round(2)
    df = df[['First_Name', 'Last_Name', 'Degree', 'Average']]
    return df.head(10)
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
    username=[]
    firstname=[]
    lastname=[]
    for i in range(100):
        fullname=fake.name()
        first_name,last_name=fullname.split(" ",1)
        user_name = first_name[:2].lower() + str(np.random.randint(1000, 9999))
        username.append(user_name)
        firstname.append(first_name)
        lastname.append(last_name)
    df = pd.DataFrame({
    'username': username,
    'first_name': firstname,
    'last_name': lastname
})
    return df

    # END SOLUTION
    


def part2_step2():

    # ---- DO NOT CHANGE
    np.random.seed(0)
    # ---- DO NOT CHANGE


    # BEGIN SOLUTION
    scorestable = [
        ('Hw1', 35, 9, 50),
        ('Hw2', 75, 15, 100),
        ('Hw3', 25, 7, 40),
        ('Hw4', 45, 10, 60),
        ('Hw5', 45, 5, 50),
        ('Exam1', 75, 20, 100),
        ('Exam2', 25, 8, 50),
        ('Exam3', 45, 9, 60),
        ('Exam4', 35, 10, 50)
    ]

    scores = np.clip(np.round(np.random.normal(loc=[y[1] for y in scorestable],scale=[y[2] for y in scorestable],size=(100, len(scorestable)))),0,[y[3] for y in scorestable])
    df = pd.DataFrame(scores, columns=[item[0] for item in scorestable])
    return df

    # END SOLUTION


def part2_step3(df2_scores):
    # BEGIN SOLUTION
    scorestable = [
        ('Hw1', 35, 9, 50),
        ('Hw2', 75, 15, 100),
        ('Hw3', 25, 7, 40),
        ('Hw4', 45, 10, 60),
        ('Hw5', 45, 5, 50),
        ('Exam1', 75, 20, 100),
        ('Exam2', 25, 8, 50),
        ('Exam3', 45, 9, 60),
        ('Exam4', 35, 10, 50)
    ]
    dfvalues=part2_step2()
    theovalues=dfvalues.describe().round(2)
    mean=theovalues.loc['mean']
    std=theovalues.loc['std']
    df = pd.DataFrame({'mean':mean,'std':std,'mean_theoritical': [y[1] for y in scorestable], 'std_theoritical':[y[2] for y in scorestable],'abs_mean_diff':abs(mean-[y[1] for y in scorestable]),'abs_std_diff':abs(std-[y[2] for y in scorestable])}).round(2)
    return df
    # END SOLUTION


def part2_step4(df2_students, df2_scores, ):
    # BEGIN SOLUTION
        max_scores = {
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

        scaled_scores = (int(df2_scores) / pd.Series(max_scores)).mul(100).round()
        df_combined = pd.concat([df2_students, scaled_scores], axis=1)

        return df_combined
            # END SOLUTION


def part2_step5():
    # BEGIN SOLUTION
   
    df = pd.read_csv('part2_step5-input.csv')
    df['AI_Count'] = 0
    for index, row in df.iterrows():
        for x in list(row):
            if x =='AI_ISSUE':
                df.at[index, 'AI_Count'] += 1
    df_filtered = df[df['AI_Count'] > 0]
    df = df_filtered[['username', 'first_name', 'last_name', 'AI_Count']]
    df = df.reset_index(drop=True)
    return df
        # END SOLUTION


def part2_step6():
    # BEGIN SOLUTION
    df = pd.read_csv('part2_step5-input.csv')
    df.replace('AI_ISSUE', 0, inplace=True)
    homeworkcolumns = ['Hw1', 'Hw2', 'Hw3', 'Hw4', 'Hw5']
    df[homeworkcolumns] = df[homeworkcolumns].astype(float)
    df[homeworkcolumns] = df[homeworkcolumns].apply(lambda x: x.fillna(round(x.mean())), axis=1)
    examcolumns = ['Exam1', 'Exam2', 'Exam3', 'Exam4']
    df[examcolumns] = df[examcolumns].astype(float)
    df[examcolumns] = df[examcolumns].apply(lambda x: x.fillna(round(x.mean())), axis=1)
    homeworkweights = np.repeat(0.05, len(homeworkcolumns))
    examweights = np.array([0.2, 0.2, 0.2, 0.15])
    df['Grade'] = ((df[homeworkcolumns] * homeworkweights).sum(axis=1) + (df[examcolumns] * examweights).sum(axis=1)).round()
    df['LetterGrade'] = df['Grade'].apply(lambda grade: 'A' if grade >= 80 else
                                        'B' if grade >= 70 else
                                        'C' if grade >= 50 else
                                        'D' if grade >= 40 else 'F')
    numericcolumns = df.select_dtypes(include='number')
    meanrow = numericcolumns.mean().round()
    meanrow.name = 'mean'
    stdrow = numericcolumns.std().round()
    stdrow.name = 'std'

    df = pd.concat([df, pd.DataFrame([meanrow, stdrow])], axis=0)
    return df

        # END SOLUTION
