from flask import Blueprint, jsonify, request
from app.models.Patient import Patient
from app.services import prediction_service

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    return jsonify(status="Hello world")


@bp.route('/patient-record', methods=['POST'])
def patient_record():
    if request.content_type.lower() != 'application/json':
        return jsonify(error='Wrong Content-Type'), 415
    data = request.get_json()
    p = Patient.create(**data)
    return jsonify(patient_id=p.id)


@bp.route('/patient-prediction/<patient_id>')
def patient_prediction(patient_id):
    patient = Patient.find(patient_id)
    prediction_service.load_model()
    prediction = prediction_service.predict(patient.to_data_frame())
    return jsonify(probability_of_diabetes=prediction)


@bp.route('/model', methods=['PUT'])
def model():
    if request.content_type.lower() != 'application/json':
        return jsonify(error='Wrong Content-Type'), 415
    data = request.get_json()
    prediction_service.prepare_model()
    prediction_service.save_model(**data)
    prediction_service.plot()
    return jsonify(accuracy=prediction_service.test_accuracy())


@bp.route('/plot')
def plot():
    prediction_service.load_model()
    prediction_service.plot()
    prediction_service.plot2()
    return jsonify(status='OK')
