# Import necessary libraries
import openai
from openai import OpenAI
from bs4 import BeautifulSoup
import requests
from urllib import robotparser
import pandas as pd
import random
import time
from secretKey import openAIKey

# Define a list of prompts for GPT-3.5-turbo
promptList = ["Summarize the main idea and key points of the paragraph about: topic_content.",
              "Provide a concise summary of the paragraph discussing ' topic_content ' in detail.",
              "Condense the information in the paragraph regarding ' topic_content ' into a brief overview.",
              "Give me a short summary highlighting the crucial information in the paragraph about: topic_content.",
              "Create a snippet summarizing the paragraph's key insights on ' topic_content ' and its implications."]

# Define headers for the generated snippets
promptHeaders = ["chatGpt1", "chatGpt2", "chatGpt3", "chatGpt4", "chatGpt5"]

# Set the OpenAI API key
openai.api_key = openAIKey

# Function to fetch Google snippets for a given query
def get_google_snippets(query):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    url = f'https://www.google.com/search?q={query}&ie=utf-8&oe=utf-8&num=10'
    html = requests.get(url, headers=headers)

    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'html.parser')
        counter = 0
        summary = []

        # Extract relevant information from Google search results
        for container in soup.findAll('div', class_="tF2Cxc"):
            try:
                heading = container.find('h3', class_='LC20lb').text
                article_summary = container.find('div', class_='VwiC3b').text
                link = container.find('a')['href']

                # Skip YouTube links
                if "youtube" in link.lower():
                    continue

                print(heading, ": ", article_summary, "\n\n")
            except Exception as e:
                continue
            counter = counter + 1

            # Append information to the summary list
            summary.append({
                'heading': heading,
                'snippet': article_summary,
                'url': link,
            })

    return summary

# Function to parse the content of a URL and return the body text
def parse_url(url):
    # Return ONLY Body. Everything else needs to be done here
    str = ""

    try:
        domain = url.split('//')[1].split('/')[0]
        rp = robotparser.RobotFileParser()
        rp.set_url(f"https://{domain}/robots.txt")
        rp.read()

        if rp.can_fetch("*", url):
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Get the body content and clean it
                body_content = soup.body.get_text()
                body_content_cleaned = body_content.replace('\n', '')
                str = body_content_cleaned

    except Exception as e:
        return str

    return str

# Function to create a prompt for GPT-3.5-turbo based on the query and selected prompt
def get_prompt(prompt, query):
    pL = prompt.split("topic_content")
    newPrompt = pL[0]
    newPrompt = newPrompt + query
    if len(pL) > 2:
        newPrompt = newPrompt + pL[2]

    return newPrompt

# Function to generate snippets using GPT-3.5-turbo
def get_snippet_from_gpt(updatedGoogleSnippet):
    for val in updatedGoogleSnippet:
        for index, prompt in enumerate(promptList):
            if len(val) == 0:
                continue
            time.sleep(25)

            try:
                client = OpenAI(api_key=openai.api_key,)

                # Create a chat completion using GPT-3.5-turbo
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system",
                         "content": get_prompt(prompt, val['query']) + "Also do so in about" + str(
                             len(val['snippet']) + 100) + " characters:"},
                        {"role": "user", "content": val['body']}
                    ],
                    model="gpt-3.5-turbo",
                )

                # Update the snippet in the dictionary with the generated content
                val[promptHeaders[index]] = chat_completion.choices[0].message.content
            except Exception as e:
                val[promptHeaders[index]] = ""

    return updatedGoogleSnippet

# Function to read and pick a random question from the file "output.txt"
def read_and_pick_question():
    with open("output.txt", 'r', encoding='utf-8') as file:
        questions = file.readlines()

    questions = [question.strip() for question in questions]

    random_question = random.choice(questions)

    return random_question



if __name__ == "__main__":
    start_time = time.time()
    updatedGoogleSnippet = []

    while len(updatedGoogleSnippet) < 20:
        query = read_and_pick_question()

        # Fetch Google snippets for the query
        googleSnippets = get_google_snippets(query)
        tempSnippets = []

        # Parse URLs and prepare snippets for GPT-3.5-turbo
        for val in googleSnippets:
            body = parse_url(val['url'])
            val['body'] = body[:4000]
            val["query"] = query
            if body != "":
                tempSnippets.append(val)

        # Append selected snippets to the list
        for snip in tempSnippets[:3]:
            updatedGoogleSnippet.append(snip)

    # Generate snippets using GPT-3.5-turbo
    updatedGoogleSnippet = get_snippet_from_gpt(updatedGoogleSnippet)

    # Create a DataFrame and save it to an Excel file
    df = pd.DataFrame(updatedGoogleSnippet)
    excel_file = 'snippet_files.xlsx'
    df.to_excel(excel_file, index=False)

    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    print("Done: ", elapsed_time)
