import json
from datetime import date

from src import neuigkeit_handler
from src.neuigkeit_dto import NeuigkeitDTO
from tests.helper import event, lambda_response, extract_id


def test_create_neuigkeit_ok(lambda_context, dynamodb_table):
    item = {
        'betreff': "Test",
        "nachricht": "Eine Testnachricht",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    response = neuigkeit_handler.handle(
        event('/api/neuigkeit', 'POST', json.dumps(item)), lambda_context)

    id = extract_id(response)

    assert id is not None
    assert response == lambda_response(201, NeuigkeitDTO(
        "Test", "Eine Testnachricht", date.fromisoformat("2022-01-01"), date.fromisoformat("2022-02-01"), id).to_json())


def test_create_neuigkeit_invalid_dateformat_bad_request(lambda_context, dynamodb_table):
    item = {
        'betreff': "Test",
        "nachricht": "Eine Testnachricht",
        "gueltigVon": "2022.01-01",
        "gueltigBis": "2022-02-01"
    }
    response = neuigkeit_handler.handle(
        event('/api/neuigkeit', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': "Invalid isoformat string: '2022.01-01'"}))


def test_create_neuigkeit_missing_field_betreff_bad_request(lambda_context, dynamodb_table):
    item = {
        "nachricht": "Eine Testnachricht",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    response = neuigkeit_handler.handle(
        event('/api/neuigkeit', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(
        400, json.dumps({'error_text': "'betreff' is missing."}))


def test_create_neuigkeit_missing_field_nachricht_bad_request(lambda_context, dynamodb_table):
    item = {
        "betreff": "Ein Betreff",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    response = neuigkeit_handler.handle(
        event('/api/neuigkeit', 'POST', json.dumps(item)), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': "'nachricht' is missing."}))


def test_create_neuigkeit_without_optional_parameters_ok(lambda_context, dynamodb_table):
    item = {
        'betreff': "Test",
        "nachricht": "Eine Testnachricht"
    }
    response = neuigkeit_handler.handle(
        event('/api/neuigkeit', 'POST', json.dumps(item)), lambda_context)
    id = extract_id(response)

    assert id is not None
    assert response == lambda_response(201, NeuigkeitDTO(
        "Test", "Eine Testnachricht", None, None, id).to_json())



def test_create_neuigkeit_without_body_not_ok(lambda_context, dynamodb_table):
    response = neuigkeit_handler.handle(
        event('/api/neuigkeit', 'POST'), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'body not present.'}))

def test_create_neuigkeit_without_tenant_id_not_ok(lambda_context, dynamodb_table):
    headers = {
        'Content-Type': 'application/json'
    }
    item = {
        'betreff': "Test",
        "nachricht": "Eine Testnachricht"
    }
    response = neuigkeit_handler.handle(
        event('/api/neuigkeit', 'POST', json.dumps(item), None, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
