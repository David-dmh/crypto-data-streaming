from flask_sqlalchemy import SQLAlchemy

# session_options={"expire_on_commit": False} =>
# would allow to manipulate out of date models
# after a transaction has been committed
# ! be aware that the above can have unintended side effects

db = SQLAlchemy()


# class CryptoList(db.Model):
#     __tablename__ = "crypto_lists"

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#         autoincrement=True,
#         unique=True)

#     name = db.Column(db.String(), nullable=False)
#     # crypto = db.relationship(
#     #     "Crypto",
#     #     backref="list",
#     #     cascade="all, delete-orphan")

#     def __repr__(self):
#         return f"<CryptoList {self.id}, {self.name}>"


class CryptoModel(db.Model):
    __tablename__ = "crypto"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_btc = db.Column(db.Boolean, nullable=False, default=False)
    description = db.Column(db.String(), nullable=False)
    my_date = db.Column(db.DateTime, nullable=True)

    # list_id = db.Column(
    #     db.Integer,
    #     db.ForeignKey("crypto_lists.id"),
    #     nullable=False
    # )

    def __repr__(self):
        return f"<CryptoModel {self.id}, {self.completed}, {self.description}>"
    
class MasterDataModel(db.Model):
    __tablename__ = "master_data"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lookup_col = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<MasterDataModel {self.id}, {self.completed}, {self.description}>"
    
        
