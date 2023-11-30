import requests
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Query
from typing import Optional
import uvicorn


class MutualFundAPI:
    def __init__(self):
        self.base_url = "https://api.mfapi.in/mf/"

    def get_nav(self, scheme_code, date):
        url = f"{self.base_url}{scheme_code}?date={date}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return float(data['data'][0]['nav'])
        return None


class ProfitCalculator(MutualFundAPI):
    def calculate_profit(self, scheme_code, start_date, end_date, capital=1000000.0):
        start = datetime.strptime(start_date, '%d-%m-%Y')
        end = datetime.strptime(end_date, '%d-%m-%Y')
        current_start = start
        current_end = end

        while current_start <= end:
            nav_start = self.get_nav(scheme_code, current_start.strftime('%d-%m-%Y'))
            if nav_start:
                break
            current_start += timedelta(days=1)

        while current_end >= start:
            nav_end = self.get_nav(scheme_code, current_end.strftime('%d-%m-%Y'))
            if nav_end:
                break
            current_end -= timedelta(days=1)

        if not nav_start or not nav_end:
            return "NAV data not available for the given date range."

        nav_start = float(nav_start)
        nav_end = float(nav_end)

        units_allotted = capital / nav_start
        value_on_redemption = units_allotted * nav_end
        net_profit = value_on_redemption - capital

        return net_profit


app = FastAPI()
profit_calculator = ProfitCalculator()


@app.get("/profit")
async def calculate_profit_route(
        scheme_code: str = Query(...),
        start_date: str = Query(...),
        end_date: str = Query(...),
        capital: float = Query(1000000.0),
):
    profit = profit_calculator.calculate_profit(scheme_code, start_date, end_date, capital)
    if isinstance(profit, str):
        raise HTTPException(status_code=404, detail=profit)
    return {"net_profit": profit}


if __name__ == "__main__":
    uvicorn.run("test:app", host='127.0.0.1', port=5000, reload=True, workers=1)
