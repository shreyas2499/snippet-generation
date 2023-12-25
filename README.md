Steps to run the above project:

1) Clone the repository using "git clone https://github.com/shreyas2499/snippet-generation.git" into a suitable directory in your system.
2) Open the local respository using your editor.
3) In the terminal, create a new virtual environment using the command: python3 -m venv -env name-.
4) Activate the virtual environment using the command: source -env name-/bin/activate
5) This would activate the virtual environment. Now, download all the required dependencies which are listed in the requirements.txt file by running the command: pip install -r requirements.txt. Note: Ensure to run this command within the virtual environment you just created.
6) The dataFormation.py file has links to all the required datasets. Download them and name them accordingly. Then run the command: py dataFormation.py to preprocess the data and get only the questions from each of the datasets.
7) Add the Open AI api key in a file called secretKey.py
8) Once the above steps are done, you should be able to run the main snippetGeneration.py file by using the command: py snippetGeneration.py
9) The results will be stored in an excel file.



To create an OpenAI API Key, follow the instructions given here: https://platform.openai.com/docs/overview
Note: Ensure that you never push your API key to a public repository. If you do that, the key gets disabled. 
