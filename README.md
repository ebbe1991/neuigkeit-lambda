# Neuigkeit-Lambda

Diese AWS-Lambda-Function dient zur Pflege  von Neuigkeiten einer Applikation. Die Neuigkeiten (Betreff + Nachricht) werden in einer DynamoDB mit einer optionalen Gültigkeit hinterlegt. 

Sofern das 'GültigBis' gepflegt ist, werden die Neuigkeiten mit einer TTL in der DynamoDB hinterlegt und nach einem Versatz von 7 Tagen zum 'GültigBis' gelöscht (Feature ist über die Umgebungsvariable 'TTL_FEATURE_ACTIVE' deaktivierbar).

## Voraussetzungen
- Python (3.9)
    - boto3
    - moto
    - pytest
    - aws_lambda_powertools

## Umgebungsvariablen
```sh
TTL_FEATURE_ACTIVE=0|1:int
NEUIGKEIT_TABLE_NAME=*:str
```

## Tests ausführen
```sh
pytest
```


# Api-Dokumentation (wip)

## POST

Erstellt eine Neuigkeit

**URL** : `/api/neuigkeit/`

**Method** : `POST`

**Data constraints**

```json
{
    "betreff": "[Betreff der Neuigkeit]",
    "nachricht": "[Nachricht]",
    "gueltigVon": "[optionaler Gültigkeitsstart der Neuigkeit]",
    "gueltigBis": "[optionales Gültigkeitsende der Neuigkeit]"
}
```

**Data example**

```json
{
    "betreff": "Herzlich Willkommen",
    "nachricht": "Dies ist unsere neue Website! Frohes neues Jahr!",
    "gueltigVon": "2022-01-01",
    "gueltigBis": "2022-15-01"
}
```

### Success Response

**Code** : `201 CREATED`

### Error Response

**Condition** : Wenn 'betreff' und/oder 'nachricht' nicht gefüllt sind.

**Code** : `400 BAD REQUEST`

## PUT

Aktualisiert einer Neuigkeit

**URL** : `/api/neuigkeit/{id}`

**Method** : `PUT`

**Data constraints**

```json
{
    "betreff": "[Betreff der Neuigkeit]",
    "nachricht": "[Nachricht]",
    "gueltigVon": "[optionaler Gültigkeitsstart der Neuigkeit]",
    "gueltigBis": "[optionales Gültigkeitsende der Neuigkeit]"
}
```

**Data example**

```json
{
    "betreff": "Herzlich Willkommen",
    "nachricht": "Dies ist unsere neue Website! Frohes neues Jahr!",
    "gueltigVon": "2022-01-01",
    "gueltigBis": "2022-15-01"
}
```

## Success Response

**Code** : `200 OK`

## Error Response

**Condition** : Wenn 'betreff' und/oder 'nachricht' nicht gefüllt sind.

**Code** : `400 BAD REQUEST`

## GET

Gibt die Neuigkeit zur Id zurück

**URL** : `/api/neuigkeit/{id}`

**Method** : `GET`

## Success Response

**Code** : `200 OK`

## GET

Gibt alle Neuigkeiten zurück

**URL** : `/api/neuigkeit

**Method** : `GET`

## Success Response

**Code** : `200 OK`

## DELETE

Löscht die Neuigkeit zur Id

**URL** : `/api/neuigkeit/{id}`

**Method** : `DELETE`

## Success Response

**Code** : `204 NO CONTENT`

## Error Response

**Condition** : Wenn 'id' nicht gesetzt

**Code** : `400 BAD REQUEST`

**Condition** : Wenn keine Neuigkeit zur 'id' existiert.

**Code** : `404 NOT FOUND`