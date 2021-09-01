import json
import os
import boto3

ENDPOINT_NAME = os.environ['SAGEMAKER_ENDPOINT']

def pred(event, context):
    body = json.loads(event['body'])
    query = body['query']
    client = boto3.client("sagemaker-runtime", region_name="ap-northeast-1")

    data = {'inputs': query}
    response = client.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        Body=json.dumps(data),
        ContentType='application/json',
        Accept='application/json'
    )

    result = json.loads(response['Body'].read().decode())[0]
    label = result['label']
    score = round(result['score'] * 100, 1)
    response_body = {
        "label": label,
        "score": score
    }

    return {
        'statusCode': 200,
        "body": json.dumps(response_body)
    }

