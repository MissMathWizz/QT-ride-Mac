from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from typing import Dict, Optional

app = FastAPI(title="QT-Ride MCP Wrapper", description="API Gateway for QT-Ride microservices.")

# Add CORS middleware for ChatGPT Custom GPT access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com", "https://chatgpt.com", "*"],  # Allow ChatGPT domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVICES = {
    "auth_service": "http://127.0.0.1:5001",
    "search_service": "http://127.0.0.1:5003",
    "offer_service": "http://127.0.0.1:5004",
    "user_profile": "http://127.0.0.1:5005"  # Adjust if needed
}

client = httpx.AsyncClient()

# Simple session store for demo (in production, use Redis or database)
user_sessions: Dict[str, Dict] = {}

def get_user_from_request(request: Request) -> Optional[Dict]:
    """Extract user info from request. In a real app, this would check headers/cookies."""
    # For demo, we'll use the first logged-in user
    # In production, you'd check Authorization header or session cookies
    if user_sessions:
        return list(user_sessions.values())[0]
    return None

@app.get("/")
async def root():
    return {"message": "QT-Ride MCP Wrapper is running", "endpoints": ["/signup", "/login", "/search", "/book", "/profile/{user_id}"], "flow": "1. Sign up → 2. Log in → 3. Use other features"}

@app.get("/health")
async def health():
    return {"status": "healthy", "services": SERVICES}

@app.get("/session")
async def get_session(request: Request):
    """Get current session status"""
    user = get_user_from_request(request)
    if user:
        return {
            "logged_in": True,
            "email": user['email'],
            "message": f"You are logged in as {user['email']}"
        }
    else:
        return {
            "logged_in": False,
            "message": "No active session. Please log in first."
        }

@app.post("/signup")
async def signup(request: Request):
    """Create a new user account"""
    data = await request.json()
    try:
        resp = await client.post(f"{SERVICES['auth_service']}/signup", json=data)
        if resp.status_code == 201:
            response_data = resp.json()
            email = data.get('email')
            response_data['message'] = f"Account created successfully for {email}! You can now log in with your credentials."
            response_data['next_step'] = "Please use the login function to sign in."
            return JSONResponse(status_code=201, content=response_data)
        return JSONResponse(status_code=resp.status_code, content=resp.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    try:
        resp = await client.post(f"{SERVICES['auth_service']}/signin", json=data)
        if resp.status_code == 200:
            response_data = resp.json()
            # Store user session with token
            email = data.get('email')
            if email and 'access_token' in response_data:
                user_sessions[email] = {
                    'access_token': response_data['access_token'],
                    'email': email
                }
                # Add session info to response
                response_data['session_created'] = True
                response_data['message'] = f"Welcome! You are now logged in as {email}. You can now search for rides, book rides, and view your profile."
            return JSONResponse(status_code=resp.status_code, content=response_data)
        return JSONResponse(status_code=resp.status_code, content=resp.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search")
async def search(request: Request):
    try:
        resp = await client.get(f"{SERVICES['search_service']}/search_rides", params=dict(request.query_params))
        return JSONResponse(status_code=resp.status_code, content=resp.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/book")
async def book(request: Request):
    data = await request.json()
    try:
        user = get_user_from_request(request)
        if not user:
            raise HTTPException(status_code=401, detail="Please log in first to book a ride")
        
        # For demo purposes, we'll create a ride offer instead of booking
        # In a real system, you'd have separate booking and offering endpoints
        offer_data = {
            "origin": data.get("origin", "Unknown"),
            "destination": data.get("destination", "Unknown"), 
            "date": data.get("date", "2025-07-01"),
            "time": data.get("time", "12:00"),
            "seats_available": data.get("seats_available", 1),
            "price": data.get("price", 0),
            "driver_name": user.get('email', 'Driver'),
            "driver_phone": data.get("driver_phone", "000-000-0000"),
            "car_model": data.get("car_model", "Unknown"),
            "car_color": data.get("car_color", "Unknown"),
            "car_plate_number": data.get("car_plate_number", "UNKNOWN")
        }
        resp = await client.post(f"{SERVICES['offer_service']}/offer_rides", data=offer_data)
        if resp.status_code == 201:
            return JSONResponse(status_code=200, content={
                "message": "Ride offer created successfully! Other users can now book your ride.",
                "booking_id": "DEMO-" + str(hash(user['email']))[:8],
                "status": "confirmed"
            })
        return JSONResponse(status_code=resp.status_code, content=resp.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profile/{user_id}")
async def get_profile(user_id: str, request: Request):
    try:
        user = get_user_from_request(request)
        if not user:
            raise HTTPException(status_code=401, detail="Please log in first to view your profile")
        
        # Try to get profile from user profile service with JWT
        headers = {"Authorization": f"Bearer {user['access_token']}"}
        try:
            resp = await client.get(f"{SERVICES['user_profile']}/get_profile", headers=headers)
            if resp.status_code == 200:
                profile_data = resp.json()
                # Add user info from auth service
                profile_data.update({
                    "id": user_id,
                    "email": user['email'],
                    "rides_taken": 5  # Mock data
                })
                return JSONResponse(status_code=200, content=profile_data)
        except:
            pass
            
        # Fallback to mock profile with logged-in user info
        mock_profile = {
            "id": user_id,
            "name": user.get('email', f"User {user_id}"),
            "email": user['email'],
            "rides_taken": 5,
            "driver_name": "Not set",
            "driver_phone": "Not set",
            "car_model": "Not set",
            "car_color": "Not set",
            "car_plate_number": "Not set"
        }
        return JSONResponse(status_code=200, content=mock_profile)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Custom GPT Actions schema
@app.get("/custom_gpt_schema.json")
async def custom_gpt_schema():
    return FileResponse("custom_gpt_schema.json")

# Legacy OpenAI Plugin routes (for compatibility)
@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    return FileResponse(".well-known/ai-plugin.json")

@app.get("/openapi.yaml")
async def openapi_spec():
    return FileResponse("openapi.yaml")

@app.get("/privacy-policy")
async def privacy_policy():
    return FileResponse("privacy-policy.html", media_type="text/html")

@app.get("/legal")
async def legal_info():
    return FileResponse("legal")

@app.get("/logo.png")
async def logo():
    return FileResponse("logo.png")

@app.on_event("shutdown")
async def shutdown_event():
    await client.aclose()

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting QT-Ride MCP Wrapper...")
    uvicorn.run(app, host="127.0.0.1", port=5010, log_level="info")