import pandas as pd

df_path = 'D:\Python projects\RST-RS1-algorithm\golf.csv'
data = pd.read_csv(df_path)


print ('\n' + '[----------------------- DATASET -----------------------]')
print (data)

X = data [['Outlook', 'Humidity%', 'Wind']] 
X_true = data[['Outlook', 'Humidity%', 'Wind']][data['Play'] == 1]

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
print ('\n' + f'Approximation occuracy: {approximation_rate}\n')
