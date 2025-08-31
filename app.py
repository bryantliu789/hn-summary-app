from fastapi import FastAPI, HTTPException, APIRouter
import boto3
import requests
from pydantic import BaseModel
import os
from mangum import Mangum 
from typing import List
import time

app = FastAPI()

# Initialize DynamoDB connection
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
    # Fetch top stories from Hacker News
    response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch top stories from Hacker News API")

    story_ids = response.json()[:3]
    summaries = []

    for story_id in story_ids:
        # Fetch story details
        story_response = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json')
        if story_response.status_code != 200:
            continue

        story_data = story_response.json()
        title = story_data.get('title')
        url = story_data.get('url')

        if url is None:
            continue
        
        # Extract text using Jina Reader API
        jina_api_url = f'https://r.jina.ai/{url}'
        jina_response = requests.get(
            jina_api_url,
            params={'url': url, 'api_key': os.environ.get('JINA_READER_API_KEY')}
        )
        if jina_response.status_code != 200:
            continue

        text = jina_response.text

        # Prepare request for OpenAI summarization
        system_input = "Summarize the following text:"
        parameters = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_input},
                {"role": "user", "content": text}
            ],
            "max_tokens": 100
        }

        openai_response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={'Authorization': f'Bearer {os.environ.get("OPENAI_API_KEY")}'},
            json=parameters
        )

        if openai_response.status_code == 200:
            openai_data = openai_response.json()
            generated_text = openai_data['choices'][0]['message']['content']
        elif openai_response.status_code == 429:
            time.sleep(1)
            continue
        else:
            continue

        summaries.append(
            Summary(
                id=str(story_id),
                title=title,
                summary=generated_text.strip(),
                url=url
            )
        )

    return summaries

app.include_router(router)

# AWS Lambda handler
handler = Mangum(app)
