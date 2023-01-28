import json
from aws_lambda_powertools.event_handler import Response
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEventV2
from http_exception import ValidationException


def extractId(event: APIGatewayProxyEventV2) -> str:
    pathParameters = event.path_parameters
    id = None
    if pathParameters:
        id = pathParameters.get('id')
    if id and len(id) > 0:
        return id
    else:
        raise ValidationException('id not present.')


def extractBody(event: APIGatewayProxyEventV2) -> str:
    body = event.decoded_body
    json_body = None
    if body:
        json_body = json.loads(body)
    if json_body and len(json_body) > 0:
        return json_body
    else:
        raise ValidationException('body not present.')


def extractTenant(event: APIGatewayProxyEventV2) -> str:
    tenant_id = event.get_header_value('x-tenant-id')
    if tenant_id and len(tenant_id) > 0:
        return tenant_id
    else:
        raise ValidationException('tenant not present.')


def emptyResponse(statusCode: int):
    return Response(
        status_code=statusCode,
        content_type='application/json',
        body=None
    )


def response(statusCode: int, body: str):
    return Response(
        status_code=statusCode,
        content_type='application/json',
        body=body
    )
