import uuid
import json
from datetime import datetime, timezone
import os
from datetime import date, timedelta
from http_exception import ValidationException


def create(item: dict):
    betreff = item.get('betreff')
    checkRequiredField(betreff, 'betreff')
    nachricht = item.get('nachricht')
    checkRequiredField(nachricht, 'nachricht')
    gueltigVon = item.get('gueltigVon')
    gueltigBis = item.get('gueltigBis')
    return NeuigkeitDTO(
        betreff,
        nachricht,
        None if gueltigVon is None else fromisoformat(gueltigVon),
        None if gueltigBis is None else fromisoformat(gueltigBis),
        item.get('id')
    )


def checkRequiredField(field, fieldname: str):
    if field is None or len(field) <= 0:
        raise ValidationException(f"'{fieldname}' is missing.")


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
        self.ttl = compute_ttl(gueltigBis)

    def to_json(self):
        return json.dumps(self.__dict__, cls=NeuigkeitDTOEncoder)


def compute_ttl(gueltigBis: date) -> int:
    ttl_feature_active = int(os.getenv('TTL_FEATURE_ACTIVE', 1)) == 1
    if ttl_feature_active == 1 and gueltigBis:
        local_date = gueltigBis + timedelta(days=7)
        utc_date = datetime(year=local_date.year,
                            month=local_date.month,
                            day=local_date.day,
                            tzinfo=timezone.utc)
        return int(utc_date.timestamp())
    else:
        return None


class NeuigkeitDTOEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        else:
            return super().default(obj)
