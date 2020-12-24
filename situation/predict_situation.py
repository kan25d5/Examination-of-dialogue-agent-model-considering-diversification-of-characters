import os
import dill
import pandas as pd
from helper.tokenizer import tokenizer
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from data.generate_samples import GenerateSamples
from helper.helper_functions import load_json


SITUATION_CONCEPTS = "data/situation_concepts.json"


class PredictSituation(object):
    def __init__(self, situation_name, is_base_situation=False):
        self.situation_name = situation_name
        self.is_base_situation = is_base_situation
        self.model_path = "situation/" + self.situation_name + ".model"

        if os.path.exists(self.model_path):
            self.load_model()
        else:
            self.load_generate_csv()
            self.training_predicter()

    def load_model(self):
        with open(self.model_path, "rb") as f:
            self.vectorizer = dill.load(f)
            self.label_encoder = dill.load(f)
            self.svc = dill.load(f)

    def load_generate_csv(self):
        base_training_file = "data/" + self.situation_name + ".xml"
        training_file = "data/" + self.situation_name + ".csv"
        json_dic = load_json(SITUATION_CONCEPTS)

        if self.is_base_situation:
            dic = {}
            for dic_ in json_dic.values():
                dic.update(dic_)
        else:
            dic = json_dic[self.situation_name]

        gs = GenerateSamples(base_training_file, training_file, dic)
        gs.generate_samples()

        self.df = pd.read_csv(training_file)

    def training_predicter(self):
        self.vectorizer = TfidfVectorizer(analyzer=tokenizer)
        X = self.vectorizer.fit_transform(self.df["utt"])

        self.label_encoder = LabelEncoder()
        Y = self.label_encoder.fit_transform(self.df["dialog_act_type"])
        print(Y)

        self.svc = SVC(gamma="scale")
        self.svc.fit(X, Y)

        with open(self.model_path, "wb") as f:
            dill.dump(self.vectorizer, f)
            dill.dump(self.label_encoder, f)
            dill.dump(self.svc, f)

    def predict_situation(self, text):
        X = self.vectorizer.transform([text])
        Y = self.svc.predict(X)
        da = self.label_encoder.inverse_transform(Y)[0]
        return da
