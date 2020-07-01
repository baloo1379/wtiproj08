import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix, roc_curve, auc
from joblib import dump, load
import matplotlib.pyplot as plt
from app.models.Patient import Patient


class PredictionService:
    dir = "app/services/"
    file_dir = "data_files/"
    model_dir = "model_files/"

    @staticmethod
    def _accuracy(cm):
        diagonal_sum = cm.trace()
        sum_of_all_elements = cm.sum()
        return diagonal_sum / sum_of_all_elements

    def __init__(self, outcome_name, model_name, file_name):
        self.outcome_name = outcome_name
        self.model_name = f"./{self.dir}{self.model_dir}{model_name}.joblib"
        self.file_name = f"./{self.dir}{self.file_dir}{file_name}"
        self.mlp = MLPClassifier()
        self.parameters = {
            'hidden_layer_sizes': [(50)],
            'activation': ['tanh'],
            'solver': ['adam'],
            'alpha': [0.05],
            'learning_rate': ['adaptive'],
        }
        self.data = pd.read_csv(self.file_name)
        self.X = self.data.loc[:, self.data.columns != self.outcome_name]
        self.y = self.data[self.outcome_name]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y)
        self.X_test.to_csv(f"./{self.dir}{self.file_dir}{model_name}_X_test.csv", index=False)
        self.y_test.to_csv(f"./{self.dir}{self.file_dir}{model_name}_y_test.csv", index=False)
        self.clf = None

    def load_model(self):
        self.clf = load(self.model_name)

    def save_model(self, new_model_file_name=None, *args, **kwargs):
        if new_model_file_name is not None:
            self.model_name = f"./{self.dir}{self.model_dir}{new_model_file_name}.joblib"
        dump(self.clf, self.model_name)

    def prepare_model(self):
        self.clf = GridSearchCV(self.mlp, self.parameters, n_jobs=1, cv=3)
        self.clf.fit(self.X_train, self.y_train)
        best_params = self.clf.best_params_
        self.clf = MLPClassifier(**best_params)
        self.clf.fit(self.X_train, self.y_train)
        # self.clf.fit(self.X, self.y)

    def test_accuracy(self):
        predictions = self.clf.predict(self.X_test)
        cm = confusion_matrix(predictions, self.y_test)
        return self._accuracy(cm)

    def plot(self):
        predictions = self.clf.predict_proba(self.X_test)[:, 0]

        fpr, tpr, thresholds = roc_curve(self.y_test, predictions, pos_label=0)
        AuROC = auc(fpr, tpr)

        plt.figure()
        plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % AuROC)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic from X_test')
        plt.legend(loc="lower right")
        plt.show()
        plt.close()

    def plot2(self):
        ps = Patient.all()
        psd = []
        for p in ps:
            psd.append(p.to_dict())
        P_test = pd.DataFrame(psd)

        predictions2 = self.clf.predict_proba(P_test)[:, 0]

        fpr2, tpr2, thresholds2 = roc_curve(self.y_test, predictions2, pos_label=0)
        AuROC2 = auc(fpr2, tpr2)

        plt.figure()
        plt.plot(fpr2, tpr2, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % AuROC2)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic from db')
        plt.legend(loc="lower right")
        plt.show()
        plt.close()

    def predict(self, data: pd.DataFrame):
        return self.clf.predict_proba(data)[:, 0][0]
