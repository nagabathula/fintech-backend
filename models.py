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
