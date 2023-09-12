curl -X PUT \
  http://localhost:5000/athlete/$1 \
  -H 'Content-Type: application/json' \
  -d '{
    "id": 2,
    "firstname": "Salvatore",
    "lastname": "Pluto",
    "city": "Sarno",
    "state": "Lazio",
    "country": "Italia",
    "sex": "M"
}'
