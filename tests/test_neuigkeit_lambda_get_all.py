import json
from src import neuigkeit_controller
from src import neuigkeit_handler
from tests.helper import event, extract_body, extract_status_code, lambda_response, DEFAULT_TENANT_ID


def test_get_neuigkeiten_ok(lambda_context, dynamodb_table):
    item1 = {
        'betreff': "Test",
        "nachricht": "Eine Testnachricht",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    item2 = {
        'betreff': "Test2",
        "nachricht": "Eine Testnachricht",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    neuigkeit_controller.create_neuigkeit(DEFAULT_TENANT_ID, item1)
    neuigkeit_controller.create_neuigkeit(DEFAULT_TENANT_ID, item2)

    response = neuigkeit_handler.handle(
        event('/api/neuigkeit', 'GET'), lambda_context)
    body = extract_body(response)

    assert extract_status_code(response) == 200
    assert len(body) == 2


def test_get_neuigkeiten_with_stichtag_ok(lambda_context, dynamodb_table):
    item1 = {
        'betreff': "Test",
        "nachricht": "Eine Testnachricht",
        "gueltigVon": "2022-01-01",
        "gueltigBis": "2022-02-01"
    }
    item2 = {
        'betreff': "Test2",
        "nachricht": "Eine Testnachricht",
        "gueltigVon": "2023-01-01",
        "gueltigBis": "2023-02-01"
    }
    neuigkeit_controller.create_neuigkeit(DEFAULT_TENANT_ID, item1)
    item2023 = neuigkeit_controller.create_neuigkeit(DEFAULT_TENANT_ID, item2)

    response = neuigkeit_handler.handle(
        event('/api/neuigkeit', 'GET', queryParameters={"stichtag": "2023-01-25"}), lambda_context)
    body = extract_body(response)

    assert extract_status_code(response) == 200
    assert len(body) == 1
    assert json.dumps(body[0]) == item2023.to_json()


def test_get_neuigkeiten_empty_ok(lambda_context, dynamodb_table):
    response = neuigkeit_handler.handle(
        event('/api/neuigkeit', 'GET'), lambda_context)
    body = extract_body(response)

    assert extract_status_code(response) == 200
    assert len(body) == 0


def test_get_neuigkeiten_without_tenant_id_not_ok(lambda_context, dynamodb_table):
    headers = {
        'Content-Type': 'application/json'
    }
    response = neuigkeit_handler.handle(
        event('/api/neuigkeit', 'GET', None, None, headers), lambda_context)

    assert response == lambda_response(400, json.dumps(
        {'error_text': 'tenant not present.'}))
