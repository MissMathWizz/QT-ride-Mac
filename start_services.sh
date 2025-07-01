#!/bin/bash

# Start all QT-Ride microservices
echo "Starting QT-Ride microservices..."

# Activate virtual environment
source venv/bin/activate

# Start auth service
echo "Starting auth service on port 5001..."
cd auth_service
python app.py &
AUTH_PID=$!
cd ..

# Start search service  
echo "Starting search service on port 5002..."
cd search_service
python app.py &
SEARCH_PID=$!
cd ..

# Start offer service
echo "Starting offer service on port 5004..."
cd offer_service
python app.py &
OFFER_PID=$!
cd ..

# Start user profile service
echo "Starting user profile service on port 5005..."
cd user_profile
python app.py &
PROFILE_PID=$!
cd ..

# Start MCP wrapper
echo "Starting MCP wrapper on port 5010..."
cd mcp_service
uvicorn main:app --reload --port 5010 &
MCP_PID=$!
cd ..

echo "All services started!"
echo "Auth Service PID: $AUTH_PID"
echo "Search Service PID: $SEARCH_PID"
echo "Offer Service PID: $OFFER_PID"
echo "Profile Service PID: $PROFILE_PID"
echo "MCP Wrapper PID: $MCP_PID"

echo "To stop all services, run: kill $AUTH_PID $SEARCH_PID $OFFER_PID $PROFILE_PID $MCP_PID" 