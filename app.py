
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Load dataset
try:
    df = pd.read_csv("clean_stocks.csv")
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print("Error: clean_stocks.csv not found!")
    df = pd.DataFrame()

# Ensure Date column is datetime type
if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Valid companies
VALID_COMPANIES = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]

@app.route('/', methods=['GET'])
def home():
    """API documentation endpoint"""
    return jsonify({
        "message": "Stock Price API",
        "endpoints": {
            "/get_stock": "GET - Retrieve stock data for a specific company and date",
            "/companies": "GET - List all available companies",
            "/date_range": "GET - Get available date range for data"
        },
        "example": "/get_stock?company=AAPL&date=2023-07-10"
    })

@app.route('/companies', methods=['GET'])
def get_companies():
    """Get list of available companies"""
    return jsonify({
        "companies": VALID_COMPANIES,
        "total": len(VALID_COMPANIES)
    })

@app.route('/date_range', methods=['GET'])
def get_date_range():
    """Get available date range"""
    if df.empty:
        return jsonify({"error": "No data available"}), 500
    
    min_date = df["Date"].min().strftime("%Y-%m-%d")
    max_date = df["Date"].max().strftime("%Y-%m-%d")
    
    return jsonify({
        "min_date": min_date,
        "max_date": max_date,
        "total_days": len(df)
    })

@app.route('/get_stock', methods=['GET'])
def get_stock():
    """Get stock data for a specific company and date"""
    company = request.args.get("company", "").upper()
    date = request.args.get("date", "")

    # Validation
    if not company or not date:
        return jsonify({
            "error": "Please provide both company and date",
            "example": "/get_stock?company=AAPL&date=2023-07-10"
        }), 400

    # Validate company
    if company not in VALID_COMPANIES:
        return jsonify({
            "error": f"Invalid company. Choose from: {', '.join(VALID_COMPANIES)}",
            "valid_companies": VALID_COMPANIES
        }), 400

    # Validate date format
    try:
        query_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({
            "error": "Invalid date format. Use YYYY-MM-DD",
            "example": "2023-07-10"
        }), 400

    # Check if dataset is loaded
    if df.empty:
        return jsonify({"error": "Dataset not available"}), 500

    # Filter dataset
    row = df[df["Date"].dt.date == query_date]

    if row.empty:
        return jsonify({
            "error": f"No data found for {date}",
            "suggestion": "Check /date_range for available dates"
        }), 404

    try:
        # Extract company-specific stock data
        result = {
            "success": True,
            "data": {
                "Date": date,
                "Company": company,
                "Open": float(row[f"{company}_Open"].values[0]),
                "High": float(row[f"{company}_High"].values[0]),
                "Low": float(row[f"{company}_Low"].values[0]),
                "Close": float(row[f"{company}_Close"].values[0]),
                "Volume": int(row[f"{company}_Volume"].values[0])
            }
        }
        
        
        try:
            open_price = result["data"]["Open"]
            close_price = result["data"]["Close"]
            change_percent = ((close_price - open_price) / open_price) * 100
            result["data"]["Change_Percent"] = round(change_percent, 2)
        except:
            pass
            
    except KeyError as e:
        return jsonify({
            "error": f"Data columns not available for company {company}",
            "missing_column": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

    return jsonify(result)

@app.route('/get_stock_range', methods=['GET'])
def get_stock_range():
    """Get stock data for a company within a date range"""
    company = request.args.get("company", "").upper()
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")
    
    if not all([company, start_date, end_date]):
        return jsonify({
            "error": "Please provide company, start_date, and end_date",
            "example": "/get_stock_range?company=AAPL&start_date=2023-07-01&end_date=2023-07-10"
        }), 400
    
    if company not in VALID_COMPANIES:
        return jsonify({
            "error": f"Invalid company. Choose from: {', '.join(VALID_COMPANIES)}"
        }), 400
    
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    if df.empty:
        return jsonify({"error": "Dataset not available"}), 500
    
    # Filter by date range
    mask = (df["Date"].dt.date >= start_dt) & (df["Date"].dt.date <= end_dt)
    filtered_df = df[mask]
    
    if filtered_df.empty:
        return jsonify({"error": "No data found for the specified date range"}), 404
    
    try:
        results = []
        for _, row in filtered_df.iterrows():
            data = {
                "Date": row["Date"].strftime("%Y-%m-%d"),
                "Company": company,
                "Open": float(row[f"{company}_Open"]),
                "High": float(row[f"{company}_High"]),
                "Low": float(row[f"{company}_Low"]),
                "Close": float(row[f"{company}_Close"]),
                "Volume": int(row[f"{company}_Volume"])
            }
            results.append(data)
        
        return jsonify({
            "success": True,
            "count": len(results),
            "data": results
        })
        
    except KeyError as e:
        return jsonify({
            "error": f"Data not available for company {company}",
            "missing_column": str(e)
        }), 400

if __name__ == '__main__':
    print("Starting Stock Price API...")
    print(f"Available companies: {', '.join(VALID_COMPANIES)}")
    app.run(debug=True, host='0.0.0.0', port=5000)