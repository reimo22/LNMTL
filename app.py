import requests
import json
import gradio as gr
from scraper import scrape_webpage  # Import the scrape_webpage function

# Define the API endpoint
API_URL = "http://localhost:11434/api/tags"

# Function to fetch the list of models
def fetch_models():
    response = requests.get(API_URL)
    if response.status_code == 200:
        models_data = response.json()
        return [model['name'] for model in models_data['models']]
    else:
        print(f"Error: {response.status_code}")
        response.raise_for_status()

# Define the model and prompt as variables
PREPEND = "You are a professional translator. Please translate the following passage from the novel into English. Return only the translated passage and nothing else. Please ignore any navigation menus, recommendations, links, or extraneous text. You may translate names phonetically but titles should be replaced by English equivalents. \nPassage:"
APPEND = "\n\nEnglish text:\n"

def generate_completion(model, prompt):
    # Prepare the payload
    payload = {
        "model": model,
        "prompt": PREPEND + prompt + APPEND
    }

    # Make the POST request to the API
    response = requests.post("http://localhost:11434/api/generate", json=payload, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Iterate over the streaming response
        for line in response.iter_lines():
            if line:
                # Decode the JSON line
                json_line = json.loads(line.decode('utf-8'))
                yield json_line
    else:
        print(f"Error: {response.status_code}")
        response.raise_for_status()

def gradio_interface(model, url):
    # Scrape the webpage to get the prompt
    prompt = scrape_webpage(url)

    output_text = ""
    chunk_size = 500
    for i in range(0, len(prompt), chunk_size):
        chunk = prompt[i:i + chunk_size]
        for response_chunk in generate_completion(model, chunk):
            if not response_chunk['done']:
                output_text += response_chunk['response']
                yield output_text

# Fetch the list of models
models = fetch_models()

# Custom CSS for increasing text size and making the markdown box scrollable
custom_css = """
.gradio-container .gradio-markdown {
    font-size: 14pt; /* Increase text size by 2 pts */
    max-height: 300px; /* Set a maximum height */
    overflow-y: auto; /* Make it scrollable */
}
"""

# Create the Gradio interface
iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Dropdown(models, label="Model"),
        gr.Textbox(label="URL")
    ],
    outputs=gr.Markdown(label="Response"),
    title="LNMTL",
    description="Translate your favorite novels using ollama",
    allow_flagging="never",
    css=custom_css  # Apply the custom CSS
)

# Launch the Gradio interface
iface.launch()
