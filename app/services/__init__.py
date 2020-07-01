from .PredictionService import PredictionService

prediction_service = PredictionService(outcome_name='Outcome', model_name='diabetes',
                                       file_name='diabetes.csv')


def init_app(app):
    pass
