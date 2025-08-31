# hn-summary-app

A serverless FastAPI application that fetches top [Hacker News](https://news.ycombinator.com/) stories and returns concise AI-generated summaries.  
Deployed on **AWS Lambda** via **AWS SAM** with **API Gateway** integration.

## Features
- Retrieves the latest top stories from Hacker News
- Extracts article text using the **Jina Reader API**
- Summarizes content with **OpenAI GPT-3.5**
- Exposes a `/summarize` route via **FastAPI + Mangum**
- Deployed on AWS Lambda with DynamoDB persistence

## Tech Stack
- **FastAPI** + **Mangum** (serverless API)
- **AWS Lambda**, **API Gateway**, **DynamoDB**
- **OpenAI GPT-3.5 API** for summarization
- **Jina Reader API** for text extraction
- **Python** (FastAPI, boto3, requests, pydantic)
- **AWS SAM / CloudFormation** for deployment

## Usage

### Deploy
```bash
sam build
sam deploy --guided
