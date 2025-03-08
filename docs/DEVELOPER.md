# 🛠 Developer Guide for Email Processor Backend

## 📌 Project Overview
This project fetches emails from Gmail, stores them in PostgreSQL, and processes them based on rules. It is built using FastAPI, PostgreSQL, SQLAlchemy, and Docker for easy deployment.

## 📌 Technologies Used
- **Python 3.10**
- **FastAPI** (Backend API)
- **PostgreSQL** (Database)
- **SQLAlchemy** (ORM)
- **Uvicorn** (ASGI Server)
- **Docker & Docker Compose** (Containerization)
- **pytest** (Testing)

## 📌 Folder Structure
```
backend-assignment/
│── config/          # Configuration files
│── database/        # Database connection & models
│── gmail/           # Gmail API-related modules
│── rules/           # Rule processing logic
│── tests/           # Unit tests
│── data/            # JSON rules & static data
│── logs/            # Log files
│── utils/           # Error handling & logging
│── Dockerfile       # Docker build file
│── docker-compose.yml # Docker Compose setup
│── README.md        # Project documentation
│── docs/            # Additional documentation
│   ├── DEVELOPER.md # Developer guide
│── setup.py         # (Optional) Packaging script
│── app.py           # FastAPI entry point
```

## 📌 Setting Up the Development Environment

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/email-processor.git
cd email-processor
```

### 2️⃣ Set Up the Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\Activate     # For Windows
3️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
📌 Running the Project in Development Mode
bash
Copy
Edit
uvicorn app:app --reload
✅ This enables hot-reloading for development.

📌 Running Tests
This project includes unit tests to ensure stability.

bash
Copy
Edit
pytest tests/
✅ Test Coverage Includes:
✔ Database connection (test_db.py)
✔ Email fetching (test_fetch_emails.py)
✔ Rule processing (test_rules.py)

📌 Debugging & Logs
All logs are stored in:

bash
Copy
Edit
logs/app.log
To monitor logs in real-time:

bash
Copy
Edit
tail -f logs/app.log
✅ Make sure logs are properly written when testing rule processing.

📌 Docker Setup (For Development & Deployment)
1️⃣ Build and Start Containers
bash
Copy
Edit
docker-compose up --build
```
This will:

Start a PostgreSQL database container
Start a FastAPI app container
2️⃣ Access PostgreSQL Inside Docker
bash
Copy
Edit
docker exec -it postgres_db psql -U email_user -d email_db
3️⃣ Stop Containers
bash
Copy
Edit
docker-compose down
📌 Best Practices
✔ Follow PEP8 coding standards
✔ Use docstrings for all functions
✔ Keep modular & reusable code
✔ Ensure tests pass before pushing code

✅ Run pytest before pushing any new code!

📌 Handling Environment Variables
Instead of hardcoding credentials, always use environment variables.

Example .env File
ini
Copy
Edit
DATABASE_URL=postgresql://email_user:securepassword@localhost/email_db
GMAIL_CREDENTIALS_PATH=config/credentials.json
TOKEN_PATH=config/token.json
📌 API Documentation
Once the server is running, test API endpoints using Swagger UI.

Open:

arduino
Copy
Edit
http://127.0.0.1:8000/docs
📌 How to Add New Rules
1️⃣ Open data/rules.json
2️⃣ Add a new rule:

json
Copy
Edit
{
  "rule_name": "Move CEO Emails",
  "predicate": "ANY",
  "conditions": [
    { "field": "from", "predicate": "contains", "value": "ceo@" },
    { "field": "subject", "predicate": "contains", "value": "urgent" }
  ],
  "actions": ["move_message"],
  "folder": "Work"
}
3️⃣ Run the rule processor:

bash
Copy
Edit
python -m rules.rule_processor
```
✅ Make sure the rule is applied correctly!

📌 Final Checklist Before Deployment
✔ Run all tests (pytest tests/)
✔ Ensure FastAPI is working (uvicorn app:app --reload)
✔ Ensure Docker runs properly (docker-compose up --build)
✔ Check logs for errors (tail -f logs/app.log)

