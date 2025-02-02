from webapp.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Cards(db.Model):
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=True)
    number = db.Column(db.Integer, nullable=False)
    col_id = db.Column(db.Integer, ForeignKey("col.id"))
    col = relationship("Col", back_populates="cards")

    def __repr__(self):
        return "<Cards {}>".format(self.text)