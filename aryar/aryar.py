# aryar.py


import requests
import os

def generate_story_from_image(filename):
    # Call the image captioning API
    caption = query_image_caption(filename)
    # Call the story generation API with the generated caption
    story = generate_story_from_text(caption)
    return story

def query_image_caption(filename):
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    headers = {"Authorization": "Bearer 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"}
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    response_json = response.json()

    if isinstance(response_json, list):
        # Extract caption from the first item in the list
        caption = response_json[0].get("generated_text", "")
    elif isinstance(response_json, dict):
        # Extract caption from the dictionary
        caption = response_json.get("generated_text", "")
    else:
        caption = ""

    return caption

def generate_story_from_text(text, max_length=30):
    API_URL = "https://api-inference.huggingface.co/models/openai-community/gpt2"
    headers = {"Authorization": "Bearer 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"}
    payload = {"inputs": text, "max_length": max_length}  # Adjust max_length as needed
    response = requests.post(API_URL, headers=headers, json=payload)
    response_json = response.json()
    
    if isinstance(response_json, list):
        return "\n".join(item["generated_text"] for item in response_json)
    elif isinstance(response_json, dict):
        return response_json.get("generated_text")
    else:
        return "Error: Unexpected response format"

def arya_tell_me(folder_path, max_length=30):
    stories = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            caption = query_image_caption(image_path)
            story = generate_story_from_text(caption, max_length)
            stories.append(('ARYA : ' + story))
    
    return stories
