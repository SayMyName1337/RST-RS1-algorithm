# Rough Set Theory (RST)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

## Project Description []

This project implements a machine learning algorithm based on Zdzislaw Pawlak's Rough Set Theory to predict golf performance based on weather conditions.

## Project structure

The project consists of the following files:

- `Train_data_golf_14ex.csv`: Training dataset.
- `Test_data_golf_50ex.csv`: Test dataset.
- `algorithm.py`: The main script with the implementation of the algorithm.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/rst-golf-prediction.git
```

2. Go to your project folder:

```bash
cd rst-golf-prediction
```

3. Install required dependencies:

```bash
pip install pandas
```

# Using the algorithm

1. Place your CSV data files in your project root folder.
2. For correct operation specify the path to the test and training dataset depending on its location on your computer
```python
df_path = 'Put your personal path here'
```
```python
df_test_path = 'Put your personal path here too'
```
3. Run the script **`RS-ML.py`**
```bash
python RS-ML.py
```

# Example of work


| Outlook       | Humidity %                | Wind | Play |
| ------------- |:------------------:| -----:|-----:|
| Overcast     | 87 | Fasle | Yes
| Sunny     | 80 | True | Yes
| Sunny  | 80 | True | Yes
| Overcast  | 75 | True | Yes
| Overcast  | 75 | True | Yes
| Rainy  | 80 | False | No
| Sunny  | 80 | True | No
| Rainy  | 80 | False | No
| Rainy  | 85 | False | No
| Overcast  | 87 | False | Yes

After launch we get the following intermediate results, which represent the construction of production rules:

```yaml
Getting an elementary subsets of dataset:
[[0, 9], [1, 2, 6], [3, 4], [5, 7], [8]]
[[0, 9], [3, 4]]

======== Production rules for positive region ========
1) IF (Outlook = Overcast)& (Humidity% = 87 & 75)& (Wind = False & True)& THEN DECISION "PLAY" = PLAY

======== Production rules for negative region ========
2) IF (Outlook = Rainy)&(Humidity% = 85 V 80)&(Wind = False) THEN DECISION "PLAY" = DON'T PLAY

======== Production rules for boundry region ========
3) IF (Outlook = Sunny)&(Humidity% = 80)&(Wind = True) THEN DECISION "PLAY" = MAYBE PLAY

Approximation accuracy: 0.571
```

The final result will be the classification of the test dataset based on the constructed rules, as well as a comparison of the classification of the algorithm with the true values.

| Outlook       | Humidity %                | Wind | Play | Classification |
| ------------- |:------------------:| -----:|-----:|-----:|
| Overcast | 87 | Fasle | Yes | Yes
| Sunny | 80 | True | Yes | Maybe
| Rainy | 80 | True | Yes | Unknown
| Sunny | 75 | True | Yes | Maybe
| NaN | 75 | True | Yes | Unknown
| Overcast | 80 | False | No | Yes
| Raqiny | 80 | True | No | No

```yaml
Accuracy of the classification RS1: 42.9 %
```

# Code Structure
The main implemented functions of the algorithm are:
* **`get_elementary_subsets(X)`**: Получение элементарных подмножеств из набора объектов.
* **`get_lower(elementary, X_true_indexes)`**: Получение нижнего приближения.
* **`get_upper(elementary, X_true_indexes)`**: Получение верхнего приближения.
* **`get_pos_rule(pos_dataframe)`**: Создание правила для положительных объектов.
* **`get_neg_rule(not_pos_dataframe)`**: Создание правила для отрицательных объектов.
* **`get_maybe_rule(maybe_dataframe)`**: Создание правила для неопределенных объектов.
* **`classify_new_data(row, pos_df, maybe_df, neg_df)`**: Классификация нового набора данных.
