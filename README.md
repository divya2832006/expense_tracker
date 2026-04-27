# Expense Tracker API

A REST API built with FastAPI and SQLite to track income
and expenses with category-wise summary.

## Tech Stack

- Python 3.x
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

## Features

- Add income and expense transactions
- Filter transactions by category
- Get total income, expense and balance summary
- Category-wise breakdown of spending
- Auto-generated Swagger UI documentation

## Project Structure

expense_tracker/
├── main.py         # API routes and logic
├── database.py     # Database connection setup
├── models.py       # Database models
└── requirements.txt

## Installation & Setup

1. Clone the repository
   git clone https://github.com/yourusername/expense-tracker-api.git
   cd expense-tracker-api

2. Install dependencies
   pip install -r requirements.txt

3. Run the server
   uvicorn main:app --reload

4. Open Swagger UI
   http://localhost:8000/docs

## API Endpoints

| Method | Endpoint            | Description                        |
|--------|---------------------|------------------------------------|
| GET    | /expenses           | Get all expenses (filter by category) |
| GET    | /expenses/{id}      | Get a single expense               |
| POST   | /expenses           | Add a new income or expense        |
| DELETE | /expenses/{id}      | Delete an expense                  |
| GET    | /summary            | Get total income, expense, balance |

## Sample Request

POST /expenses
{
  "title": "Salary",
  "amount": 50000,
  "category": "Job",
  "type": "income"
}

## Sample Response from /summary

{
  "total_income": 50000,
  "total_expense": 12000,
  "balance": 38000,
  "category_breakdown": [
    { "category": "Food", "total": 5000 },
    { "category": "Transport", "total": 7000 }
  ]
}

## Author

Divyadharshini P
GitHub: https://github.com/divya2832006
