from webapp.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Boards(db.Model):
    __tablename__ = "boards"
    id = db.Column(db.Integer, primary_key=True)
    board_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="boards")
    col = relationship("Col", back_populates="boards")

    def __repr__(self):
        return "<Boards {}>".format(self.board_name)

