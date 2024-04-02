import pandas as pd

data = pd.DataFrame({'Прогноз погоды':['Пасмурно', 'Солнечно', 'Солнечно', 'Пасмурно', 'Пасмурно', 'Дождливо', 'Солнечно', 'Дождливо', 'Дождливо', 'Пасмурно'],
                     'Влажность%':[87,80,80,75,75,80,80,80,85,87], 'Ветер':[False,True,True,True,True,False,True,False,False,False], 
                     'Играть ли в гольф':[1,1,1,1,1,0,0,0,0,1]})

print (data)

X = data[['Прогноз погоды', 'Влажность%', 'Ветер']]
X_true = data[['Прогноз погоды', 'Влажность%', 'Ветер']][data['Играть ли в гольф'] == 1]

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
        if item[0] != 'Играть ли в гольф':
            res += f'({item[0]}='
            value = ''
            for l in range(len(item[1])):
                if not value:
                    value = str(item[1][l])
                elif str(item[1][l]) in value:
                    pass
                else:
                    value += str(f'V{item[1][l]}')
            res += value
            res += ')&'  
        else:
            res = res[:-1]
            res += ' THEN "PLAY" = PLAY'
    return res

def get_maybe_rule(maybe_dataframe): #get a rule to print objects are able to be positive
    res = 'IF '
    for item in maybe_dataframe.items():
        if item[0] != 'Играть ли в гольф':
            res += f'({item[0]}='
            value = ''
            for l in range(len(item[1])):
                if not value:
                    value = str(item[1][l])
                elif str(item[1][l]) in value:
                    pass
                else:
                    value += str(f'V{item[1][l]}')
            res += value
            res += ')&'  
        else:
            res = res[:-1]
            res += ' THEN "PLAY" = MAYBE PLAY'
    return res

def get_neg_rule(not_pos_dataframe): #get a rule to print only negative objects
    res = 'IF '
    for item in not_pos_dataframe.items():
        if item[0] != 'Играть ли в гольф':
            res += f'({item[0]}='
            value = ''
            for l in range(len(item[1])):
                if not value:
                    value = str(item[1][l])
                elif str(item[1][l]) in value:
                    pass
                else:
                    value += str(f'V{item[1][l]}')
            res += value
            res += ')&'  
        else:
            res = res[:-1]
            res += ' THEN "PLAY" = DONT PLAY'
    return res

elementary = get_elementary_subsets(X)

lower_init, lower, all_lower = get_lower(elementary, X_true_indexes)
upper_init, upper, all_upper = get_upper(elementary, X_true_indexes)

approximation_rate = len(all_lower)/len(all_upper) #get an approximation rate

POS_x = lower
BOND_x = set(upper).difference(set(lower))
not_POS_x = all_indexes.difference(set(all_upper))

not_pos_dataframe = pd.DataFrame([data.loc[el] for el in not_POS_x], index=range(len(not_POS_x)))
pos_dataframe = pd.DataFrame([data.loc[el] for el in POS_x], index=range(len(POS_x)))
maybe_dataframe = pd.DataFrame([data.loc[el] for el in BOND_x], index=range(len(BOND_x)))

pos_rule = get_pos_rule(pos_dataframe)
neg_rule = get_neg_rule(not_pos_dataframe)
maybe_rule = get_maybe_rule(maybe_dataframe)

#to print all the rules we get and the approximation rate
print(f'1) {pos_rule}')
print(f'2) {neg_rule}')
print(f'3) {maybe_rule}')
print(f'approximation rate is {approximation_rate}')