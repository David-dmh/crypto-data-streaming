from flask_sqlalchemy import SQLAlchemy

# session_options={"expire_on_commit": False} =>
# would allow to manipulate out of date models
# after a transaction has been committed
# ! be aware that the above can have unintended side effects

db = SQLAlchemy()

class FactPriceModel(db.Model):
    __tablename__ = "fact_price"

    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    date = db.Column(db.TIMESTAMP, nullable=False, default=False)
    coin_id = db.Column(db.BIGINT, nullable=False)
    price = db.Column(db.DECIMAL(precision=5, scale=5), nullable=True)
    checksum = db.Column(db.VARCHAR(512), nullable=True)

    def __repr__(self):
        return f"""
        <FactPriceModel
        {self.id}, 
        {self.date}, 
        {self.coin_id}>
        {self.price}>
        {self.checksum}>
        """
    
class DimCoinModel(db.Model):
    __tablename__ = "dim_coin"

    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    coin_symbol = db.Column(db.VARCHAR(64), nullable=False, default=False)
    coin_name = db.Column(db.VARCHAR(512), nullable=False, default=False)
    checksum = db.Column(db.VARCHAR(512), nullable=False, default=False)


    def __repr__(self):
        return f"""
        <DimCoinModel
        {self.id}, 
        {self.coin_symbol}, 
        {self.coin_name}, 
        {self.checksum}>
        """
