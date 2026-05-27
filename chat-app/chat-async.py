import os
from dotenv import load_dotenv

# import namespaces for async
import asyncio
from openai import AsyncOpenAI
from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider


def create_async_openai_client(azure_openai_endpoint: str):
    auth_mode = os.getenv("FOUNDRY_AUTH_MODE", "credential").strip().lower()

    if auth_mode in ("key", "api_key", "apikey"):
        foundry_api_key = os.getenv("FOUNDRY_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
        if not foundry_api_key:
            raise ValueError(
                "FOUNDRY_AUTH_MODE is 'key' but no API key was found. "
                "Set FOUNDRY_API_KEY (or AZURE_OPENAI_API_KEY) in .env."
            )
        return AsyncOpenAI(base_url=azure_openai_endpoint, api_key=foundry_api_key), None

    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(
        credential, "https://ai.azure.com/.default"
    )
    return AsyncOpenAI(base_url=azure_openai_endpoint, api_key=token_provider), credential



async def main(): 

    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings 
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        if not azure_openai_endpoint or not model_deployment:
            raise ValueError("Set AZURE_OPENAI_ENDPOINT and MODEL_DEPLOYMENT in .env.")

        # Initialize an async OpenAI client
        async_client, credential = create_async_openai_client(azure_openai_endpoint)


        # Track responses
        last_response_id = None

        # Loop until the user wants to quit
        while True:
            input_text = input('\nEnter a prompt (or type "quit" to exit): ')
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            # Await an asynchronous response
            response = await async_client.responses.create(
                        model=model_deployment,
                        instructions="You are a helpful AI assistant that answers questions and provides information.",
                        input=input_text,
                        previous_response_id=last_response_id
            )
            assistant_text = response.output_text
            print("Assistant:", assistant_text)
            last_response_id = response.id

            

    except Exception as ex:
        print(ex)

    finally:
        if credential is not None:
            await credential.close()


if __name__ == '__main__': 
    asyncio.run(main())
