## Over view
- This is my graduation internship project, a backend application built with FastAPI that integrates Google's Gemini AI. The project was developed to explore backend development practices, RESTful API design, and AI/LLM integration using the Gemini API. 
- It focuses on building a scalable backend architecture while learning how modern AI services can be integrated into real-world applications.
## Key Features
- RESTful API built with FastAPI.
- JWT-based authentication and authorization.
- AI-powered text generation using Google Gemini.
- Database interaction using SQLAlchemy ORM.
- Request and response validation using Pydantic.
- Interactive API documentation with Swagger UI.
## Tech Stack
- Language:** Python
- Framework:** FastAPI, Uvicorn
- Database:** PostgreSQL
- ORM:** SQLAlchemy
- Authentication:** JWT (JSON Web Token)
- AI Integration:** Google Gemini API
## Project Structure
```text
fastapivsgemini
├── backend
│   ├── app
│   │   ├── core
│   │   ├── crud
│   │   ├── database
│   │   ├── models
│   │   ├── routers
│   │   ├── schemas
│   │   ├── dependencies.py
│   │   └── main.py
│   ├── chroma_db
│   ├── data
│   ├── .env
│   └── requirements.txt
├── frontend
│   └── app
│       ├── public
│       ├── src
│       │   ├── components
│       │   ├── pages
│       │   ├── api.js
│       │   ├── App.js
│       │   ├── index.css
│       │   └── index.js
│       ├── package-lock.json
│       └── package.json
├── .gitignore
└── README.md
```
## Installation

### 1. Clone the repository
```bash
git clone https://github.com/PhamManhLan/fastapi-gemini.git

cd fastapi-gemini
```
### 2. Create a virtual environment
```bash
cd backend

python -m venv .venv
```
Activate the virtual environment.
```bash
.venv\Scripts\activate
```
### 3. Install dependencies

```bash
pip install -r requirements.txt
```
## Environment Variables

Create a `.env` file inside the `backend` folder.

```env
GEMINI_API_KEY=
SECRET_KEY=

POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB=
```
## Running the Project

Start the backend server.

```bash
cd backend

uvicorn app.main:app --reload
```

The API will be available at

```
http://127.0.0.1:8000
```
Start the frontend.

```bash
cd frontend/app

npm install

npm start
```
## Project Goals

This project was developed during my graduation internship to:

- Learn backend development with FastAPI.
- Build secure RESTful APIs.
- Integrate Large Language Models (Google Gemini).
- Apply database design using PostgreSQL and SQLAlchemy.
- > **Note**
> This project was developed personally as part of my graduation internship. The goal was to learn backend programming, RESTful APIs, and artificial intelligence integration with Google Gemini.
