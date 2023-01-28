import json
from src import neuigkeit_controller

from src import neuigkeit_handler
from tests.helper import event, lambda_response, DEFAULT_TENANT_ID


def test_get_neuigkeit_not_found(lambda_context, dynamodb_table):
    pathParameters = {
        "id": "unknown_id"
    }
    response = neuigkeit_handler.handle(event(
        '/api/neuigkeit/{id}', 'GET', None, pathParameters), lambda_context)

    assert response == lambda_response(404)


def test_get_neuigkeit_ok(lambda_context, dynamodb_table):
    item = {
        'betreff': "Test",
        "nachricht": "Eine Testnachricht",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    createdNeuigkeit = neuigkeit_controller.create_neuigkeit(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdNeuigkeit.id
    }
    response = neuigkeit_handler.handle(event(
        '/api/neuigkeit/{id}', 'GET', None, pathParameters), lambda_context)

    assert response == lambda_response(200, createdNeuigkeit.to_json())

def test_get_neuigkeit_without_tenant_id_not_ok(lambda_context, dynamodb_table):
    headers = {
        'Content-Type': 'application/json'
    }
    item = {
        'betreff': "Test",
        "nachricht": "Eine Testnachricht",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    createdNeuigkeit = neuigkeit_controller.create_neuigkeit(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": createdNeuigkeit.id
    }
    response = neuigkeit_handler.handle(event(
        '/api/neuigkeit/{id}', 'GET', None, pathParameters, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
