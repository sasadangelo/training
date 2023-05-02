curl -X POST \
  http://localhost:5000/athlete \
  -H 'Content-Type: application/json' \
  -d '{
    "id": "2",
    "firstname": "Salvatore",
    "lastname": "DAngelo",
    "city": "Roma",
    "state": "Lazio",
    "country": "Italia",
    "sex": "M"
}'
