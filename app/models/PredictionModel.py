import pandas as pd
from . import db
import json


class PredictionModel(db.Model):
    __tablename__ = 'prediction_models'
    id = db.Column(db.INTEGER, primary_key=True)
    data_path = db.Column(db.VARCHAR, nullable=False)
    file_path = db.Column(db.VARCHAR, nullable=False)

    def __repr__(self):
        return f"<PredictionModel(id={self.id}, data_path={self.data_path}, file_path={self.file_path}"

    def to_dict(self) -> dict:
        return {
            'data_path': self.data_path,
            'file_path': self.file_path
        }

    @staticmethod
    def create(data_path, file_path):
        p = PredictionModel(data_path=data_path, file_path=file_path)
        db.session.add(p)
        db.session.commit()
        return p

    @staticmethod
    def find(idx):
        return db.session.query(PredictionModel).filter(PredictionModel.id == idx).first()

    @staticmethod
    def all():
        return db.session.query(PredictionModel).all()
