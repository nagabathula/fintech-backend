from run import db

class UserCredentials(db.Model):
    __tablename__ = 'finprj_user_credentials'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.CHAR(60), nullable=False)

class UserProfile(db.Model):
    __tablename__ = 'finprj_user_profile'
    user_id = db.Column(db.Integer, db.ForeignKey('finprj_user_credentials.id'), primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    trading_api_key = db.Column(db.String(255))
    trading_api_secret = db.Column(db.String(255))

class TradingPlatform(db.Model):
    __tablename__ = 'finprj_trading_platforms'
    platform_id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.String(255), unique=True, nullable=False)
    platform_description = db.Column(db.Text)

class UserTrade(db.Model):
    __tablename__ = 'finprj_user_trades'
    trade_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('finprj_user_credentials.id'), nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey('finprj_trading_platforms.platform_id'), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    trade_type = db.Column(db.Enum('buy', 'sell'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_value = db.Column(db.Numeric(15, 2))
    trade_date = db.Column(db.DateTime, nullable=False)

class Stocks(db.Model):
    __tablename__ = 'Stocks'

    stock = db.Column('Stock', db.String(10), primary_key=True)
    company_name = db.Column('CompanyName', db.String(100), nullable=False)
    index_name = db.Column('IndexName', db.String(20), nullable=False)
    risk = db.Column('Risk', db.String(10), nullable=False)


class StockPrediction(db.Model):
    __tablename__ = 'stock_prediction'

    ticker = db.Column(db.String(16383), primary_key=True)
    company_name = db.Column(db.String(16383))
    sector = db.Column(db.String(16383))
    market_cap = db.Column(db.BigInteger)
    beta = db.Column(db.Float)
    volatility = db.Column(db.Float)
    risk_category = db.Column(db.Float)
    predicted_returns = db.Column(db.Float)