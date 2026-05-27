Start with
```bash
py -3.13 -m venv .venv

.\.venv\Scripts\Activate.ps1
python --version

.\.venv\Scripts\activate.ps1 
pip install -r requirements.txt

python -m pip install --upgrade pip
python -m pip install {package_name}

pip install python-dotenv aiohttp azure-identity openai

pip list
python -c "import sys; print('\n'.join(sorted(sys.modules.keys())))"


# Remove the broken .venv
Remove-Item -Recurse -Force .venv

# Create a fresh virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install packages
pip install -r labfiles/foundry-chat/python/chat-app/requirements.txt
```

In the Command Palette, use the command python:select interpreter

https://microsoftlearning.github.io/mslearn-ai-studio/Instructions/Exercises/03-foundry-sdk.html

https://github.com/microsoftlearning/mslearn-ai-studio

Environment variables used by chat scripts (`chat-app/chat-app.py` and `chat-app/chat-async.py`):

```env
AZURE_OPENAI_ENDPOINT=https://<your-foundry-resource>.openai.azure.com/openai/v1/
MODEL_DEPLOYMENT=<your-model-deployment-name>

# Option 1 (default): Microsoft Entra ID / DefaultAzureCredential
FOUNDRY_AUTH_MODE=credential

# Option 2: API key authentication from .env
# FOUNDRY_AUTH_MODE=key
# FOUNDRY_API_KEY=<your-foundry-api-key>
```

Notes:
- If `FOUNDRY_AUTH_MODE` is not set, it defaults to `credential`.
- In `key` mode, `FOUNDRY_API_KEY` is required (or `AZURE_OPENAI_API_KEY` as fallback).
