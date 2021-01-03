import os
import dill
import pandas as pd
from data.generate_samples import GenerateSamples
from helper.tokenizer import tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC


SITUATION_CONCEPTS = "data/situation_concepts.json"
PREDICT_MODEL = "data/situation_predicter.model"
TRAINING_DATA_PATH = "data/situation_predicter.csv"


class SituationDomainPredict(object):
    """
    会話シチュエーションドメインを推定するモデル
    """

    def __init__(self) -> None:
        if os.path.exists(PREDICT_MODEL):
            # モデルをロード
            self.__load_model()
        else:
            # モデルを作成
            self.create_predict_model()

    def create_predict_model(self):
        # 訓練データの増幅
        GenerateSamples().generate_samples()
        # 訓練データをDataFrameへ変換
        self.training_data = pd.read_csv(TRAINING_DATA_PATH)
        # シチュエーション予測モデルを学習
        self.__training_predicter_model()
        # モデルを保存
        self.__write_model()

    def __training_predicter_model(self):
        # 発話データを分かち書きしてベクトル化
        self.vectorizer = TfidfVectorizer(analyzer=tokenizer)
        X = self.vectorizer.fit_transform(self.training_data["utt"])

        # 対話行為タイプをラベル化
        self.label_encoder = LabelEncoder()
        Y = self.label_encoder.fit_transform(self.training_data["dialog_act_type"])

        # SVMで学習
        self.svc = SVC(gamma="scale")
        self.svc.fit(X, Y)

    def __load_model(self):
        with open(PREDICT_MODEL, "rb") as f:
            self.vectorizer = dill.load(f)
            self.label_encoder = dill.load(f)
            self.svc = dill.load(f)

    def __write_model(self):
        with open(PREDICT_MODEL, "wb") as f:
            dill.dump(self.vectorizer, f)
            dill.dump(self.label_encoder, f)
            dill.dump(self.svc, f)

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

            return SituationEat()
        elif situation_type == "situation-game":
            from situation.situation_game import SituationGame

            return SituationGame()

