# Competitor Analyzer Project

This project is a web-based application built to compare websites and generate SEO recommendations using AI. It consists of a **Next.js Frontend** and a **FastAPI Backend**.

## Tech Stack
*   **Frontend**: Next.js (App Router), React 19, TypeScript, TailwindCSS v4.
*   **Backend**: Python, FastAPI, Uvicorn, SlowAPI (Rate Limiting).
*   **AI Integration**: Google GenAI API (Gemini) for analyzing websites and generating recommendations.

---

## Folder Structure
*   `/frontend` - Contains all the UI and Next.js React code.
*   `/backend` - Contains the FastAPI Python application, services, and routing.

---

## Required Environment Variables (.env)

You need to create a `.env` file in the root directory (or use the one provided in `.env.example`).

Here are the required keys:

```env
# Your Gemini API key for AI-based analysis
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_PROJECT_NAME=projects/your_project_number
GEMINI_PROJECT_NUMBER=your_project_number

# Used for Google reCAPTCHA verification to prevent bot spam
RECAPTCHA_SECRET_KEY=your_recaptcha_secret_here

# Frontend URL to configure CORS in the FastAPI backend
# Note: Since frontend runs on port 3001 by default, this should ideally be http://localhost:3001
FRONTEND_URL=http://localhost:3000

# Project environment (development / production)
ENVIRONMENT=development
```

---

## How to Run the Project Locally

### 1. Backend Setup (FastAPI)
Open a terminal in the `/backend` directory:
1.  **Create a Virtual Environment** (optional but recommended):
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Start the Backend Server**:
    ```bash
    uvicorn main:app --reload
    ```
    *The API will be available at `http://127.0.0.1:8000` and Swagger docs at `http://127.0.0.1:8000/docs`.*

### 2. Frontend Setup (Next.js)
Open a terminal in the `/frontend` directory:
1.  **Install Dependencies**:
    ```bash
    npm install
    ```
2.  **Start the Frontend Development Server**:
    ```bash
    npm run dev
    ```
    *The frontend will be available at `http://localhost:3001`.*

---

## Notes for Senior / Reviewer
*   **AI Generated Code**: This setup and structure was generated with AI assistance. 
*   **Ports**: The backend runs on standard port `8000`. The frontend is configured in `package.json` to start on port `3001`.
*   **Services**: Core logic resides in `/backend/services/ai_analyzer.py` and `/backend/api/analyze.py`.
