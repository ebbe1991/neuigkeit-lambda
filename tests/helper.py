import json

DEFAULT_TENANT_ID = 'mytenant1'


def event(path: str, method='GET',
          body: str = None,
          pathParameters: str = None,
          headers: str = {'x-tenant-id': DEFAULT_TENANT_ID,
                          'Content-Type': 'application/json'}
          ) -> dict:
    return {
        'version': '2.0',
        'routeKey': f"{method} {path}",
        'rawPath': path,
        'rawQueryString': '',
        'cookies': [],
        'requestContext': {
            'accountId': '123',
            'apiId': 'test',
            'domainName': 'test.execute-api.eu-central-1.amazonaws.com',
            'domainPrefix': 'test',
            'http': {
                'method': method,
                'path': path,
                'protocol': 'HTTP/1.1',
                'sourceIp': '127.0.0.1'
            },
            'stage': '$default',
            'requestId': '123',
            'routeKey': f"{method} {path}",
            'timeEpoch': 1673596800000
        },
        'pathParameters': pathParameters,
        "headers": headers,
        'body': body,
        'isBase64Encoded': False
    }


def lambda_response(status_code: int, body: str = None) -> dict:
    return {
        'statusCode': status_code,
        'body': body,
        'isBase64Encoded': False,
        'cookies': [],
        'headers': {'Content-Type': 'application/json'}
    }


def extract_body(response):
    return json.loads(response['body'])


def extract_status_code(response):
    return response['statusCode']


def extract_id(response):
    return extract_body(response)['id']
