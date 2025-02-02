from webapp.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Col(db.Model):
    __tablename__ = "col"
    id = db.Column(db.Integer, primary_key=True)
    col_name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    board_id = db.Column(db.Integer, ForeignKey("boards.id"))
    boards = relationship("Boards", back_populates="col")
    cards = relationship("Cards", back_populates="col")

    def __repr__(self):
        return "<Column {}>".format(self.col_name)