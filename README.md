# Calculate-Mutual-Fund-Profit
FastAPI Mutual Fund Profit Calculator: Calculates investment profit using scheme code, purchase &amp; redemption dates, and initial amount. Integrates external API, adjusts dates for available data. Object-oriented, modular design.
Mutual Fund Profit Calculator using Python and FastAPI
This repository contains a simple yet powerful Mutual Fund Profit Calculator built with Python and FastAPI. It's designed for beginners looking to understand API integration, data retrieval, and basic web development concepts.

Importing Necessary Modules
The code starts by importing required modules. These are external libraries that contain pre-written code to perform specific tasks.

requests: Helps in making HTTP requests to external APIs.
datetime and timedelta from datetime: Aid in handling dates and time calculations.
FastAPI: This is the main library that helps in building APIs quickly with Python.
HTTPException: An exception class from FastAPI used to handle HTTP errors.
Query and Optional: Classes from FastAPI for handling query parameters in API endpoints.
uvicorn: A library used to run the FastAPI application.
Defining Functions
get_nav Function:

Fetches the Net Asset Value (NAV) of a mutual fund for a specific date and scheme code from an external API (https://api.mfapi.in/).
Parses the response from the API and returns the NAV as a float (a numeric type with decimal points) if available.
calculate_profit Function:

Calculates the profit for a mutual fund investment based on given parameters: scheme code, start date, end date, and initial investment amount.
Finds the nearest available start and end dates for which NAV data is available within the specified date range.
Calculates the number of units allotted and the net profit based on NAV data.
FastAPI Integration
@app.get("/profit") Decorator:

Defines an endpoint /profit that handles GET requests.
Accepts query parameters (scheme_code, start_date, end_date, capital) to calculate the net profit of a mutual fund investment.
Calls the calculate_profit function with the provided parameters and returns the result.
calculate_profit_route Function:

A handler function for the /profit endpoint.
Invokes the calculate_profit function to calculate the profit based on the query parameters provided.
If the result is a string (indicating an error), it raises an HTTPException with a 404 status code.
Returns the calculated net profit as a JSON response.
Running the Application
The if __name__ == "__main__": block ensures that the FastAPI application runs when the script is executed directly.

It uses uvicorn.run to start the FastAPI application, specifying the host (127.0.0.1), port (5000), enabling auto-reload (reload=True), and setting the number of workers to handle requests (workers=3).
This code demonstrates how to create a simple API using FastAPI, fetch data from an external source, perform calculations, and expose an endpoint for users to calculate the profit of a mutual fund investment.
