# Neuigkeit-Lambda

## Routen

### Neuigkeit 

- POST api/neuigkeit
- GET api/neuigkeit/<id>
- GET api/neuigkeit[?stichtag=YYYY-MM-DD]
- PUT api/neuigkeit/<id>
- DELETE api/neuigkeit/<id>


## Umgebungsvariablen
| Name                    | Beschreibung                                            |
|-------------------------|---------------------------------------------------------|
| NEUIGKEIT_TABLE_NAME    | Name der Neuigkeit DynamoDB-Table                       |
| TTL_FEATURE_ACTIVE      | Flag, ob TTL für die Neuigkeit DynamoDB-Table aktiv ist |