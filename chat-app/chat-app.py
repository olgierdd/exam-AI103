import os
from dotenv import load_dotenv

# import namespaces
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


def create_openai_client(azure_openai_endpoint: str):
    auth_mode = os.getenv("FOUNDRY_AUTH_MODE", "credential").strip().lower()

    if auth_mode in ("key", "api_key", "apikey"):
        foundry_api_key = os.getenv("FOUNDRY_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
        if not foundry_api_key:
            raise ValueError(
                "FOUNDRY_AUTH_MODE is 'key' but no API key was found. "
                "Set FOUNDRY_API_KEY (or AZURE_OPENAI_API_KEY) in .env."
            )
        return OpenAI(base_url=azure_openai_endpoint, api_key=foundry_api_key)

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://ai.azure.com/.default"
    )
    return OpenAI(base_url=azure_openai_endpoint, api_key=token_provider)


def main(): 
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings 
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        if not azure_openai_endpoint or not model_deployment:
            raise ValueError("Set AZURE_OPENAI_ENDPOINT and MODEL_DEPLOYMENT in .env.")

        # Initialize the OpenAI client
        openai_client = create_openai_client(azure_openai_endpoint)


        # Loop until the user wants to quit
        # Track responses
        last_response_id = None
        
        while True:
            input_text = input('\nEnter a prompt (or type "quit" to exit): ')
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            # Get a response
            stream = openai_client.responses.create(
                        model=model_deployment,
                        instructions="You are a helpful AI assistant that answers questions and provides information.",
                        input=input_text,
                        previous_response_id=last_response_id,
                        stream=True
            )
            for event in stream:
                if event.type == "response.output_text.delta":
                    print(event.delta, end="")
                elif event.type == "response.completed":
                    last_response_id = event.response.id
            print()
            

    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()
