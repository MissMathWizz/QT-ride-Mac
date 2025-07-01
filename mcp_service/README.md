# MCP Wrapper for QT-Ride-Mac

This service acts as an API gateway for the QT-Ride microservices, providing a unified interface for authentication, ride search, booking, and user profile access.

## How to Run

### Prerequisites
1. Make sure all microservices (auth_service, search_service, offer_service, user_profile) are running on their respective ports.
2. Ensure you have the Python 3.11 virtual environment activated.

### Starting the MCP Service

**Method 1: HTTP (Basic Testing)**
```bash
# Navigate to the MCP service directory
cd /Users/yw/QT-ride-Mac-test2/QT-ride-Mac/mcp_service

# Activate the virtual environment
source /Users/yw/QT-ride-Mac-test2/venv_py311/bin/activate

# Start the service using Python
python -c "
import uvicorn
print('Starting MCP service...')
uvicorn.run('main:app', host='127.0.0.1', port=5010, log_level='info')
"
```

**Method 2: HTTPS on Port 443 (Required for ChatGPT Custom GPT)**
```bash
# Navigate to the MCP service directory
cd /Users/yw/QT-ride-Mac-test2/QT-ride-Mac/mcp_service

# Activate the virtual environment
source /Users/yw/QT-ride-Mac-test2/venv_py311/bin/activate

# Create SSL certificate (first time only)
openssl genrsa -out localhost.key 2048
openssl req -new -x509 -key localhost.key -out localhost.crt -days 365 -subj '/CN=localhost'

# Start the service with HTTPS on port 443 (requires sudo)
sudo $VIRTUAL_ENV/bin/python start_https.py
```

**Method 3: HTTPS on Port 5010 (Alternative)**
```bash
# Navigate to the MCP service directory
cd /Users/yw/QT-ride-Mac-test2/QT-ride-Mac/mcp_service

# Activate the virtual environment
source /Users/yw/QT-ride-Mac-test2/venv_py311/bin/activate

# Start the service with HTTPS on port 5010
python -c "
import uvicorn
print('Starting MCP service with HTTPS...')
uvicorn.run('main:app', host='127.0.0.1', port=5010, log_level='info', 
           ssl_keyfile='localhost.key', ssl_certfile='localhost.crt')
"
```

**Method 2: Using uvicorn command line**
```bash
# Navigate to the MCP service directory
cd /Users/yw/QT-ride-Mac-test2/QT-ride-Mac/mcp_service

# Activate the virtual environment
source /Users/yw/QT-ride-Mac-test2/venv_py311/bin/activate

# Start the service
$VIRTUAL_ENV/bin/python -m uvicorn main:app --host 127.0.0.1 --port 5010
```

### Verifying the Service

**For HTTP (Method 1):**
After starting, you should see:
```
Starting MCP service...
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:5010 (Press CTRL+C to quit)
```

Test the service:
```bash
curl http://127.0.0.1:5010/
```

**For HTTPS on Port 443 (Method 2):**
After starting, you should see:
```
🚀 Starting MCP service on HTTPS port 443...
   This will be accessible at: https://localhost
   Press Ctrl+C to stop
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on https://127.0.0.1:443 (Press CTRL+C to quit)
```

Test the service:
```bash
curl -k https://localhost/
```

**For HTTPS on Port 5010 (Method 3):**
After starting, you should see:
```
Starting MCP service with HTTPS...
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on https://127.0.0.1:5010 (Press CTRL+C to quit)
```

Test the service:
```bash
curl -k https://127.0.0.1:5010/
```

**Expected response:**
```json
{"message": "QT-Ride MCP Wrapper is running", "endpoints": ["/login", "/search", "/book", "/profile/{user_id}"]}
```

## Endpoints

- `POST /login` — User login (forwards to auth_service)
- `GET /search` — Search for rides (forwards to search_service)
- `POST /book` — Book a ride (forwards to offer_service)
- `GET /profile/{user_id}` — Get user profile (forwards to user_profile)

## Example Usage

```bash
curl -X POST http://127.0.0.1:5010/login -H 'Content-Type: application/json' -d '{"email": "test@example.com", "password": "testpass"}'

curl 'http://127.0.0.1:5010/search?from=NYC&to=Boston'

curl -X POST http://127.0.0.1:5010/book -H 'Content-Type: application/json' -d '{"ride_id": 123, "user_id": 1}'
```

## Troubleshooting

### Common Issues

**1. "Error loading ASGI app. Could not import module 'main'"**
- **Cause**: You're not in the correct directory or the virtual environment isn't activated
- **Solution**: Make sure you're in `/Users/yw/QT-ride-Mac-test2/QT-ride-Mac/mcp_service` and the virtual environment is activated

**2. "Address already in use" (Port 5010)**
- **Cause**: Another process is using port 5010
- **Solution**: 
  ```bash
  # Find the process using port 5010
  lsof -ti:5010
  
  # Kill the process (replace XXXX with the process ID)
  kill -9 XXXX
  ```

**3. Shell command parsing issues with `&&` operators**
- **Cause**: Complex shell commands can get mangled
- **Solution**: Use separate commands instead of chaining with `&&`

**4. Background process not starting**
- **Cause**: Background processes (`&`) may not work reliably in some terminal environments
- **Solution**: Run the service in foreground using Method 1 (Python directly)

**5. ChatGPT Custom GPT Errors**
- **Error**: "None of the provided servers is under the root origin https://localhost"
- **Cause**: ChatGPT requires the server URL to be exactly `https://localhost` (no port number)
- **Solution**: Use Method 2 (HTTPS on port 443) to run the service on `https://localhost`

- **Error**: "('openapi',): Input should be '3.1.0'"
- **Cause**: ChatGPT requires OpenAPI version 3.1.0 exactly
- **Solution**: The schema has been updated to use OpenAPI 3.1.0

- **Error**: SSL certificate warnings in browser
- **Cause**: Self-signed certificate for localhost
- **Solution**: This is normal for development. Click "Advanced" → "Proceed to localhost" in your browser

### Dependencies
The following packages are required and should be installed in the virtual environment:
- `fastapi==0.115.14`
- `uvicorn==0.35.0`
- `httpx==0.28.1`

---

This service is also ready to be exposed as an OpenAI Plugin (see plugin manifest and OpenAPI spec). 