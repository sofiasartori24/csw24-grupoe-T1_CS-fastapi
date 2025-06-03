import json
from utils import process_data, validate_input

def lambda_handler(event, context):
    # Log do evento recebido
    print("Received event:", json.dumps(event, indent=2))

    # Validar entrada
    if not validate_input(event):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid input"})
        }

    # Processar os dados
    processed = process_data(event)

    # Resposta de exemplo
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello from AWS Lambda (Python)!",
            "processedInput": processed
        })
    }
