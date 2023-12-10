import openai
from openai import OpenAI
from googlesearch import search
from bs4 import BeautifulSoup
import requests
from urllib import robotparser
import pandas as pd
import random
import time

promptList2 = ["Generate a snippet from the below data in approximately ", "Provide a summary of the below content in approximately "]

promptList = ["Summarize the main idea and key points of the paragraph about: topic_content", "Provide a concise summary of the paragraph discussing ' topic_content ' in detail.",
"Condense the information in the paragraph regarding ' topic_content ' into a brief overview.", "Give me a short summary highlighting the crucial information in the paragraph about: topic_content.",
"Create a snippet summarizing the paragraph's key insights on ' topic_content ' and its implications."]


columns = ["a", "b", "c"]
openai.api_key = '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'



def get_results(query):
    urlList = []

    for i in search(query=query, tld="com", num=10, stop=10, pause=2):
        urlList.append(i)
    
    return urlList


def get_google_snippets(query):
    googleSnippets = {}
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    url=f'https://www.google.com/search?q={query}&ie=utf-8&oe=utf-8&num=10'
    html = requests.get(url,headers=headers)

    if(html.status_code == 200):
        soup = BeautifulSoup(html.text, 'html.parser')
        counter = 0
        
        summary = []
        topStuff = soup.find('div', {"id": "search"})
        bottomStuff = soup.find('div', {"id": "botstuff"})

        for container in soup.findAll('div', class_="tF2Cxc"):
            try: 
                heading = container.find('h3', class_='LC20lb').text
                article_summary = container.find('div', class_='VwiC3b').text
                link = container.find('a')['href']    
                if("youtube" in link.lower()):
                    continue

                print(heading, ": ", article_summary, "\n\n")
            except Exception as e:
                continue    
            counter = counter + 1
            
            summary.append({
                'heading': heading,
                'snippet': article_summary,
                'url': link,
            })

    return summary


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

                body_content = soup.body.get_text()

                body_content_cleaned = body_content.replace('\n', '')

                str = body_content_cleaned

        # response = requests.get(url)
    except Exception as e:  
        return str
   
    return str


def get_prompt(prompt, query):
    pL = prompt.split("topic_content")

    newPrompt = pL[0]
    newPrompt = newPrompt + query
    if(len(pL)>2):
        newPrompt = newPrompt + pL[2]

    return newPrompt


def get_snippet_from_gpt(updatedGoogleSnippet, query):
    # print(promptList)

    # print("saoddna")    
    for val in updatedGoogleSnippet:
        for index, prompt in enumerate(promptList):
            
            time.sleep(25)
            # message = input("User: ")
            client = OpenAI(
            
            api_key=openai.api_key,
            )

            chat_completion = client.chat.completions.create(
                messages=[
                    { "role": "system", "content": get_prompt(prompt, query) + "Also do so in " + str(len(val['snippet'])) + " characters: "},
                    { "role": "user", "content": val['body']}
                ],
                model="gpt-3.5-turbo",
            )

            val[index] = chat_completion.choices[0].message.content
            print(chat_completion.choices[0].message.content, "\n")

    return updatedGoogleSnippet
            


def read_and_pick_question():
    with open("output.txt", 'r', encoding='utf-8') as file:
        questions = file.readlines()

    
    questions = [question.strip() for question in questions]

    
    random_question = random.choice(questions)

    return random_question

if __name__ == "__main__":
    query = read_and_pick_question()
    print(query, "\n\n\n\n")
    # query = "what is encapsulation"
    # topic = query

    
    
    googleSnippets = get_google_snippets(query)
    updatedGoogleSnippet = []
    for val in googleSnippets:
        body = parse_url(val['url'])
        val['body'] = body
        val["query"] = query
        if(body != ""):
            updatedGoogleSnippet.append(val)


    updatedGoogleSnippet = updatedGoogleSnippet[0]
    
    print("something")

    updatedGoogleSnippet = get_snippet_from_gpt([updatedGoogleSnippet], query)
    
    df = pd.DataFrame(updatedGoogleSnippet, columns=columns)
    excel_file = 'snippet_files.xlsx'
    df.to_excel(excel_file, index=False)

    print("something2")


