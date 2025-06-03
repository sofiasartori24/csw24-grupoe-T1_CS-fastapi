import json
from utils import process_data, validate_input

def lambda_handler(event, context):
    # Log do evento recebido (equivalente a console.log em JS)
    print("Received event:", json.dumps(event, indent=2))

    # Validação (como no validateInput)
    if not validate_input(event):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid input"})
        }

    # Processamento (como em processData)
    processed = process_data(event)

    # Exemplo de resposta
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello from AWS Lambda (Python)!",
            "processedInput": processed
        })
    }
