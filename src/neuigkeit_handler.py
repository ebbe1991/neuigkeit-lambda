from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
import neuigkeit_controller
from neuigkeit_controller import NeuigkeitDTO
from handler_util import extractBody, extractId, extractTenant, response, emptyResponse
from http_exception import ValidationException
import json
app = APIGatewayHttpResolver()


def handle(event: dict, context: dict):
    return app.resolve(event, context)


@app.post('/api/neuigkeit')
def post():
    event = app.current_event
    tenant_id = extractTenant(event)
    body = extractBody(event)
    neuigkeit = neuigkeit_controller.create_neuigkeit(tenant_id, body)
    return response(201, neuigkeit.to_json())


@app.put('/api/neuigkeit/{id}')
def put():
    event = app.current_event
    tenant_id = extractTenant(event)
    id = extractId(event)
    body = extractBody(event)
    neuigkeit = neuigkeit_controller.update_neuigkeit(tenant_id, id, body)
    return response(200, neuigkeit.to_json())


@app.get('/api/neuigkeit/{id}')
def get():
    event = app.current_event
    tenant_id = extractTenant(event)
    id = extractId(event)
    neuigkeit = neuigkeit_controller.get_neuigkeit(tenant_id, id)
    if neuigkeit:
        return response(200, neuigkeit.to_json())
    else:
        return emptyResponse(404)


@app.get('/api/neuigkeit')
def getAll():
    event = app.current_event
    tenant_id = extractTenant(event)
    neuigkeiten = neuigkeit_controller.get_neuigkeiten(tenant_id)
    return response(200, json.dumps(neuigkeiten, default=NeuigkeitDTO.to_json))


@app.delete('/api/neuigkeit/{id}')
def delete():
    event = app.current_event
    tenant_id = extractTenant(event)
    id = extractId(event)
    deleted = neuigkeit_controller.delete_neuigkeit(tenant_id, id)
    if deleted:
        return emptyResponse(204)
    else:
        return emptyResponse(404)


@app.exception_handler(ValidationException)
def handle_http_exception(exception: ValidationException):
    return response(exception.http_status, exception.to_json())
