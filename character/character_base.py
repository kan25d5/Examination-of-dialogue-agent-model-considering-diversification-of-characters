import oseti
import pandas as pd
from helper.cabocha_helper import USER_DIC
from helper.helper_functions import load_json


MAX_DISTANCE = 40000
CHARACTER_PARAMETER_SETTING_PATH = "data/character_parameter_setting.json"
STATION_FILE_PATH = "data/stations-simplify.csv"
UTT_PATH = "data/character_utt.json"


class CharacterBase(object):
    """
    キャラクタモデルの基底クラス
    """

    def __init__(self, character_label: str):
        # 派生クラス内で定義するフィールド変数
        self.emotion = 0.0  # 感情度
        self.interest = 0.0  # 関心度
        self.intimacy = 0.0  # 親身度
        self.threshold_point = 0.0  # 行動する／しないの閾値
        self.first_personal_pronoun = ""  # 一人称代名詞
        self.third_personal_pronoun = ""  # 三人称代名詞
        self.now_time = 18

        # 基底クラスが保持するフィールド変数
        self.situation = None
        self.character_label = character_label
        self.check_concept = "__concept__ですね。"  # コンセプトを確認するセリフ

        # 基底クラスが保持するプライベートフィールド変数
        self.__oseti = oseti.Analyzer(USER_DIC)

    def set_situation(self, situation):
        self.situation = situation
        self.utt = load_json(UTT_PATH)[str(self.situation.situation_str)]

    def calculate_point(self):
        """総合点を算出"""
        return (self.emotion + self.interest + self.intimacy) / 3
