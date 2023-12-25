# Search Dataset used:  https://www.kaggle.com/code/tataiee1375/starter-question-pairs-dataset-6135b053-9
#                       https://www.kaggle.com/datasets/imoore/60k-stack-overflow-questions-with-quality-rate
#                       https://rajpurkar.github.io/SQuAD-explorer/


import pandas as pd
import json

# Function to extract questions from Q&A dataset
def extract_from_qna():
    # Read Q&A dataset from CSV
    df = pd.read_csv("questions.csv")
    questions = df['question2']
    with open("output.txt", 'a', encoding='utf-8') as file:
        for row in questions:
            file.write(f"{row}\n")

# Function to extract questions from Stack Overflow dataset
def extract_from_stack_overflow():
    df = pd.read_csv("train.csv")
    questions = df['Title']
    with open("output.txt", 'a', encoding='utf-8') as file:
        for row in questions:
            file.write(f"{row}\n")

# Function to extract questions from SQuAD dataset
def extract_from_squad():
    with open("output.txt", 'a', encoding='utf-8') as file:
        with open('train.json') as f:
            data = json.load(f)
            for rec in data['data']:
                for ques in rec["paragraphs"]:
                    for qas in ques['qas']:
                        file.write(f"{qas['question']}\n")


if __name__ == "__main__":
    extract_from_qna()
    extract_from_stack_overflow()
    extract_from_squad()
