from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: str
    type: str  # "income" or "expense"

@app.get("/expenses")
def get_all_expenses(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Expense)
    if category:
        query = query.filter(models.Expense.category == category)
    return query.all()

@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@app.post("/expenses", status_code=201)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    if expense.type not in ["income", "expense"]:
        raise HTTPException(status_code=400, detail="Type must be 'income' or 'expense'")
    new_expense = models.Expense(**expense.dict())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"message": f"Expense {expense_id} deleted successfully"}

@app.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    total_income = db.query(func.sum(models.Expense.amount)).filter(
        models.Expense.type == "income").scalar() or 0
    total_expense = db.query(func.sum(models.Expense.amount)).filter(
        models.Expense.type == "expense").scalar() or 0
    balance = total_income - total_expense

    category_breakdown = db.query(
        models.Expense.category,
        func.sum(models.Expense.amount)
    ).group_by(models.Expense.category).all()

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "category_breakdown": [
            {"category": c, "total": t} for c, t in category_breakdown
        ]
    }