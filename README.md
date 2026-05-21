# Compliance Photo Gallery

A FastAPI application for managing a compliance photo gallery.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/nikim0927/compliance-photo-gallery
   cd compliance-photo-gallery
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to run the application

Run the application locally using Uvicorn:
```bash
uvicorn main:app --reload
```

Then visit the API documentation at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
