# Custom GPT Setup for QT-Ride

Since OpenAI has deprecated the plugin system, we now use **Custom GPTs with Actions** to integrate QT-Ride with ChatGPT.

## 🚀 **Setup Instructions**

### **Step 1: Start the MCP Wrapper**
```bash
# Make sure you're in the project directory
cd QT-ride-Mac

# Activate virtual environment
source venv/bin/activate

# Start the MCP wrapper
cd mcp_service
uvicorn main:app --reload --port 5010
```

### **Step 2: Create a Custom GPT**

1. **Go to ChatGPT**: Open [ChatGPT](https://chat.openai.com)
2. **Access GPT Builder**: Click on your profile → "My GPTs" → "Create a GPT"
3. **Configure the GPT**:
   - **Name**: "QT-Ride Assistant"
   - **Description**: "I help you search for rides, book transportation, and manage your QT-Ride account."
   - **Instructions**: 
     ```
     You are a helpful assistant for QT-Ride, a ride-sharing platform. You can help users:
     - Log into their accounts
     - Search for available rides
     - Book rides
     - View their profile information
     
     Always be friendly and provide clear information about ride options, prices, and booking confirmations.
     ```

### **Step 3: Add Actions**

1. **Go to the "Configure" tab**
2. **Scroll down to "Actions"**
3. **Click "Create new action"**
4. **Import Schema**: 
   - Copy the content from `http://localhost:5010/custom_gpt_schema.json`
   - Paste it into the schema field
5. **Set Authentication**: Choose "None" (for development)
6. **Test the Action**: Use the test interface to verify connectivity

### **Step 4: Test Your Custom GPT**

Try these example prompts:

```
"Help me search for rides from New York to Boston"

"I want to log into my QT-Ride account with email test@example.com"

"Book ride ID 123 for user 456"

"Show me the profile for user 789"
```

---

## 🛠 **Alternative: OpenAI API with Function Calling**

If you prefer programmatic access, you can use the OpenAI API directly:

### **Python Example**:

```python
import openai
import json

# Configure OpenAI client
client = openai.OpenAI(api_key="your-api-key-here")

# Define functions that correspond to your MCP wrapper endpoints
functions = [
    {
        "name": "search_rides",
        "description": "Search for available rides",
        "parameters": {
            "type": "object",
            "properties": {
                "from": {"type": "string", "description": "Origin location"},
                "to": {"type": "string", "description": "Destination location"},
                "date": {"type": "string", "description": "Travel date"}
            },
            "required": ["from", "to"]
        }
    },
    {
        "name": "book_ride",
        "description": "Book a ride",
        "parameters": {
            "type": "object",
            "properties": {
                "ride_id": {"type": "integer", "description": "ID of the ride to book"},
                "user_id": {"type": "integer", "description": "ID of the user"}
            },
            "required": ["ride_id", "user_id"]
        }
    }
]

# Example conversation
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Find rides from NYC to Boston"}
    ],
    functions=functions,
    function_call="auto"
)

# Handle function calls
if response.choices[0].message.function_call:
    function_name = response.choices[0].message.function_call.name
    function_args = json.loads(response.choices[0].message.function_call.arguments)
    
    # Call your MCP wrapper endpoint
    if function_name == "search_rides":
        # Make HTTP request to http://localhost:5010/search
        pass
```

---

## 🔧 **Troubleshooting**

### **Common Issues**:

1. **CORS Errors**: 
   - Make sure the MCP wrapper is running with CORS enabled
   - Check that `http://localhost:5010` is accessible

2. **Schema Import Fails**:
   - Verify the JSON schema is valid
   - Check that the MCP wrapper is serving the schema at `/custom_gpt_schema.json`

3. **Actions Don't Work**:
   - Ensure all microservices are running
   - Test endpoints manually with curl first
   - Check the ChatGPT action logs for error details

### **Debug Commands**:
```bash
# Test MCP wrapper
curl http://localhost:5010/health

# Test schema endpoint
curl http://localhost:5010/custom_gpt_schema.json

# Test a specific action
curl -X POST http://localhost:5010/login \
  -H 'Content-Type: application/json' \
  -d '{"email": "test@example.com", "password": "password"}'
```

---

## 📋 **Next Steps**

1. **Production Deployment**: 
   - Deploy to a public server with HTTPS
   - Update the schema URL to your production endpoint
   - Set up proper authentication

2. **Enhanced Features**:
   - Add more sophisticated ride search filters
   - Implement real-time booking updates
   - Add payment processing integration

3. **Share Your GPT**:
   - Once working, you can make your Custom GPT public
   - Share it with other QT-Ride users

---

## 🎯 **Key Benefits of Custom GPTs**

- ✅ **No Plugin Deprecation**: Uses current OpenAI technology
- ✅ **Better Integration**: More natural conversation flow
- ✅ **Easier Setup**: No complex plugin registration
- ✅ **Customizable**: Full control over GPT behavior and personality
- ✅ **Shareable**: Can be shared with other users

Your QT-Ride MCP wrapper is now ready for the modern ChatGPT ecosystem! 🚀 