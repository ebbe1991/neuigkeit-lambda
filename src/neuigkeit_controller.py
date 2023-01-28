from neuigkeit_dto import NeuigkeitDTO, create
from http_exception import ValidationException
import dynamo_db_service


def create_neuigkeit(tenant_id: str, dto: dict) -> NeuigkeitDTO:
    neuigkeit = create(dto)
    dynamo_db_service.put_neuigkeit(tenant_id, neuigkeit)
    return neuigkeit


def update_neuigkeit(tenant_id: str, id: str, dto: dict) -> NeuigkeitDTO:
    dto.update({'id': id})
    neuigkeit = create(dto)
    to_update = get_neuigkeit(tenant_id, id)
    if to_update:
        dynamo_db_service.put_neuigkeit(tenant_id, neuigkeit)
        return neuigkeit
    else:
        raise ValidationException(f"unknown id '{id}' (tenant='{tenant_id}') to update.")


def get_neuigkeit(tenant_id: str, id: str) -> NeuigkeitDTO:
    item = dynamo_db_service.get_neuigkeit(tenant_id, id)
    if item:
        neuigkeit = create(item)
        return neuigkeit
    else:
        return None


def get_neuigkeiten(tenant_id: str) -> list[NeuigkeitDTO]:
    neuigkeiten = []
    items = dynamo_db_service.get_neuigkeiten(tenant_id)
    for item in items:
        neuigkeit = create(item)
        neuigkeiten.append(neuigkeit)
    return neuigkeiten


def delete_neuigkeit(tenant_id: str, id: str) -> bool:
    neuigkeit = get_neuigkeit(tenant_id, id)
    if neuigkeit:
        dynamo_db_service.delete_neuigkeit(tenant_id, id)
        return True
    else:
        return False
