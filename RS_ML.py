import pandas as pd

# df_path = 'D:\Python projects\RST-RS1-algorithm\golf.csv'
df_path = 'D:\Python projects\RST-RS1-algorithm\Train_data_golf_14ex.csv'

try:
    data = pd.read_csv(df_path)
    print ('\n' + '[----------------------- DATASET -----------------------]')
    print (data)
    print ('\n' + '[-------------------------------------------------------]')
except Exception as e:
    print(e)

X = data [['Outlook', 'Humidity%', 'Wind']] 
X_true = data[['Outlook', 'Humidity%', 'Wind']][data['Play'] == 'yes']

all_indexes = set(data.index)
X_true_indexes = set(X_true.index)

def get_elementary_subsets(X): #get elementary subsets from set of objects
    subsets = []
    for i in range(len(X)):
        similar = [i]
        for j in range(i + 1, len(X)):
            if X.iloc[i].equals(X.iloc[j]):
                similar.append(j)

        if not any(set(similar) & set(sub) for sub in subsets):
            subsets.append(similar)

    return subsets

def get_lower(elementary, X_true_indexes): #get a lower approximation
    lower_init = [elem for elem in elementary if set(elem).issubset(X_true_indexes)]
    lower = [elem[0] for elem in lower_init]
    all_lower = [j for elem in lower_init for j in elem]

    return lower_init, lower, all_lower

def get_upper(elementary, X_true_indexes): #get an upper approximation
    upper_init = [elem for elem in elementary if set(elem).intersection(X_true_indexes) != set()]
    upper = [elem[0] for elem in upper_init]
    all_upper = [j for elem in upper_init for j in elem]
    
    return upper_init, upper, all_upper

def get_pos_rule(pos_dataframe): #get a rule to print only positive objects
    res = 'IF '
    for item in pos_dataframe.items():
        if item[0] != 'Play':
            res += f'({item[0]} = '
            value = ''
            for l in range(len(item[1])):
                if not value:
                    value = str(item[1][l])
                elif str(item[1][l]) in value:
                    pass
                else:
                    value += str(f' & {item[1][l]}')
            res += value
            res += ')& '  
        else:
            res = res[:-1]
            res += ' THEN DECISION "PLAY" = PLAY'
    return res

def get_maybe_rule(maybe_dataframe): #get a rule to print objects are able to be positive
    res = 'IF '
    for item in maybe_dataframe.items():
        if item[0] != 'Play':
            res += f'({item[0]} = '
            value = ''
            for l in range(len(item[1])):
                if not value:
                    value = str(item[1][l])
                elif str(item[1][l]) in value:
                    pass
                else:
                    value += str(f' V {item[1][l]}')
            res += value
            res += ')&'  
        else:
            res = res[:-1]
            res += ' THEN DECISION "PLAY" = MAYBE PLAY'
    return res

def get_neg_rule(not_pos_dataframe): #get a rule to print only negative objects
    res = 'IF '
    for item in not_pos_dataframe.items():
        if item[0] != 'Play':
            res += f'({item[0]} = '
            value = ''
            for l in range(len(item[1])):
                if not value:
                    value = str(item[1][l])
                elif str(item[1][l]) in value:
                    pass
                else:
                    value += str(f' V {item[1][l]}')
            res += value
            res += ')&'  
        else:
            res = res[:-1]
            res += ' THEN DECISION "PLAY" = DON\'T PLAY'
    return res

elementary = get_elementary_subsets(X)

lower_init, lower, all_lower = get_lower(elementary, X_true_indexes)
upper_init, upper, all_upper = get_upper(elementary, X_true_indexes)

# Calculating an approximation occuracy
approximation_rate = round(len(all_lower) / len(all_upper), 3)

POS_x = lower
BND_X = set(upper).difference(set(lower))
NEG_X = all_indexes.difference(set(all_upper))

# Creating a dataframe for each region
not_pos_dataframe = pd.DataFrame([data.loc[el] for el in NEG_X], index=range(len(NEG_X)))
pos_dataframe = pd.DataFrame([data.loc[el] for el in POS_x], index=range(len(POS_x)))
maybe_dataframe = pd.DataFrame([data.loc[el] for el in  BND_X], index=range(len( BND_X)))

# Creating production rules for lower, upper and boundry region
pos_rule = get_pos_rule(pos_dataframe)
neg_rule = get_neg_rule(not_pos_dataframe)
maybe_rule = get_maybe_rule(maybe_dataframe)

print ('\nGetting an elementary subsets of dataset:\n' + f'{elementary}')
print (lower_init)
print ('\n' + '======== Production rules for positive region ========')
print (f'1) {pos_rule}')
print ('\n' + '======== Production rules for negative region ========')
print (f'2) {neg_rule}')
print ('\n' + '======== Production rules for boundry region ========')
print (f'3) {maybe_rule}')
print ('\n' + f'Approximation accuracy: {approximation_rate}\n')



# =================================================================================



# df_test_path = 'D:\Python projects\RST-RS1-algorithm\Test_data_golf.csv'
df_test_path = 'D:\Python projects\RST-RS1-algorithm\Test_data_golf_50ex.csv'

try:
    data_test = pd.read_csv(df_test_path)
    print ('\n' + '[----------------------- TRAIN DATASET WITHOUT ATTRIBUTE \'PLAY\' -----------------------]')
    print (data_test)
except Exception as e:
    print(e)


# Function for classification test dataset
def classify_new_data(row, pos_df, maybe_df, neg_df):
    # Checking if a row contains the conditions for a boundry region (POS)
    for _, pos_row in pos_df.iterrows():
        if (row['Outlook'] == pos_row['Outlook'] and
            row['Humidity%'] == pos_row['Humidity%'] and
            row['Wind'] == pos_row['Wind']):
            return 'yes'
    
    # Checking if a row contains the conditions for a boundry region (BND)
    for _, maybe_row in maybe_df.iterrows():
        if (row['Outlook'] == maybe_row['Outlook'] and
            row['Humidity%'] == maybe_row['Humidity%'] and
            row['Wind'] == maybe_row['Wind']):
            return 'maybe'
    
    # Checking if a row contains the conditions for a negative region (NEG)
    for _, neg_row in neg_df.iterrows():
        if (row['Outlook'] == neg_row['Outlook'] and
            row['Humidity%'] == neg_row['Humidity%'] and
            row['Wind'] == neg_row['Wind']):
            return 'no'
    
    # If row not in conditions POS/NEG/BND then return 'Unknown'
    return 'Unknown'

# Applying the classification function to the test dataset
data_test['Classification'] = data_test.apply(classify_new_data, args=(pos_dataframe, maybe_dataframe, not_pos_dataframe,), axis=1)

# Print result of classification train dataset
print ('\n' + '[----------------------- CLASSIFIED TRAIN DATASET -----------------------]')
print(data_test)

data_test['Correctly_Classified'] = data_test['Classification'] == data_test['Play']
accuracy = round(data_test['Correctly_Classified'].mean(), 3) * 100
print(f'Accuracy of the classification RS1: {accuracy} %')
