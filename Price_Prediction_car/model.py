from connection import db


class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key = True)
    Year  = db.Column(db.String(100))
    ShowroomPrice = db.Column(db.String(100))
    Kilometers = db.Column(db.String(100))
    Owners = db.Column(db.String(100))
    FuelType =db.Column(db.String(100))
    SellerType = db.Column(db.String(100))
    TransmissionType = db.Column(db.String(100))
    PredictedPrice = db.Column(db.String(100))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
