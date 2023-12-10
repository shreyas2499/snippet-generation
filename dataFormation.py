# Search Dataset used:  https://www.kaggle.com/code/tataiee1375/starter-question-pairs-dataset-6135b053-9

import pandas as pd


def extract_questions():
    df = pd.read_csv("questions.csv")
    questions = df['question2']
    with open("output.txt", 'a', encoding='utf-8') as file:
        for row in questions:
            file.write(f"{row}\n")

extract_questions()


