import os
class Config:
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@35.193.180.216:3306/predict_result"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@"+os.getenv('DB_HOST', '35.193.180.216') +":3306/predict_result"