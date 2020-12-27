import os
import dill
import pandas as pd
from helper.tokenizer import tokenizer
from helper.helper_functions import load_json


SITUATION_CONCEPTS = "data/situation_concepts.json"
PREDICT_MODEL = "data/situation_predicter.model"


class SituationDomainPredict(object):
    """
    会話シチュエーションドメインを推定するモデル
    """

    def __init__(self) -> None:
        if os.path.exists(PREDICT_MODEL):
            # モデルをロード
            self.__load_model()

    def __load_model(self):
        with open(PREDICT_MODEL, "rb") as f:
            self.vectorizer = dill.load(f)
            self.label_encoder = dill.load(f)
            self.svc = dill.load(f)

    def predict_da(self, text):
        """対話行為タイプを推定"""
        X = self.vectorizer.transform([text])  # ベクトル化
        Y = self.svc.predict(X)  # 予測
        da = self.label_encoder.inverse_transform(Y)[0]  # ラベルを返す
        return da

    def get_situation(self, text):
        """シチュエーションを推定してクラスを返す"""
        situation_type = self.predict_da(text)

        if situation_type == "situation-eat":
            from situation.situation_eat import SituationEat

            return SituationEat

