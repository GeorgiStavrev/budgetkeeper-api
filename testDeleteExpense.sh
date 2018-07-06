curl --header "Content-Type: application/json" \
  --request DELETE \
  --data '{"name":"test expense modified","date":"2018-07-04T12:15:41T00:00:00", "sum": 11.0}' \
  http://localhost:8080/expenses/1