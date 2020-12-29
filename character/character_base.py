import oseti
import pandas as pd
from helper.cabocha_helper import USER_DIC
from helper.helper_functions import load_json
from numpy import sqrt


MAX_DISTANCE = 40000
MAX_DISTANCE = 40000
CHARACTER_PARAM_SET = "data/character_parameter_setting.json"
UTT_PATH = "data/character_utt.json"
STATION_FILE_PATH = "data/stations-simplify.csv"


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
        self.__sation_df = pd.read_csv(STATION_FILE_PATH)
        self.__pre_frame = {}

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
        frame = self.situation.frame

        if user_da == "chatting":
            # フレームが更新されないならネガポジ値を算出
            self.__update_emotion_by_text(text)
        else:
            for key in frame.keys():
                if key not in self.__pre_frame.keys():
                    if frame[key] != "":
                        self.__update_param_by_frame(key, frame[key])
                        self.__pre_frame.update({key: frame[key]})

    def __update_param_by_frame(self, key, concept):
        if key == "place":
            self.__update_interest_by_distance(concept)
            return
        if concept not in self.params_set[key].keys():
            return
        param = self.params_set[key][concept]
        self.emotion += param["emotion"]
        self.interest += param["interest"]

    def __update_emotion_by_text(self, text):
        """フレームが更新されないテキストからネガポジ値を算出"""
        emotion = 0
        for point in self.__oseti.analyze(text):
            emotion += ((2 * point - 1) / 2) * 2

        self.emotion += emotion

    def __get_distance(self, dest):
        """神奈川工科大学から場所までの距離を算出"""
        # ox, oy = df[df.station == orig].iloc[0, :].values[1:3]
        df = self.__sation_df
        ox, oy = -44662, -56845
        dx, dy = df[df.station == dest].iloc[0, :].values[1:3]
        return int(round(sqrt((ox - dx) ** 2 + (oy - dy) ** 2)))

    def __update_interest_by_distance(self, place):
        """近いとの距離から感情度を加算"""
        # ２駅間の距離を算出
        distance = self.__get_distance(place)
        # 距離をMAX_DISTANCE以上にしない
        distance = distance if distance < MAX_DISTANCE else MAX_DISTANCE
        # [0,1]で正規化
        interest = distance / MAX_DISTANCE
        print("interest", interest)

        self.interest -= interest
