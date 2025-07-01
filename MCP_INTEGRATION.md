# QT-Ride MCP Wrapper Integration Guide

This guide explains how to use the MCP (Multi-Channel Platform) wrapper for QT-Ride microservices and integrate it with ChatGPT as an OpenAI Plugin.

## Overview

The MCP wrapper (`mcp_service/`) acts as a unified API gateway for all QT-Ride microservices:
- **Auth Service** (Port 5001) - User authentication
- **Search Service** (Port 5002) - Ride searching  
- **Offer Service** (Port 5004) - Ride booking
- **User Profile Service** (Port 5005) - User management
- **MCP Wrapper** (Port 5010) - Unified API gateway

## Quick Start

### 1. Install Dependencies
```bash
# Make sure you're using Python 3.11
python3.11 --version

# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### 2. Start All Services
```bash
# Option 1: Use the convenience script
./start_services.sh

# Option 2: Start services manually in separate terminals
# Terminal 1: Auth Service
cd auth_service && python app.py

# Terminal 2: Search Service  
cd search_service && python app.py

# Terminal 3: Offer Service
cd offer_service && python app.py

# Terminal 4: User Profile Service
cd user_profile && python app.py

# Terminal 5: MCP Wrapper
cd mcp_service && uvicorn main:app --reload --port 5010
```

### 3. Test the MCP Wrapper
```bash
# Check if wrapper is running
curl http://127.0.0.1:5010/

# Check service health
curl http://127.0.0.1:5010/health

# Test login (example)
curl -X POST http://127.0.0.1:5010/login \
  -H 'Content-Type: application/json' \
  -d '{"email": "test@example.com", "password": "password"}'

# Test search (example)
curl 'http://127.0.0.1:5010/search?from=NYC&to=Boston'
```

## OpenAI Plugin Integration

### 1. Plugin Manifest
The MCP wrapper exposes an OpenAI Plugin manifest at:
```
http://127.0.0.1:5010/.well-known/ai-plugin.json
```

### 2. OpenAPI Specification
The API specification is available at:
```
http://127.0.0.1:5010/openapi.yaml
```

### 3. Register with ChatGPT

#### For ChatGPT Plus/Pro Users:
1. Go to ChatGPT settings
2. Navigate to "Beta features" or "Plugins"
3. Click "Develop your own plugin"
4. Enter the plugin URL: `http://127.0.0.1:5010`
5. ChatGPT will automatically discover the manifest and API spec

#### For Development/Testing:
1. Use the ChatGPT Plugin development environment
2. Point to your local MCP wrapper URL
3. Test the plugin functionality

### 4. Using the Plugin in ChatGPT

Once registered, you can use natural language to interact with QT-Ride:

**Examples:**
- "Help me log into QT-Ride with email test@example.com"
- "Search for rides from New York to Boston"
- "Book ride ID 123 for user 456"
- "Show me the profile for user 789"

## API Endpoints

### Authentication
- `POST /login` - User login
  ```json
  {
    "email": "user@example.com",
    "password": "userpassword"
  }
  ```

### Ride Search
- `GET /search?from={origin}&to={destination}` - Search for rides

### Ride Booking
- `POST /book` - Book a ride
  ```json
  {
    "ride_id": 123,
    "user_id": 456
  }
  ```

### User Profile
- `GET /profile/{user_id}` - Get user profile

### System
- `GET /` - API status and available endpoints
- `GET /health` - Service health check

## Architecture

```
ChatGPT/Client
      ↓
MCP Wrapper (Port 5010)
      ↓
┌─────────────────────────────────────┐
│  Auth Service (5001)                │
│  Search Service (5002)              │
│  Offer Service (5004)               │
│  User Profile Service (5005)        │
└─────────────────────────────────────┘
```

## Troubleshooting

### Common Issues

1. **Services not starting**
   - Check if ports are already in use: `lsof -i :5001`
   - Ensure virtual environment is activated
   - Check database permissions and paths

2. **MCP Wrapper can't connect to services**
   - Verify all microservices are running
   - Check service URLs in `mcp_service/main.py`
   - Test individual service endpoints

3. **OpenAI Plugin not working**
   - Ensure MCP wrapper is accessible from ChatGPT
   - Check plugin manifest format
   - Verify OpenAPI spec is valid

### Debug Commands
```bash
# Check running services
ps aux | grep python

# Check port usage
lsof -i :5010

# Test individual services
curl http://127.0.0.1:5001/health
curl http://127.0.0.1:5002/health
curl http://127.0.0.1:5004/health
curl http://127.0.0.1:5005/health
```

## Security Considerations

- The current setup uses `auth.type: "none"` for simplicity
- For production, implement proper authentication
- Use HTTPS for all communications
- Validate and sanitize all inputs
- Implement rate limiting and monitoring

## Next Steps

1. **Production Deployment**
   - Deploy services to cloud infrastructure
   - Set up proper domain and SSL certificates
   - Configure production databases

2. **Enhanced Features**
   - Add authentication to the plugin
   - Implement real-time notifications
   - Add more sophisticated search and booking logic

3. **Monitoring & Logging**
   - Add comprehensive logging
   - Set up monitoring and alerting
   - Implement performance metrics

## Support

For issues or questions:
- Check the main project README
- Review service-specific documentation
- Contact: support@qt-ride.com 