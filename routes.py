from flask import request,jsonify
import requests
from run import app,db

from models import UserCredentials
from models import UserProfile
from models import UserTrade
from models import Stocks
import datetime
from dateutil import parser


@app.route("/")
def helloworld():
    return "Hello World!"

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data['username']
    password_hash = data['password_hash']
    new_user = UserCredentials(username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/users/<int:username>', methods=['GET'])
def get_user(username):
    user = UserCredentials.query.get(username)
    return jsonify({'username': user.username, 'password_hash': user.password_hash})

@app.route('/api/allusers', methods=['GET'])
def get_all_users():
    users = UserCredentials.query.all()
    all_users = [{'username': user.username, 'password_hash': user.password_hash} for user in users]
    print(all_users)
    return jsonify(all_users)

@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = UserCredentials.query.get_or_404(id)
    data = request.get_json()
    user.username = data['username']
    user.password_hash = data['password_hash']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = UserCredentials.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})


ALPACA_API_KEY = 'PK4ZWZ0OK1URS2BSC6AW'
ALPACA_SECRET_KEY = 'N15y9j4ZyUcN3KtMfrz008p0Kvc8I1hwXLpisRoV'
BASE_URL = 'https://paper-api.alpaca.markets'

def submit_order(symbol, qty, side, type, time_in_force):
    url = f"{BASE_URL}/v2/orders"
    headers = {
        'APCA-API-KEY-ID': ALPACA_API_KEY,
        'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
    }
    data = {
        'symbol': symbol,
        'qty': qty,
        'side': side,
        'type': type,
        'time_in_force': time_in_force
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

@app.route('/api/trade', methods=['POST'])
def place_trade():
    data = request.get_json()
    response = submit_order(
        symbol=data['symbol'],
        qty=data['qty'],
        side='buy',
        type='market',
        time_in_force='gtc'
    )
    return jsonify(response)

@app.route('/api/alpaca_positions', methods=['GET'])
def get_positions():
    url = f"{BASE_URL}/v2/positions"
    headers = {
        'APCA-API-KEY-ID': ALPACA_API_KEY,
        'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
    }
    response = requests.get(url, headers=headers)
    return jsonify(response.json())

@app.route('/api/refresh_trades', methods=['GET'])
def refresh_trades():

    alpaca_endpoint = f"{BASE_URL}/v2/account/activities"
    headers = {
        'APCA-API-KEY-ID': ALPACA_API_KEY,
        'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
    }

    # Truncate the existing UserTrade table
    try:
        num_rows_deleted = db.session.query(UserTrade).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to truncate the table', 'details': str(e)}), 500

    # Fetch new positions from Alpaca's API
    # Fetch trade activities from Alpaca's API
    response = requests.get(alpaca_endpoint, headers=headers, params={'activity_type': 'FILL'})
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch trade activities from Alpaca', 'status_code': response.status_code}), 500

    trade_activities = response.json()
    print(trade_activities)
    new_positions_count = 0

    # Load new data into the UserTrade table
    for activity in trade_activities:
        if activity['activity_type'] == 'FILL':  # Ensure we're only processing filled trades
            trade_date = parser.parse(activity['transaction_time'])
            new_trade = UserTrade(
                user_id=1,  # Replace with logic to determine user ID
                platform_id=1,  # Replace with logic to determine platform ID
                symbol=activity['symbol'],
                trade_type=activity['side'],  # 'buy' or 'sell'
                price=float(activity['price']),
                quantity=int(activity['qty']),
                total_value=float(activity['qty']) * float(activity['price']),
                trade_date=trade_date
            )
            db.session.add(new_trade)
            new_positions_count += 1

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to load new data', 'details': str(e)}), 500

    return jsonify({'message': f'Successfully refreshed with {new_positions_count} new trades'}), 200

@app.route('/api/user_profiles', methods=['POST'])
def create_user_profile():
    print('Inside create_user_profile')
    data = request.get_json()
    print(data)
    new_profile = UserProfile(
        user_id=data['user_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data.get('phone', None),  # Optional
        trading_api_key=data.get('trading_api_key', None),  # Optional
        trading_api_secret=data.get('trading_api_secret', None)  # Optional
    )
    db.session.add(new_profile)
    db.session.commit()
    return jsonify({'message': 'User profile created successfully'}), 201

@app.route('/api/user_profiles/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    profile = UserProfile.query.get_or_404(user_id)
    return jsonify({
        'user_id': profile.user_id,
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'email': profile.email,
        'phone': profile.phone,
        'trading_api_key': profile.trading_api_key,
        'trading_api_secret': profile.trading_api_secret
    })

@app.route('/api/all_user_profiles', methods=['GET'])
def get_all_user_profiles():
    profiles = UserProfile.query.all()
    all_profiles = [{
        'user_id': profile.user_id,
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'email': profile.email,
        'phone': profile.phone,
        'trading_api_key': profile.trading_api_key,
        'trading_api_secret': profile.trading_api_secret
    } for profile in profiles]
    return jsonify(all_profiles)

@app.route('/api/user_profiles/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    profile = UserProfile.query.get_or_404(user_id)
    data = request.get_json()
    profile.first_name = data['first_name']
    profile.last_name = data['last_name']
    profile.email = data['email']
    profile.phone = data.get('phone', profile.phone)
    profile.trading_api_key = data.get('trading_api_key', profile.trading_api_key)
    profile.trading_api_secret = data.get('trading_api_secret', profile.trading_api_secret)
    db.session.commit()
    return jsonify({'message': 'User profile updated successfully'})

@app.route('/api/user_profiles/<int:user_id>', methods=['DELETE'])
def delete_user_profile(user_id):
    profile = UserProfile.query.get_or_404(user_id)
    db.session.delete(profile)
    db.session.commit()
    return jsonify({'message': 'User profile deleted successfully'})

@app.route('/fetch_stocks', methods=['GET'])
def fetch_stocks():
    # Retrieve the 'index' and 'risk' from the query parameters
    index_name = request.args.get('index')
    risk_level = request.args.get('risk')
    
    # Filter the Stocks based on provided index and risk
    if index_name and risk_level:
        stocks = Stocks.query.filter_by(index_name=index_name, risk=risk_level).all()
        results = [
            {"StockTicker": stock.stock, "CompanyName": stock.company_name}
            for stock in stocks
        ]
        return jsonify(results)
    else:
        return jsonify({"error": "Missing index or risk parameters"}), 400

@app.route('/api/all_user_trades', methods=['GET'])
def get_all_user_trades():
    try:
        # Query all trades in the UserTrade table
        trades = UserTrade.query.all()
        # Serialize the data to JSON format
        trades_list = [{
            'trade_id': trade.trade_id,
            'user_id': trade.user_id,
            'platform_id': trade.platform_id,
            'symbol': trade.symbol,
            'trade_type': trade.trade_type,
            'price': float(trade.price),
            'quantity': trade.quantity,
            'total_value': float(trade.total_value) if trade.total_value else None,
            'trade_date': trade.trade_date.isoformat() if trade.trade_date else None
        } for trade in trades]
        
        return jsonify(trades_list), 200
    except Exception as e:
        # Handle errors in case the database query fails
        return jsonify({'error': 'Unable to fetch user trades', 'details': str(e)}), 500