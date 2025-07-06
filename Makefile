test-api:
	curl -X POST http://localhost:8000/api/v1/talent-experiences \
	-H "Content-Type: application/json" \
	-d @$${FILE}