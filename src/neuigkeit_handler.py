from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
import neuigkeit_controller
from neuigkeit_controller import NeuigkeitDTO
from lambda_utils.response_utils import response, empty_response, to_json_array
from lambda_utils.event_utils import extract_body, extract_tenant, extract_stichtag
from lambda_utils.exception import ValidationException
import json
app = APIGatewayHttpResolver()


def handle(event: dict, context: dict):
    return app.resolve(event, context)


@app.post('/api/neuigkeit')
def post():
    event = app.current_event
    tenant_id = extract_tenant(event)
    body = extract_body(event)
    neuigkeit = neuigkeit_controller.create_neuigkeit(tenant_id, body)
    return response(201, neuigkeit.to_json())


@app.put('/api/neuigkeit/<id>')
def put(id):
    event = app.current_event
    tenant_id = extract_tenant(event)
    body = extract_body(event)
    neuigkeit = neuigkeit_controller.update_neuigkeit(tenant_id, id, body)
    return response(200, neuigkeit.to_json())


@app.get('/api/neuigkeit/<id>')
def get(id):
    event = app.current_event
    tenant_id = extract_tenant(event)
    neuigkeit = neuigkeit_controller.get_neuigkeit(tenant_id, id)
    if neuigkeit:
        return response(200, neuigkeit.to_json())
    else:
        return empty_response(404)


@app.get('/api/neuigkeit')
def getAll():
    event = app.current_event
    tenant_id = extract_tenant(event)
    stichtag = extract_stichtag(event)
    neuigkeiten = neuigkeit_controller.get_neuigkeiten(tenant_id, stichtag)
    body = to_json_array(list(map(NeuigkeitDTO.to_json, neuigkeiten)))
    return response(200, body)


@app.delete('/api/neuigkeit/<id>')
def delete(id):
    event = app.current_event
    tenant_id = extract_tenant(event)
    deleted = neuigkeit_controller.delete_neuigkeit(tenant_id, id)
    if deleted:
        return empty_response(204)
    else:
        return empty_response(404)


@app.exception_handler(ValidationException)
def handle_http_exception(exception: ValidationException):
    return response(exception.http_status, exception.to_json())
