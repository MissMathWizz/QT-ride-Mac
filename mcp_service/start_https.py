#!/usr/bin/env python3
"""
Start the MCP service on HTTPS port 443 for ChatGPT Custom GPT compatibility
"""

import uvicorn
import os
import sys

def start_https_service():
    """Start the service on HTTPS port 443"""
    
    # Check if SSL files exist
    cert_file = "localhost.crt"
    key_file = "localhost.key"
    
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print("❌ SSL certificate files not found!")
        print("Please run the SSL certificate creation first:")
        print("   openssl genrsa -out localhost.key 2048")
        print("   openssl req -new -x509 -key localhost.key -out localhost.crt -days 365 -subj '/CN=localhost'")
        return False
    
    # Check if running as root (required for port 443)
    if os.geteuid() != 0:
        print("⚠️  Port 443 requires root privileges!")
        print("Please run with sudo:")
        print(f"   sudo {sys.executable} {__file__}")
        return False
    
    print("🚀 Starting MCP service on HTTPS port 443...")
    print("   This will be accessible at: https://localhost")
    print("   Press Ctrl+C to stop")
    
    try:
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=443,
            ssl_keyfile=key_file,
            ssl_certfile=cert_file,
            log_level="info"
        )
    except PermissionError:
        print("❌ Permission denied. Make sure to run with sudo.")
        return False
    except Exception as e:
        print(f"❌ Error starting service: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_https_service() 