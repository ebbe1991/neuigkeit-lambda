import uuid
import json
import os
from datetime import date
from lambda_utils.exception import ValidationException
from lambda_utils.validation import check_required_field
from lambda_utils.ttl import compute_ttl_for_date
from lambda_utils.env_utils import getenv_as_boolean


def create(item: dict):
    betreff = item.get('betreff')
    check_required_field(betreff, 'betreff')
    nachricht = item.get('nachricht')
    check_required_field(nachricht, 'nachricht')
    gueltigVon = item.get('gueltigVon')
    gueltigBis = item.get('gueltigBis')
    return NeuigkeitDTO(
        betreff,
        nachricht,
        None if gueltigVon is None else fromisoformat(gueltigVon),
        None if gueltigBis is None else fromisoformat(gueltigBis),
        item.get('id')
    )


def fromisoformat(d: str):
    try:
        return date.fromisoformat(d)
    except ValueError as ex:
        raise ValidationException(ex.args[0])


class NeuigkeitDTO:

    def __init__(self, betreff: str, nachricht: str, gueltigVon: date, gueltigBis: date, id: str = None):
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())
        self.betreff = betreff
        self.nachricht = nachricht
        self.gueltigVon = gueltigVon
        self.gueltigBis = gueltigBis
        self.ttl = compute_ttl_for_date(gueltigBis, 7) if getenv_as_boolean(
            'TTL_FEATURE_ACTIVE', True) else None

    def to_json(self):
        return json.dumps(self.__dict__, cls=NeuigkeitDTOEncoder)


class NeuigkeitDTOEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        else:
            return super().default(obj)
