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


class PredictDialogActType(object):
    """
    対話行為推定モデル

    parameter
    ------------
    situation_name : str
      推定したいシチュエーションの名前
      同名の訓練元データがdataフォルダ内に存在している必要がある

    is_base_situation : bool(False)
      ユーザの第一発話から
      シチュエーションを推定するモデルの生成したい場合
    """

    def __init__(self, situation_name, is_base_situation=False):
        self.situation_name = situation_name
        self.is_base_situation = is_base_situation
        self.model_path = "situation/" + self.situation_name + ".model"

        if os.path.exists(self.model_path):
            # モデルをロード
            self.load_model()
        else:
            # モデルを作成する
            self.generate_training_data()
            self.train_predicter()

    def load_model(self):
        with open(self.model_path, "rb") as f:
            self.vectorizer = dill.load(f)
            self.label_encoder = dill.load(f)
            self.svc = dill.load(f)

    def generate_training_data(self):
        base_training_file = "data/" + self.situation_name + ".xml"
        training_file = "data/" + self.situation_name + ".csv"
        json_dic = load_json(SITUATION_CONCEPTS)

        if self.is_base_situation:
            # シチュエーション推定モデルなら
            # コンセプトデータを結合して訓練データを生成
            dic = {}
            for dic_ in json_dic.values():
                dic.update(dic_)
        else:
            # 特定のシチュエーションの対話行為タイプの推定なら
            # そのシチュエーションのコンセプトを渡す
            dic = json_dic[self.situation_name]

        # 訓練元データを増幅させた訓練データを生成
        gs = GenerateSamples(base_training_file, training_file, dic)
        gs.generate_samples()

        # 訓練データをDataFrameへ変換
        self.training_data = pd.read_csv(training_file)

    def train_predicter(self):
        # 発話データを分かち書きしてベクトル化
        self.vectorizer = TfidfVectorizer(analyzer=tokenizer)
        X = self.vectorizer.fit_transform(self.training_data["utt"])

        # 対話行為タイプをラベル化
        self.label_encoder = LabelEncoder()
        Y = self.label_encoder.fit_transform(self.training_data["dialog_act_type"])

        # SVMで学習
        self.svc = SVC(gamma="scale")
        self.svc.fit(X, Y)

        # モデルをアウトプット
        with open(self.model_path, "wb") as f:
            dill.dump(self.vectorizer, f)
            dill.dump(self.label_encoder, f)
            dill.dump(self.svc, f)

    def predict_da(self, text):
        """対話行為タイプを推定"""
        X = self.vectorizer.transform([text])  # ベクトル化
        Y = self.svc.predict(X)  # 予測
        da = self.label_encoder.inverse_transform(Y)[0]  # ラベルを返す
        return da
