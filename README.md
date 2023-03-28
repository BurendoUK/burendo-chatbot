# burendo-chatbot
This repository contains a script for a sample use case of a chatbot as a Document Search Assistant. The assistant uses the OpenAI GPT-3.5 Turbo model, SentenceTransformer library, and Gradio to search through indexed documents in a specified folder and provide relevant answers based on user queries.  This has been created for fun and testing the integrations with OpenAI's API.

*Features*
- Indexes documents within a folder and converts them into embeddings for efficient searching.
- Uses the GPT-3.5 Turbo model to generate human-like responses based on the most relevant document found.
- Provides a user-friendly Gradio interface to input queries and receive responses.
- Supports a wide range of file types (text, markdown, PDF, Word, Excel, etc.) thanks to the textract library.

##  Package Install

To maximise the functionality of `textract` and to be able to process all filetypes, it's recommended you follow the installation instructions below.  You can, however, just run `make install` and test functionality against simple files like `.md` or `.txt` etc.

[See here:](https://textract.readthedocs.io/en/latest/installation.html)

_TL;DR_

### Ubuntu Install

```
apt-get install python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr \
flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig libpulse-dev

make install
```

### Mac OSX Install

```
brew cask install xquartz
brew install poppler antiword unrtf tesseract swig

make install
```

## Run

- Clone the repository to your local machine
- Set your OpenAI API key by modifying the openai.api_key variable in the script.  You can generate an API key [here](https://platform.openai.com/account/api-keys) - n.b. you may need to sign up.
- Put your documents in a directory and set the `folder_path` variable to the path of the directory in the script; e.g., `documents`
- Run the script:
```
python3 chat.py
```

- The script will launch a web interface where you can enter your query and get an answer based on the most relevant document in the directory
```
Running on local URL:  http://127.0.0.1:7860
```

You can track your token usage [here](https://platform.openai.com/account/usage)



## Example

Suppose you have a directory called documents containing the following files:

report1.docx
report2.pdf
report3.md

To use the script to answer a question about the documents, follow these steps:

Set folder_path to "documents"
Run the script with the command python document_retrieval_qa.py
The script will launch a web interface
Enter a question like "What is the purpose of these reports?"
The script will retrieve the most relevant document and use GPT-3 to generate an answer to the question based on the retrieved document
