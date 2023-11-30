import requests
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Query
from typing import Optional
import uvicorn

app = FastAPI()


def get_nav(scheme_code, date):
    url = f"https://api.mfapi.in/mf/{scheme_code}?date={date}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return float(data['data']['nav'])
    return None


def calculate_profit(scheme_code, start_date, end_date, capital=1000000.0):
    start = datetime.strptime(start_date, '%d-%m-%Y')
    end = datetime.strptime(end_date, '%d-%m-%Y')

    # Loop to find the nearest available start date
    current_start = start
    while True:
        nav = get_nav(scheme_code, current_start.strftime('%d-%m-%Y'))
        if nav:
            break
        current_start += timedelta(days=1)

    # Loop to find the nearest available end date
    current_end = end
    while True:
        nav = get_nav(scheme_code, current_end.strftime('%d-%m-%Y'))
        if nav:
            break
        current_end -= timedelta(days=1)

    if current_start > current_end:
        return "NAV data not available for the given date range."

    units_allotted = capital / get_nav(scheme_code, current_start.strftime('%d-%m-%Y'))
    value_on_redemption = units_allotted * get_nav(scheme_code, current_end.strftime('%d-%m-%Y'))
    net_profit = value_on_redemption - capital

    return net_profit



@app.get("/profit")
async def calculate_profit_route(
        scheme_code: str = Query(..., description="The unique scheme code of the mutual fund."),
        start_date: str = Query(..., description="The purchase date of the mutual fund."),
        end_date: str = Query(..., description="The redemption date of the mutual fund."),
        capital: float = Query(1000000.0, description="The initial investment amount."),
):
    profit = calculate_profit(scheme_code, start_date, end_date, capital)
    if isinstance(profit, str):
        raise HTTPException(status_code=404, detail=profit)
    return {"net_profit": profit}


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=5000, reload=True, workers=3)
