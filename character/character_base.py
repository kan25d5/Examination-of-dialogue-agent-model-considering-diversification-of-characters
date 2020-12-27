import copy
import oseti
from situation.situation_base import SituationBase
from stadist_simple_api.api import Stations
from helper.helper_functions import load_json


# 設定値
MAX_DISTANCE = 40000
CHARACTER_PARAMETER_SETTING_PATH = "data/character_parameter_setting.json"
UTT_PATH = "data/utt.json"


class CharacterModel(object):
    """
    キャラクタの基底モデル
    """

    def __init__(self, situation: SituationBase, character_label: str):
        # クラス内で共有するパラメータ
        self._reply_count = 0
        self._situation = situation
        self.__oseti = oseti.Analyzer()
        self.__concepts = load_json(CHARACTER_PARAMETER_SETTING_PATH)[character_label]
        self.utt = load_json(UTT_PATH)[str(self._situation)]
        self.pre_frame = self.get_init_frame()

        # 派生クラスで定義するパラメータ
        self.first_personal_pronoun = ""  # 一人称代名詞
        self.third_personal_pronoun = ""  # 三人称代名詞
        self.threshold_emotion = 0.0  # 感情値の閾値
        self.threshold_interest = 0.0  # 関心度の閾値
        self.threshold_intimacy = 0.0  # 親密度の閾値
        self.expression_disapproval = ""  # 難色を示すセリフ
        self.expression_pleasure = ""  # 喜びを表すセリフ

    def get_init_frame(self):
        return {key: "" for key in self._situation.frame.keys()}

    def __update_emotion_by_distance(self):
        """近いとの距離から感情度を算出"""
        # ２駅間の距離を算出
        distance = Stations().api("", self._situation.frame["place"])
        # 距離をMAX_DISTANCE以上にしない
        distance = distance if distance < MAX_DISTANCE else MAX_DISTANCE
        # [0,1]で正規化
        emotion = distance / MAX_DISTANCE

        print("emotion", self.emotion, emotion)
        self.emotion -= emotion

    def __update_emotion_by_text(self, text):
        """フレームが更新されないテキストからネガポジ値を算出"""
        emotion = 0
        for point in self.__oseti.analyze(text):
            emotion += ((2 * point - 1) / 2) * 2

        print("emotion", self.emotion, emotion)
        self.emotion += emotion

    def __update_parameter_if_update_frame(self):
        """
        発話によってフレーム情報が更新された場合、
        フレーム情報から関心度・感情度・親密度を算出
        """
        f = self._situation.frame
        pre_f = self.pre_frame

        # コンセプト毎に関心度を更新
        for key in f.keys():
            if f[key] == "":
                continue
            if key not in self.__concepts.keys():
                continue
            concept_dic = self.__concepts[key]
            if f[key] not in concept_dic.keys():
                continue
            if f[key] == pre_f[key]:
                continue
            concept = concept_dic[f[key]]

            print("emotion", self.emotion, concept["emotion"])
            print("interest", self.interest, concept["interest"])
            self.emotion += concept["emotion"]
            self.interest += concept["interest"]

        if f["place"] != "" and f["place"] != pre_f["place"]:
            self.__update_emotion_by_distance()

    def _convert_utt(self, text: str):
        f = self._situation.frame
        for key in f.keys():
            concept = "__" + key + "__"
            text = text.replace(concept, f[key])
        return text

    def _get_sysda_by_anser(self, threshold):
        point = self.calculate_point()
        if point < threshold:
            return "negative"
        else:
            return "positive"

    def calculate_point(self):
        return (self.emotion + self.interest + self.intimacy) / 3

    def _update_parameter(self, text):
        """テキストからキャラクタモデルのパラメーターを更新"""
        if self._situation.user_da == "chatting":
            # フレーム情報が更新されないなら
            # その発話からネガポジ値を判定
            self.__update_emotion_by_text(text)
        else:
            # フレーム情報が更新されるなら
            # フレーム情報から感情値・関心度・親密度の更新
            self.__update_parameter_if_update_frame()

        self.pre_frame = copy.deepcopy(self._situation.frame)
