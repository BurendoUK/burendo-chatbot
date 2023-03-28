import os
import glob
import openai
import requests
import json
import gradio as gr
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
import textract

openai.api_key = "your-api-token"

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def get_supported_extensions():
    return [
        '*.csv', '*.doc', '*.docx', '*.eml', '*.epub', '*.gif', '*.htm', '*.html', '*.jpeg', '*.jpg', '*.json',
        '*.log', '*.md', '*.mp3', '*.msg', '*.odt', '*.ogg', '*.pdf', '*.png', '*.pptx', '*.ps', '*.psv', '*.rtf',
        ' *.tab', '*.tff', '*.tif', '*.tiff', '*.tsv', '*.txt', '*.wav', '*.xls', '*.xlsx'
    ]

def index_documents(folder_path):
    all_files = []
    for ext in get_supported_extensions():
        all_files.extend(glob.glob(os.path.join(folder_path, '**', ext), recursive=True))

    contents = []
    for file in all_files:
        try:
            if file.lower().endswith('.md'):
                text = read_markdown_file(file)
            else:
                text = textract.process(file).decode('utf-8')
            contents.append((file, text))
        except Exception as e:
            print(f"Error processing {file}: {e}")

    return contents

def build_embeddings_index(contents):
    if not contents:
        raise ValueError("No documents were processed. Please check your folder path and file types.")
    
    model = SentenceTransformer('sentence-transformers/paraphrase-xlm-r-multilingual-v1')
    embeddings = model.encode([content[1] for content in contents])

    nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(embeddings)

    return model, nbrs, embeddings

def query_gpt3(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }

    data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    "max_tokens": 100,
    "temperature": 0.5
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(data))
    response_json = response.json()

    if response.status_code != 200 or "choices" not in response_json:
        raise ValueError(f"Error calling GPT-3.5 Turbo: {response.text}")

    return response_json["choices"][0]["message"]["content"].strip()

def generate_response(prompt):
    _, idx = nbrs.kneighbors(model.encode([prompt]))
    best_match_content = contents[idx[0][0]][1]
    gpt3_prompt = f"{prompt}\n\nDocument Content:\n{best_match_content}\n\nResponse:"
    return query_gpt3(gpt3_prompt)

if __name__ == "__main__":
    # 
    folder_path = "path/to/your/folder"
    contents = index_documents(folder_path)
    model, nbrs, embeddings = build_embeddings_index(contents)

    interface = gr.Interface(
        generate_response,
        inputs=gr.inputs.Textbox(lines=5, placeholder="Enter your query..."),
        outputs="text",
        examples=[("What is the purpose of this document?"), ("Who is the author?")]
    )
    interface.launch()
