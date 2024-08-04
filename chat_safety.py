import os

import azure.identity
import openai
from dotenv import load_dotenv

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST")

if API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = openai.AzureOpenAI(
        api_version=os.getenv("AZURE_OPENAI_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_ad_token_provider=token_provider,
    )
    MODEL_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")
elif API_HOST == "ollama":
    client = openai.OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="nokeyneeded",
    )
    MODEL_NAME = os.getenv("OLLAMA_MODEL")
else:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_KEY"))
    MODEL_NAME = os.getenv("OPENAI_MODEL")

try:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.7,
        max_tokens=100,
        n=1,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that makes lots of cat references and uses emojis.",
            },
            {"role": "user", "content": "Write a haiku about tuna"},
        ],
    )
    print("Response: ")
    print(response.choices[0].message.content)
except openai.APIError as error:
    if error.code == "content_filter":
        print("We detected a content safety violation. Please remember our code of conduct.")
