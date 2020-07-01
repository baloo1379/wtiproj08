import pandas as pd
from . import db
import json


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.INTEGER, primary_key=True)
    pregnancies = db.Column(db.INTEGER, nullable=False)
    glucose = db.Column(db.INTEGER, nullable=False)
    blood_pressure = db.Column(db.INTEGER, nullable=False)
    skin_thickness = db.Column(db.INTEGER, nullable=False)
    insulin = db.Column(db.INTEGER, nullable=False)
    bmi = db.Column(db.FLOAT, nullable=False)
    diabetes_pedigree_function = db.Column(db.FLOAT, nullable=False)
    age = db.Column(db.INTEGER, nullable=False)

    def __repr__(self):
        return f"<Patient(id={self.id}, skin_thickness={self.skin_thickness}, age={self.age}, " \
               f"glucose={self.glucose}, pregnancies={self.pregnancies}, blood_pressure={self.blood_pressure}, " \
               f"diabetes_pedigree_function={self.diabetes_pedigree_function}, insulin={self.insulin}, bmi={self.bmi})>"

    def to_dict(self) -> dict:
        return {
            'Pregnancies': int(self.pregnancies),
            'Glucose': int(self.glucose),
            'BloodPressure': int(self.blood_pressure),
            'SkinThickness': int(self.skin_thickness),
            'Insulin': int(self.insulin),
            'BMI': float(self.bmi),
            'DiabetesPedigreeFunction': float(self.diabetes_pedigree_function),
            'Age': int(self.age),
        }

    def to_data_frame(self) -> pd.DataFrame:
        return pd.DataFrame([self.to_dict()])

    # noinspection PyPep8Naming
    @staticmethod
    def create(SkinThickness, Age, Glucose, Pregnancies, BloodPressure, DiabetesPedigreeFunction, Insulin, BMI):
        p = Patient(skin_thickness=SkinThickness, age=Age, glucose=Glucose, pregnancies=Pregnancies,
                    blood_pressure=BloodPressure, diabetes_pedigree_function=DiabetesPedigreeFunction,
                    insulin=Insulin, bmi=BMI)
        db.session.add(p)
        db.session.commit()
        return p

    @staticmethod
    def find(idx):
        return db.session.query(Patient).filter(Patient.id == idx).first()

    @staticmethod
    def all():
        return db.session.query(Patient).all()
