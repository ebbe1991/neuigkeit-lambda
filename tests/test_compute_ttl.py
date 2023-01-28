from neuigkeit_dto import NeuigkeitDTO
from datetime import date


def test_compute_none():
    gueltigBis = None
    neuigkeit_dto = NeuigkeitDTO("Betreff", "Nachricht", None, gueltigBis)
    assert neuigkeit_dto.ttl is None


def test_compute_ttl():
    gueltigBis = date.fromisoformat("2023-01-27")
    neuigkeit_dto = NeuigkeitDTO("Betreff", "Nachricht", None, gueltigBis)
    assert neuigkeit_dto.ttl == 1675382400
