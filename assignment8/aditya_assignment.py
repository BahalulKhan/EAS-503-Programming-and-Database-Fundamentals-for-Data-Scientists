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
    titanicdata=pd.read_csv("https://gist.githubusercontent.com/mkzia/aa4f293661dba857b8c4459c0095ac95/raw/8075037f6f7689a1786405c1bc8ea9471d3aa9c3/train.csv")
    df = pd.DataFrame(titanicdata)
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
    df=df.drop(['PassengerId','Name','Ticket','Cabin'],axis=1)
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
    df=df.dropna()
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
    from sklearn import preprocessing
    label_encoder = preprocessing.LabelEncoder()
    sex_encoded = label_encoder.fit_transform(df["Sex"])
    df['Sex'] = sex_encoded
    embarked_encoded = label_encoder.fit_transform(df["Embarked"])
    df['Embarked'] = embarked_encoded
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
    df["Pclass"]   = pd.Categorical(df["Pclass"])
    df["Sex"]      = pd.Categorical(df["Sex"])
    df["Embarked"] = pd.Categorical(df["Embarked"])
    df["Survived"] = pd.Categorical(df["Survived"])
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
    features = df.drop('Survived',axis=1)
    label=df['Survived']
    from sklearn.model_selection import train_test_split
    train_features,test_features,train_label,test_label = train_test_split(features,label,test_size = 0.25,random_state = 1,stratify = df["Survived"])
    from sklearn.linear_model import LogisticRegression
    from sklearn import metrics
    log_regress = LogisticRegression()
    log_regress.fit(X = train_features ,y = train_label)
    preds = log_regress.predict(X=test_features)
    conmatrix=metrics.confusion_matrix(y_true = test_label,y_pred = preds)
    tn,fp,fn,tp=conmatrix.ravel()
    accuracy=round(log_regress.score(X = test_features, y = test_label),4)
    return accuracy,tn,fp,fn,tp
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
    with open('AdmissionsCorePopulatedTable.txt', 'r') as f:
        lines = f.readlines()
        headers = lines[0].strip().split('\t')
        moths=[]
        for line in lines[1:]:
            data = line.strip().split('\t')
            moths.append(data[2].split(" ")[0].split("-")[1])
    months = {
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
    months_name = [months[int(num)] for num in moths]
    month_count = {}
    for month in months_name:
        if month in month_count:
            month_count[month] += 1
        else:
            month_count[month] = 1
    sorted_dict = dict(sorted(month_count.items(), key=lambda item: (-item[1],item[0])))
    with open('ex1.tsv', 'w') as file:
        header=f'AdmissionMonth\tAdmissionCount'
        file.write(header)
        for x,y in sorted_dict.items():
            file.write(f'\n{x}\t{y}')

    # END SOLUTION


def ex2():
    """
    YOU CANNOT USE PANDAS OR CSV MODULE to solve the following problems
    Repeat ex1 but add the Quarter column 
    This is the last SQL query on https://mkzia.github.io/eas503-notes/sql/sql_6_conditionals.html#conditionals
    Hint: https://stackoverflow.com/questions/60624571/sort-list-of-month-name-strings-in-ascending-order
    """

    # BEGIN SOLUT
    with open('AdmissionsCorePopulatedTable.txt', 'r') as f:
        lines = f.readlines()
        headers = lines[0].strip().split('\t')
        moths=[]
        for line in lines[1:]:
            data = line.strip().split('\t')
            moths.append(data[2].split(" ")[0].split("-")[1])
    months = {
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
    Quarters={
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
    months_name = [months[int(num)] for num in moths]
    month_count = {}
    for month in months_name:
        if month in month_count:
            month_count[month] += 1
        else:
            month_count[month] = 1
    sorted_dict = dict(sorted(month_count.items(), key=lambda item: list(months.keys())[list(months.values()).index(item[0])]))
    with open('ex2.tsv', 'w') as file:
        header=f'Quarter\tAdmissionMonth\tAdmissionCount'
        file.write(header)
        for x,y in sorted_dict.items():
            file.write(f'\n{Quarters[x]}\t{x}\t{y}')
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
    with open('LabsCorePopulatedTable.txt','r') as file:
        lines=file.readlines()
        headers = lines[0].strip().split('\t')
        values1=[]
        for line in lines[1:]:
                data = line.strip().split('\t')
                values1.append([data[0],data[2],data[3],data[4],data[5]])
    with open('PatientCorePopulatedTable.txt','r') as file:
        lines=file.readlines()
        headers = lines[0].strip().split('\t')
        values2=[]
        for line in lines[1:]:
                data = line.strip().split('\t')
                values2.append((data[0],data[1]))
    values2dict=dict(values2)
    list1=[]
    for da in values1:
        if da[0] in values2dict.keys():
            da.append(values2dict[da[0]])
    newlist=[]
    for x in values1:
        if x[1]=='METABOLIC: CREATININE':
            newlist.append(x)
    for y in newlist:
        if (y[5]=='Male' and 0.7<=float(y[2])<=1.3) or (y[5]=='Female' and 0.6<=float(y[2])<=1.1):
            y.append('Normal')
        else:
            y.append('Out of Range')
    newlist.sort(key=lambda x: x[2])
    newlist.sort(key=lambda x: (x[0], x[4]))
    with open('ex3.tsv', 'w') as file:
            header=f'PatientID\tPatientGender\tLabName\tLabValue\tLabUnits\tLabDateTime\tInterpretation'
            file.write(header)
            for y in newlist:
                file.write(f'\n{y[0]}\t{y[5]}\t{y[1]}\t{y[2]}\t{y[3]}\t{y[4]}\t{y[6]}')
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
    with open('PatientCorePopulatedTable.txt','r') as file:
        lines=file.readlines()
        headers = lines[0].strip().split('\t')
        values2=[]
        for line in lines[1:]:
                data = line.strip().split('\t')
                values2.append([data[0],data[2]])
    reference_date = datetime.datetime.strptime('2022-12-11', '%Y-%m-%d')
    def calculate_age(date_of_birth, reference_date):
        delta = reference_date - date_of_birth
        age = math.floor(delta.days / 365.25)
        return age
    for y in values2:
        y.append(calculate_age( datetime.datetime.strptime(y[1], '%Y-%m-%d %H:%M:%S.%f'),reference_date))
            
    for y in values2:
        if y[2]<18:
            y.append('YOUTH')
        if 18<=y[2]<=35:
            y.append('YOUNG ADULT')
        if 36<=y[2]<=55:
            y.append('ADULT')
        if y[2]>=56:
            y.append('SENIOR')
    category_counts = {
        'YOUTH':0,
        'YOUNG ADULT':0,
        'ADULT': 0,
        'SENIOR': 0,
    }

    for y in values2:
        if y[3] == 'YOUTH':
            category_counts['YOUTH'] += 1
        if y[3] == 'YOUNG ADULT':
            category_counts['YOUNG ADULT'] += 1
        if y[3] == 'ADULT':
            category_counts['ADULT'] += 1
        if y[3] == 'SENIOR':
            category_counts['SENIOR'] += 1
    with open('ex4.tsv', 'w') as file:
            header=f'AGE_RANGE\tAGE_RANGE_COUNT'
            file.write(header)
            for x,y in category_counts.items():
                if y!=0:
                    file.write(f'\n{x}\t{y}')
        
    # END SOLUTION
