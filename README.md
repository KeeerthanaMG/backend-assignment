📧 Email Processor Backend
🚀 Automated email processing system using FastAPI, PostgreSQL, and Docker.

This project fetches emails from Gmail, stores them in PostgreSQL, and processes them based on custom rules.
It provides a REST API to manage rules and is Docker-ready for easy deployment.

📌 Features
✔ Fetches emails from Gmail API
✔ Stores emails in PostgreSQL
✔ Rule-based email processing (mark as read, move, delete, etc.)
✔ REST API to fetch and execute rules
✔ Uses FastAPI for API
✔ Logging & Error Handling for maintainability
✔ Docker support for easy deployment

📌 Installation & Setup
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/YOUR_USERNAME/email-processor.git
cd email-processor
2️⃣ Create & Activate Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\Activate     # For Windows
3️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Set Up Environment Variables
Create a .env file in the root directory and add:

ini
Copy
Edit
DATABASE_URL=postgresql://email_user:securepassword@localhost/email_db
GMAIL_CREDENTIALS_PATH=config/credentials.json
TOKEN_PATH=config/token.json
📌 Running the Project Locally
1️⃣ Start PostgreSQL Database
Ensure PostgreSQL is running, then create the database manually:

sql
Copy
Edit
CREATE DATABASE email_db;
2️⃣ Run the FastAPI Server
bash
Copy
Edit
uvicorn app:app --reload
The API will be available at:

cpp
Copy
Edit
http://127.0.0.1:8000
3️⃣ Fetch Emails from Gmail
bash
Copy
Edit
python -m gmail.fetch_emails
4️⃣ Process Emails Using Rules
bash
Copy
Edit
python -m rules.rule_processor
📌 API Documentation
After running uvicorn, open:

arduino
Copy
Edit
http://127.0.0.1:8000/docs
This Swagger UI will let you test endpoints interactively.

Method	Endpoint	Description
GET	/rules	Fetch all email processing rules
POST	/process_emails	Execute rule-based email processing
📌 Running the Project with Docker
1️⃣ Build and Start the Containers
bash
Copy
Edit
docker-compose up --build
This will:

Start a PostgreSQL database container
Start a FastAPI app container
2️⃣ Verify Running Containers
bash
Copy
Edit
docker ps
API should be available at:

cpp
Copy
Edit
http://127.0.0.1:8000
3️⃣ Stop the Containers
bash
Copy
Edit
docker-compose down
📌 Running Tests
This project includes unit tests to ensure everything works correctly.

1️⃣ Run All Tests
bash
Copy
Edit
pytest tests/
✅ Test Coverage Includes:

Database connection (test_db.py)
Email fetching (test_fetch_emails.py)
Rule processing (test_rules.py)
📌 Folder Structure
bash
Copy
Edit
backend-assignment/
│── config/                 # Configuration files
│── database/               # Database connection & models
│── gmail/                  # Gmail API-related modules
│── rules/                  # Rule processing logic
│── tests/                  # Unit tests
│── data/                   # JSON rules & static data
│── logs/                   # Log files
│── utils/                  # Error handling & logging
│── Dockerfile              # Docker build file
│── docker-compose.yml      # Docker Compose setup
│── README.md               # Project documentation
│── setup.py                # (Optional) Packaging script
│── app.py                  # FastAPI entry point
📌 FAQ (Troubleshooting)
1️⃣ Gmail Authentication Fails
Try deleting config/token.json and re-run:

bash
Copy
Edit
python -m gmail.auth
2️⃣ Database Not Connecting
Check if PostgreSQL is running and .env contains the correct database URL.

3️⃣ Docker Not Working
Ensure Docker is installed and running:

bash
Copy
Edit
docker --version
📌 License
This project is open-source and available under the MIT License.

