import pandas as pd

# Read the following link and complete this homework. https://www.codemag.com/Article/1711091/Implementing-Machine-Learning-Using-Python-and-Scikit-learn

# Make sure to install scikit-learn and Pandas

def step1():
    """
    # Step 1: Getting the Titanic Dataset
    Return a dataframe containing the Titantic dataset from the following URL
    # URL: https://gist.githubusercontent.com/mkzia/aa4f293661dba857b8c4459c0095ac95/raw/8075037f6f7689a1786405c1bc8ea9471d3aa9c3/train.csv

    """
    # BEGIN SOLUTION
    Titanic_Dataset=pd.read_csv("https://gist.githubusercontent.com/mkzia/aa4f293661dba857b8c4459c0095ac95/raw/8075037f6f7689a1786405c1bc8ea9471d3aa9c3/train.csv")
    df = pd.DataFrame(Titanic_Dataset)
    # END SOLUTION
    return df


def step2(df):
    """
    # Step 2: Clean data
    Modify df to drop the following columns:
    PassengerId
    Name
    Ticket
    Cabin
    Hint: Just pass all the columns to the .drop() method as an array
    """
    # BEGIN SOLUTION
    columns_to_drop = ['PassengerId', 'Name', 'Ticket', 'Cabin']
    df = df.drop(columns=columns_to_drop)
    # END SOLUTION
    return df


def step3(df):
    """
    # Step 3: Drop NaNs and reindex
    You want to reindex so your index does not have missing values after you drop the NaNs. Remember, index is used 
    to access a row. Notice how many rows you dropped!
    Modify df to drop NaNs and reindex
    """
    # BEGIN SOLUTION
    df = df[~df.isnull().any(axis=1)]
    df = df.reset_index(drop=True)
    # END SOLUTION
    return df


def step4(df):
    """
    # Step 4: Encoding the Non-Numeric Fields
    Encode text fields to numbers
    Modify df to encode Sex and Embarked to encoded values.
    """
    # BEGIN SOLUTION
    # initialize label encoder
    sex_mapping = {"male": 0, "female": 1}
    embarked_mapping = {"C": 0, "Q": 1, "S": 2}
    df['Sex'] = df['Sex'].map(sex_mapping)
    df['Embarked'] = df['Embarked'].map(embarked_mapping)
    # END SOLUTION
    return df


def step5(df):
    """
    # Step 5: Making Fields Categorical
    Turn values that are not continues values into categorical values
    Modify df to make Pclass, Sex, Embarked, and Survived a categorical field
    """
    # BEGIN SOLUTION
    # make fields categorical
    df["Pclass"] = df["Pclass"].astype("category")
    df["Sex"] = df["Sex"].astype("category")
    df["Embarked"] = df["Embarked"].astype("category")
    df["Survived"] = df["Survived"].astype("category")
    # END SOLUTION
    return df


def step6(df):
    """
    1. Split dataframe into feature and label
    2. Do train and test split; USE: random_state = 1
    4. Use LogisticRegression() for classification
    3. Return accuracy and confusion matrix

    Use  metrics.confusion_matrix to calculate the confusion matrix
    # https://towardsdatascience.com/understanding-confusion-matrix-a9ad42dcfd62
    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
    # IMPORTANT !!!! 
    # https://stackoverflow.com/questions/56078203/why-scikit-learn-confusion-matrix-is-reversed

    From the confusion matrix get TN, FP, FN, TP

    return --> accuracy, TN, FP, FN, TP; 
    Hint: round accuracy to 4 decimal places

    """
    # BEGIN SOLUTION
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import confusion_matrix
    feature = df.loc[:, df.columns != 'Survived']
    label = df['Survived']
    train_feature, test_feature, train_label, test_label = train_test_split(
        feature, label, test_size=0.25, random_state=1, stratify=df["Survived"])
    LR = LogisticRegression()
    LR.fit(train_feature, train_label)
    prediction_probabilities = LR.predict_proba(test_feature)
    prediction = prediction_probabilities.argmax(axis=1)
    total_samples = len(test_label)
    correct_predictions = sum(prediction == test_label)
    accuracy = round(correct_predictions / total_samples, 4)
    conmatrix = confusion_matrix(test_label, prediction)
    tn = conmatrix[0, 0]
    fp = conmatrix[0, 1]
    fn = conmatrix[1, 0]
    tp = conmatrix[1, 1]
    return accuracy, tn, fp, fn, tp
    # END SOLUTION

####
# YOU CANNOT USE PANDAS OR CSV MODULE to solve the following problems

####


def ex1():
    """
    YOU CANNOT USE PANDAS OR CSV MODULE to solve the following problems
    Reproduce ex1.tsv from 'AdmissionsCorePopulatedTable.txt'
    https://mkzia.github.io/eas503-notes/sql/sql_6_conditionals.html#conditionals
    Separate the columns by a tab
    """
    # BEGIN SOLUTION
    lines = open('AdmissionsCorePopulatedTable.txt', 'r').readlines()
    month_count = {}
    index = 1
    while index < len(lines):
        line = lines[index]
        data = line.strip().split('\t')
        month = data[2].split()[0].split('-')[1]
        month_name = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December',
        }
        month_name = month_name.get(int(month))
        month_count.setdefault(month_name, 0)
        month_count[month_name] += 1
        index += 1
    sorted_dict = dict(sorted(month_count.items(), key=lambda item: (-item[1], item[0]), reverse=False))
    file = open('ex1.tsv', 'w')
    header = 'AdmissionMonth\tAdmissionCount'
    file.write(header)
    keys = list(sorted_dict.keys())
    index = 0
    while index < len(keys):
        month = keys[index]
        count = sorted_dict[month]
        file.write(f'\n{month}\t{count}')
        index += 1
    # END SOLUTION


def ex2():
    """
    YOU CANNOT USE PANDAS OR CSV MODULE to solve the following problems
    Repeat ex1 but add the Quarter column 
    This is the last SQL query on https://mkzia.github.io/eas503-notes/sql/sql_6_conditionals.html#conditionals
    Hint: https://stackoverflow.com/questions/60624571/sort-list-of-month-name-strings-in-ascending-order
    """

    # BEGIN SOLUTION
    lines = open('AdmissionsCorePopulatedTable.txt', 'r').readlines()
    month_count = {}
    index = 1
    while index < len(lines):
        line = lines[index]
        data = line.strip().split('\t')
        month = data[2].split()[0].split('-')[1]
        month_name_mapping = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December',
        }
        quarters = {
            'January': 'Q1',
            'February': 'Q1',
            'March': 'Q1',
            'April': 'Q2',
            'May': 'Q2',
            'June': 'Q2',
            'July': 'Q3',
            'August': 'Q3',
            'September': 'Q3',
            'October': 'Q4',
            'November': 'Q4',
            'December': 'Q4'
        }
        month_name = month_name_mapping[int(month)]
        month_count.setdefault(month_name, 0)
        month_count[month_name] += 1
        index += 1
    sorted_dict = dict(sorted(month_count.items(), key=lambda item: list(month_name_mapping.values()).index(item[0])))
    file = open('ex2.tsv', 'w')
    header = f'Quarter\tAdmissionMonth\tAdmissionCount'
    file.write(header)
    keys = list(sorted_dict.keys())
    index = 0
    while index < len(keys):
        month = keys[index]
        count = sorted_dict[month]
        file.write(f'\n{quarters[month]}\t{month}\t{count}')
        index += 1
    # END SOLUTION


def ex3():
    """
    YOU CANNOT USE PANDAS OR CSV MODULE to solve the following problems
    Reproduce 
    SELECT
        LabsCorePopulatedTable.PatientID,
        PatientCorePopulatedTable.PatientGender,
        LabName,
        LabValue,
        LabUnits,
        CASE
            WHEN PatientCorePopulatedTable.PatientGender = 'Male'
            AND LabValue BETWEEN 0.7
            AND 1.3 THEN 'Normal'
            WHEN PatientCorePopulatedTable.PatientGender = 'Female'
            AND LabValue BETWEEN 0.6
            AND 1.1 THEN 'Normal'
            ELSE 'Out of Range'
        END Interpretation
    FROM
        LabsCorePopulatedTable
        JOIN PatientCorePopulatedTable ON PatientCorePopulatedTable.PatientID = LabsCorePopulatedTable.PatientID
    WHERE
        LabName = 'METABOLIC: CREATININE'
    ORDER BY
        - LabValue

    using PatientCorePopulatedTable.txt and LabsCorePopulatedTable

    **** ADD  LabDateTime
    **** SORT BY Patient ID and then LabDateTime in ascending order 
    """
    # BEGIN SOLUTION
    lines = open('LabsCorePopulatedTable.txt', 'r').readlines()
    Labs_core = []
    index = 1
    while index < len(lines):
        data = lines[index].strip().split('\t')
        Labs_core += [[data[0], data[2], data[3], data[4], data[5]]]
        index += 1
    lines = open('PatientCorePopulatedTable.txt', 'r').readlines()
    Patient_core = []
    index = 1
    while index < len(lines):
        data = lines[index].strip().split('\t')
        Patient_core += [[data[0], data[1]]]
        index += 1
    Patient_core_dict = dict(Patient_core)
    index = 0
    while index < len(Labs_core):
        key = Labs_core[index]
        key_index = 0
        while key_index < len(key):
            if key[key_index] in Patient_core_dict.keys():
                key += [Patient_core_dict[key[key_index]]]
            key_index += 1
        index += 1
    Labs_core_lst = []
    key_index = 0
    while key_index < len(Labs_core):
        key = Labs_core[key_index]
        if key[1] == 'METABOLIC: CREATININE':
            Labs_core_lst += [key]
        key_index += 1
    key_index = 0
    while key_index < len(Labs_core_lst):
        key = Labs_core_lst[key_index]        
        key_index = 0
        while key_index < len(Labs_core_lst):
            key = Labs_core_lst[key_index]           
            gender = key[5]
            value = float(key[2])           
            case = {
                (gender == 'Male' and 0.7 <= value <= 1.3): 'Normal',
                (gender == 'Female' and 0.6 <= value <= 1.1): 'Normal'
            }            
            key.append(case.get(True, 'Out of Range'))            
            key_index += 1 
        key_index += 1
    Labs_core_lst = sorted(Labs_core_lst, key=lambda x: (x[0], x[4], x[2]))
    with open('ex3.tsv', 'w') as file:
        header = f'PatientID\tPatientGender\tLabName\tLabValue\tLabUnits\tLabDateTime\tInterpretation'
        file.write(header)
        for key in Labs_core_lst:
            file.write(f'\n{key[0]}\t{key[5]}\t{key[1]}\t{key[2]}\t{key[3]}\t{key[4]}\t{key[6]}')
    # END SOLUTION


def ex4():
    """
    YOU CANNOT USE PANDAS OR CSV MODULE to solve the following problems
    Reproduce this
    WITH AGE AS (
        SELECT 
            PATIENTID,
            ROUND((JULIANDAY('NOW') - JULIANDAY(PATIENTDATEOFBIRTH))/365.25) AGE
        FROM 
            PATIENTCOREPOPULATEDTABLE
    )
    SELECT 
        CASE 
            WHEN AGE < 18 THEN 'YOUTH'
            WHEN AGE BETWEEN 18 AND 35 THEN 'YOUNG ADULT'
            WHEN AGE BETWEEN 36 AND 55 THEN 'ADULT'
            WHEN AGE >= 56 THEN 'SENIOR'
        END AGE_RANGE,
        COUNT(*) AGE_RANGE_COUNT
    FROM 
        AGE
    GROUP BY AGE_RANGE
    ORDER BY AGE

    ****** VERY IMPORTANT: Use the Date: 2022-12-11 as today's date!!!! VERY IMPORTANT otherwise your result will change everyday!
    ****** VERY IMPORTANT divide the number of days by 365.25; to get age do math.floor(delta.days/365.25), where delta days is now-dob

    """
    # BEGIN SOLUTION
    import math
    import datetime
    strp_time = datetime.datetime.strptime
    lines = open('PatientCorePopulatedTable.txt', 'r').readlines()
    Patient_core = []
    line_index = 1
    while line_index < len(lines):
        line = lines[line_index].strip().split('\t')
        Patient_core += [[line[0], line[2]]]
        line_index += 1
    index = 0
    while index < len(Patient_core):
        Patient_core_index = Patient_core[index]
        current_date = strp_time('2022-12-11', '%Y-%m-%d')
        dob = strp_time(Patient_core_index[1], '%Y-%m-%d %H:%M:%S.%f')
        age = current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day))
        Patient_core_index += [age]
        index += 1
    index = 0
    while index < len(Patient_core):
        Patient_core_index = Patient_core[index]
        age_range = {
            (Patient_core_index[2] < 18): 'YOUTH',
            (18 <= Patient_core_index[2] <= 35): 'YOUNG ADULT',
            (36 <= Patient_core_index[2] <= 55): 'ADULT',
            (Patient_core_index[2] >= 56): 'SENIOR'
        }
        Patient_core_index += [age_range.get(True, '')]
        index += 1
    category_counts = {
        'YOUTH': 0,
        'YOUNG ADULT': 0,
        'ADULT': 0,
        'SENIOR': 0,
    }
    index = 0
    while index < len(Patient_core):
        Patient_core_index = Patient_core[index]
        category_counts[Patient_core_index[3]] += 1
        index += 1
    file = open('ex4.tsv', 'w')
    header = f'AGE_RANGE\tAGE_RANGE_COUNT'
    file.write(header)
    index = 0
    while index < len(category_counts):
        key = list(category_counts.keys())[index]
        value = list(category_counts.values())[index]
        if value != 0:
            file.write(f'\n{key}\t{value}')
        index += 1
    # END SOLUTION
