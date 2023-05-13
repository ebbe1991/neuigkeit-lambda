import os
import boto3
from neuigkeit_dto import NeuigkeitDTO
from boto3.dynamodb.conditions import Key


def get_neuigkeiten_table():
    dynamodb = boto3.resource('dynamodb')
    table_name = os.getenv('NEUIGKEIT_TABLE_NAME')
    return dynamodb.Table(table_name)


def put_neuigkeit(tenant_id: str, neuigkeit: NeuigkeitDTO):
    table = get_neuigkeiten_table()
    table.put_item(
        Item={
            'tenant-id': tenant_id,
            'id': neuigkeit.id,
            'betreff': neuigkeit.betreff,
            'nachricht': neuigkeit.nachricht,
            'introtext': neuigkeit.introtext,
            'gueltigVon': neuigkeit.gueltigVon.isoformat() if neuigkeit.gueltigVon is not None else None,
            'gueltigBis': neuigkeit.gueltigBis.isoformat() if neuigkeit.gueltigBis is not None else None,
            'ttl': neuigkeit.ttl
        }
    )


def get_neuigkeit(tenant_id: str, id: str):
    table = get_neuigkeiten_table()
    result = table.get_item(
        Key={
            "tenant-id": tenant_id,
            "id": id
        }
    )
    return result.get('Item')


def get_neuigkeiten(tenant_id: str) -> list:
    table = get_neuigkeiten_table()
    response = table.query(
        KeyConditionExpression=Key('tenant-id').eq(tenant_id)
    )
    return response['Items']

def delete_neuigkeit(tenant_id: str, id: str):
    table = get_neuigkeiten_table()
    table.delete_item(
        Key={
            "tenant-id": tenant_id,
            "id": id
        }
    )
