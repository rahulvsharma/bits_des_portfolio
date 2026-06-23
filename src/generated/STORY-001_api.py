# Portfolio Service Backend
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging

app = FastAPI(title="Portfolio Service")
logger = logging.getLogger(__name__)

class PortfolioItem(BaseModel):
    symbol: str
    quantity: float
    purchase_price: float
    current_price: float

class Portfolio(BaseModel):
    user_id: str
    items: List[PortfolioItem]
    created_at: datetime

# In-memory storage
portfolios = {}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "portfolio"}

@app.post("/portfolio/create")
def create_portfolio(user_id: str, portfolio: Portfolio):
    try:
        if user_id in portfolios:
            raise HTTPException(status_code=400, detail="Portfolio already exists")
        
        portfolios[user_id] = portfolio
        logger.info(f"Portfolio created for user {user_id}")
        return {"status": "success", "user_id": user_id}
    except Exception as e:
        logger.error(f"Error creating portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/portfolio/{user_id}")
def get_portfolio(user_id: str):
    try:
        if user_id not in portfolios:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolio = portfolios[user_id]
        total_value = sum(item.quantity * item.current_price for item in portfolio.items)
        
        return {
            "portfolio": portfolio,
            "total_value": total_value,
            "item_count": len(portfolio.items)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/portfolio/{user_id}/update")
def update_portfolio(user_id: str, portfolio: Portfolio):
    try:
        if user_id not in portfolios:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        portfolios[user_id] = portfolio
        logger.info(f"Portfolio updated for user {user_id}")
        return {"status": "success", "updated": True}
    except Exception as e:
        logger.error(f"Error updating portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/portfolio/{user_id}")
def delete_portfolio(user_id: str):
    try:
        if user_id not in portfolios:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        del portfolios[user_id]
        logger.info(f"Portfolio deleted for user {user_id}")
        return {"status": "success", "deleted": True}
    except Exception as e:
        logger.error(f"Error deleting portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))
