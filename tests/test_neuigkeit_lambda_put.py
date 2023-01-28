import json
from datetime import date
from src import neuigkeit_controller

from src import neuigkeit_handler
from src.neuigkeit_dto import NeuigkeitDTO
from tests.helper import event, lambda_response, DEFAULT_TENANT_ID


def test_update_neuigkeit_ok(lambda_context, dynamodb_table):
    item = {
        'betreff': "Test",
        "nachricht": "Eine Testnachricht",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    createdNeuigkeit = neuigkeit_controller.create_neuigkeit(
        DEFAULT_TENANT_ID, item
    )

    pathParameters = {
        "id": createdNeuigkeit.id
    }
    itemUpdate = {
        'betreff': "Test",
        "nachricht": "Eine Testnachricht (aktualisiert)",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    response = neuigkeit_handler.handle(event(
        '/api/neuigkeit/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(200, NeuigkeitDTO(
        "Test", "Eine Testnachricht (aktualisiert)", date.fromisoformat("2022-01-01"), date.fromisoformat("2022-02-01"), createdNeuigkeit.id).to_json())


def test_update_neuigkeit_required_field_to_null_not_ok(lambda_context, dynamodb_table):
    item = {
        'betreff': "Test",
        "nachricht": "Eine Testnachricht",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    createdNeuigkeit = neuigkeit_controller.create_neuigkeit(
        DEFAULT_TENANT_ID, item
    )

    pathParameters = {
        "id": createdNeuigkeit.id
    }
    itemUpdate = {
        'betreff': "",
        "nachricht": "Eine Testnachricht (aktualisiert)",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    response = neuigkeit_handler.handle(event(
        '/api/neuigkeit/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "'betreff' is missing."}))


def test_update_neuigkeit_with_unknown_id_not_ok(lambda_context, dynamodb_table):
    pathParameters = {
        "id": 'unknown'
    }
    itemUpdate = {
        'betreff': "Test",
        "nachricht": "Eine Testnachricht (aktualisiert)",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    response = neuigkeit_handler.handle(event(
        '/api/neuigkeit/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "unknown id 'unknown' (tenant='mytenant1') to update."}))


def test_update_neuigkeit_set_null_value(lambda_context, dynamodb_table):
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

    itemUpdate = {
        'betreff': "Test",
        "nachricht": "Eine Testnachricht (aktualisiert)",
        "gueltigVon": "2022-01-01"
    }
    response = neuigkeit_handler.handle(event(
        '/api/neuigkeit/{id}', 'PUT', json.dumps(itemUpdate), pathParameters), lambda_context)

    assert response == lambda_response(200, NeuigkeitDTO(
        "Test", "Eine Testnachricht (aktualisiert)", date.fromisoformat("2022-01-01"), None, createdNeuigkeit.id).to_json())


def test_update_neuigkeit_without_body_not_ok(lambda_context, dynamodb_table):
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

    response = neuigkeit_handler.handle(
        event('/api/neuigkeit/{id}', 'PUT', None, pathParameters), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'body not present.'}))


def test_update_neuigkeit_without_id_not_ok(lambda_context, dynamodb_table):
    item = {
        'betreff': "Test",
        "nachricht": "Eine Testnachricht",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    neuigkeit_controller.create_neuigkeit(
        DEFAULT_TENANT_ID, item)

    pathParameters = {
        "id": ''
    }

    response = neuigkeit_handler.handle(
        event('/api/neuigkeit/{id}', 'PUT', json.dumps(item), pathParameters), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'id not present.'}))


def test_update_neuigkeit_without_tenant_id_not_ok(lambda_context, dynamodb_table):
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
    itemUpdate = {
        'betreff': "Test",
        "nachricht": "Eine Testnachricht (aktualisiert)",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    response = neuigkeit_handler.handle(event(
        '/api/neuigkeit/{id}', 'PUT', json.dumps(itemUpdate), pathParameters, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
