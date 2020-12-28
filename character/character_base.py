import oseti
import pandas as pd
from helper.cabocha_helper import USER_DIC
from helper.helper_functions import load_json


MAX_DISTANCE = 40000
CHARACTER_PARAM_SET = "data/character_parameter_setting.json"
STATION_FILE_PATH = "data/stations-simplify.csv"
UTT_PATH = "data/character_utt.json"


class CharacterBase(object):
    """
    キャラクタモデルの基底クラス
    """

    def __init__(self, character_label: str):
        # 派生クラス内で定義するフィールド変数
        self.emotion = 0.0  # 感情度
        self.interest = 0.5  # 関心度
        self.intimacy = 0.0  # 親身度
        self.threshold_point = 0.0  # 行動する／しないの閾値
        self.first_personal_pronoun = ""  # 一人称代名詞
        self.third_personal_pronoun = ""  # 三人称代名詞
        self.now_time = 18

        # 基底クラスが保持するフィールド変数
        self.situation = None
        self.character_label = character_label
        self.params_set = load_json(CHARACTER_PARAM_SET)[self.character_label]

        # 基底クラスが保持するプライベートフィールド変数
        self.__oseti = oseti.Analyzer(USER_DIC)

    def set_situation(self, situation):
        self.situation = situation
        self.utt = load_json(UTT_PATH)[str(self.situation.situation_str)][
            self.character_label
        ]

    def calculate_point(self) -> float:
        """総合点を算出"""
        return (self.emotion + self.interest + self.intimacy) / 3

    def update_point(self, text):
        sys_da = self.situation.sys_da
        user_da = self.situation.user_da
        if user_da == "chatting":
            # フレームが更新されないならネガポジ値を算出
            self.__update_emotion_by_text(text)
        elif self.situation._is_fill_frame():
            # コンセプト毎に感情度・関心度を評価する
            self.situation.update_parameter_by_frame()
            for key in self.params_set.keys():
                concept = self.situation.frame[key]
                param_set = self.params_set[key][concept]
                self.emotion += param_set["emotion"]
                self.interest += param_set["interest"]

    def __update_emotion_by_text(self, text):
        """フレームが更新されないテキストからネガポジ値を算出"""
        emotion = 0
        for point in self.__oseti.analyze(text):
            emotion += ((2 * point - 1) / 2) * 2

        self.emotion += emotion
