from fastapi import FastAPI, HTTPException
import boto3
import requests
from pydantic import BaseModel
import os
from mangum import Mangum 
from fastapi import APIRouter, HTTPException
from typing import List
import time

app = FastAPI()

# Retrieve environment variables
dynamodb_table_name = os.environ['DYNAMODB_TABLE_NAME']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)

class Summary(BaseModel):
    id: str
    title: str
    summary: str
    url: str

router = APIRouter()

@router.get("/summarize")
async def summarize() -> List[Summary]:
    response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch top stories from Hacker News API")

    story_ids = response.json()[:3]
    # print('hi1')

    summaries = []
    for story_id in story_ids:
        story_response = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json')
        if story_response.status_code != 200:
            # Skip this story if failed to fetch its data
            continue

        story_data = story_response.json()
        title = story_data.get('title')
        url = story_data.get('url')

        if url is None:
            # Skip this story if it doesn't have a URL
            continue
        # print('hi2')
        
        jina_api_url = f'https://r.jina.ai/{url}'
        jina_response = requests.get(jina_api_url, params={'url': url, 'api_key': os.environ.get('JINA_READER_API_KEY')})
        if jina_response.status_code != 200:
            # Skip this story if failed to fetch text from Jina Reader API
            continue
        # print('hi3')
        text = jina_response.text
        print(text)

        my_prompt = text
        system_input = "Summarize the following text:"

        parameters = {
                        "model": "gpt-3.5-turbo",
                        "messages": [
                            {"role": "system", "content": system_input},
                            {"role": "user", "content": my_prompt}
                        ],
                        "max_tokens":100
        }

        openai_response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={'Authorization': f'Bearer {os.environ.get("OPENAI_API_KEY")}'},
            json = parameters
        )
        # print("hi3.5")
        # print(openai_response)
        # print("hi3.6")
        openai_data = openai_response.json()
        if openai_response.status_code == 200:
            generated_text = openai_data['choices'][0]['message']['content']
        elif openai_response.status_code == 429:
            time.sleep(1)
        elif openai_response.status_code != 200:
            # Skip this story if failed to get summary from OpenAI API
            # print('hi4')
            continue

        summaries.append(Summary(id=str(story_id), title=title, summary=generated_text.strip(), url=url))
        # print('hi5')
        print(summaries)

    return summaries

app.include_router(router)
# Create a handler for AWS Lambda using Mangum
handler = Mangum(app)
