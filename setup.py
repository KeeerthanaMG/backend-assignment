from setuptools import setup, find_packages

setup(
    name="email_processor",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "psycopg2",
        "google-auth-oauthlib",
        "google-auth",
        "google-auth-httplib2",
        "google-auth-api-client",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "run-email-processor=app:main",
        ],
    },
)
