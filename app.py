from fastapi import FastAPI
from rules.rule_processor import process_emails, load_rules

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Email Rule Processor API"}

@app.get("/rules")
def get_rules():
    return load_rules()

@app.post("/process_emails")
def execute_email_processing():
    process_emails()
    return {"message": "Email processing triggered successfully."}
