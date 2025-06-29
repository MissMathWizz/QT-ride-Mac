[![Python CI](https://github.com/ramilevi1/QT-ride/actions/workflows/python-app.yml/badge.svg)](https://github.com/ramilevi1/QT-ride/actions/workflows/python-app.yml)

test 2
# QT-ride Mac Version (Testing)

A microservices-based ride-sharing application specifically adapted and tested for macOS. This version is currently under development and testing.

⚠️ **Note: This is a testing version, not ready for production use.**

## Services

- **Auth Service** (Port 5001): Handles user authentication
- **Search Service** (Port 5002): Manages ride searches
- **Offer Service** (Port 5004): Handles ride offers
- **User Profile Service**: Manages user profiles

## Important Setup Notes

⚠️ **Python Version Compatibility**: This project requires Python 3.11 for optimal compatibility with all dependencies. Python 3.13 is not currently supported due to package compatibility issues.

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/MissMathWizz/QT-ride-Mac.git
cd QT-ride-Mac
```

2. Ensure you have Python 3.11 installed:
```bash
python3.11 --version
```
If Python 3.11 is not installed, you can install it using Homebrew:
```bash
brew install python@3.11
```

3. Create and activate a virtual environment with Python 3.11:
```bash
python3.11 -m venv venv_py311
source venv_py311/bin/activate
```

4. Upgrade pip and install core dependencies:
```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

5. Install the spaCy English language model:
```bash
python -m spacy download en_core_web_sm
```

## Mac-Specific Setup
1. Clone the repository:
```bash
git clone https://github.com/MissMathWizz/QT-ride-Mac.git
cd QT-ride-Mac
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

The application consists of multiple microservices that need to run simultaneously. You'll need to open separate terminal windows/tabs for each service.

### Terminal 1: Authentication Service
```bash
cd QT-ride-Mac
cd auth_service
source ../venv/bin/activate
change line 12 in app.py " app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/auth_service.db' " to "app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/yw/QT-ride-Mac-test2/QT-ride-Mac/auth_service/instance/auth_service.db'"

python3 app.py
```
This service will run on http://127.0.0.1:5001

### Terminal 2: Search Service
```bash
cd QT-ride-Mac
cd search_service
source ../venv/bin/activate
python3 app.py
```
This service will run on http://127.0.0.1:5003

### Terminal 3: Offer Service
```bash
cd QT-ride-Mac
cd offer_service
source ../venv/bin/activate
python3 app.py
```

### Terminal 4: User Profile
```bash
cd QT-ride-Mac
cd user_profile
source ../venv/bin/activate
python3 app.py
```
This service will run on http://127.0.0.1:5004

### Terminal 5: Main Application
```bash
# Make sure you're in the project root directory
cd QT-ride-Mac
source venv/bin/activate
python3 app.py
```
The main application will run on http://127.0.0.1:5002

## API Endpoints

### Auth Service (localhost:5001)
- POST /signup - Create new user
- POST /signin - User login
- POST /signout - User logout

### Search Service (localhost:5002)
- GET /search - Search for rides

### Offer Service (localhost:5004)
- POST /offer - Create ride offer

## Requirements
- macOS
- Python 3.11+
- Flask
- SQLAlchemy
- PyJWT

## Testing Status
- ✅ Basic setup tested on macOS
- ✅ Authentication service functional
- ⚠️ Search service under testing
- ⚠️ Offer service under testing
- 🔄 Integration testing in progress

## Known Issues
- Some services may require additional configuration for macOS
- Database paths may need adjustment based on your macOS setup
- Virtual environment setup might vary based on your Python installation

Please report any issues or bugs you encounter while testing!

Carpooliong. features included:
1. sign up and log-in/log-out (authentication)
2. HTTPS support (currently with self sign certificate)
3. responsive front-end and backend
7. blog to share our progress and learnings
8. parsing blog for dynamic content and search functionality
9. newletter signin for anyone who wants to be notified of new posts
10. script to send weekly/monthly newsletter to registered users
11. unsubscrite functionality
12. contact us - Email sender (currently send to rami's personal email)


# Technology used : 
1. HTML 5
2. CSS 3
3. Javascript (vanilla)
4. Jquery
5. Bootstrap
6. MixItUp plugin
7. Flask - Python
8. Ajax for serving JS files
9. SQlite3
10. Playwright basic e2e tests
11. unit tests 

Next to do:
1. containerize (p1)
2. admin backoffice for managing users and blog posts (p2)
2. deploy to production using uWSGI ?! (p2)
3. github action setup for CI/CD (p0)
4. using web server NginX or Apache (p1)
5. SSL support (HTTP, HSTS) for security (p1)
6. RabbitMQ for serving email async and push notification later on live rides notification (p2)
7. MongoDB for serving images (p2)
8. sqlite3 database replication with the app and failover seperate service (p1)
9. create the offerRide and SearchRide as microservices (p0)


To start the web application:
python -m venv venv  OR 
python -m venv C:\xyz\venv\Scripts\python.exe
.\venv\Scripts\activate
$env:PATH = ".\venv\Scripts;" + $env:PATH 
flask db init     
flask db upgrade
flask db migrate
pip install Flask
set FLASK_APP=app.py flask run
pip install Flask-Mail
pip install Flask-SQLAlchemy      
pip install beautifulsoup4
pip install flask-migrate
pip install flask-login
pip install spacy
python -m spacy download en_core_web_sm
pip install WTForms
pip install Flask-WTF

# install selfsign certificate:
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=127.0.0.1'
# remove passcode: 
openssl rsa -in key.pem -out key_decrypted.pem        

$env:PATH = ".\venv\Scripts;" + $env:PATH   
export PYTHONPATH=/path/to/parent_directory:$PYTHONPATH
>> python scripts/parse_blogs.py
python -m venv C:\xyz\venv\Scripts\python.exe
.\venv\Scripts\activate   
python .\app.py -debug 
flask run
 
 
Architecture:
N-tier microservices arcitecture 
                        --------
                        |Client |
                        --------
                            |
                            |
                            |  
------------------------    -------------------    -------------------
|authentication service|    |offerRide service|   |searchRide service|
------------------------    -------------------   --------------------
            |                        |                    |
            |                        |                    |
      ------------            --------------         ----------
      |   DB     |            |     DB     |         |    DB   |
      ------------            -------------          ----------

# QT-ride-Mac

A ride-sharing application built with Flask microservices architecture.

## Prerequisites

- Python 3.11 (recommended, tested version)
- macOS (tested on macOS 24.5.0)
- Terminal access



### Known Installation Issues

1. If you encounter issues with spaCy or its dependencies:
   - Make sure you're using Python 3.11
   - The requirements.txt includes numpy==1.24.3 which is specifically chosen for compatibility
   - If you still have issues, try installing the core dependencies first:
     ```bash
     pip install -r requirements_core.txt
     ```

2. For M1/M2 Mac users:
   - The project has been tested and configured for Apple Silicon
   - All binary dependencies are compatible with arm64 architecture

