# hn-summary-app

A serverless FastAPI application that fetches top Hacker News
 stories and returns concise AI-generated summaries. Deployed on AWS Lambda via AWS SAM with API Gateway integration.

Features

Retrieves latest top stories from Hacker News

Extracts article text using the Jina Reader API

Summarizes content with OpenAI GPT-3.5

Exposes a REST API endpoint (/summarize) via FastAPI + Mangum

Deployed on AWS Lambda with DynamoDB persistence

Tech Stack

FastAPI + Mangum for serverless API

AWS Lambda, API Gateway, DynamoDB

OpenAI GPT-3.5 API for summarization

Jina Reader API for text extraction

Python (FastAPI, boto3, requests, pydantic)

AWS SAM / CloudFormation for deployment

Usage
Deploy
sam build
sam deploy --guided

Example Request
curl https://<api-endpoint>/summarize

Example Response
[
  {
    "id": "123456",
    "title": "Show HN: A new open-source project",
    "summary": "This project introduces...",
    "url": "https://example.com/post"
  },
  ...
]
Next, you can use the AWS Serverless Application Repository to deploy ready-to-use apps that go beyond Hello World samples and learn how authors developed their applications. For more information, see the [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/) and the [AWS Serverless Application Repository Developer Guide](https://docs.aws.amazon.com/serverlessrepo/latest/devguide/what-is-serverlessrepo.html).
