import copy
import oseti
from situation.situation_base import SituationBase
from stadist_simple_api.api import Stations
from helper.helper_functions import load_json

MAX_DISTANCE = 45000
CHARACTER_PARAMETER_SETTING_PATH = "data/character_parameter_setting.json"


class CharacterModel(object):
    """
    キャラクタの基底モデル
    """

    def __init__(self, situation: SituationBase, character_label: str):
        # クラス内で共有するパラメータ
        self._reply_count = 0
        self._situation = situation
        self.__previous_situation_frame = {}
        self.__oseti = oseti.Analyzer()
        self.__concepts = load_json(CHARACTER_PARAMETER_SETTING_PATH)[self.__str__()]

        # キャラクタモデルのパラメータ
        self.emotion = 0.5  # 感情度
        self.interest = 0.0  # 関心度
        self.intimacy = 0.0  # 親密度

        # 派生クラスで定義するパラメータ
        self.first_personal_pronoun = ""  # 一人称代名詞
        self.third_personal_pronoun = ""  # 三人称代名詞
        self.threshold_emotion = 0.0  # 感情値の閾値
        self.threshold_interest = 0.0  # 関心度の閾値
        self.threshold_intimacy = 0.0  # 親密度の閾値

    def get_emotion_by_distance(self):
        # ２駅間の距離を算出
        distance = Stations().api("", self._situation.frame["place"])
        # 距離をMAX_DISTANCE以上にしない
        distance = distance if distance < MAX_DISTANCE else MAX_DISTANCE
        # [0,1]で正規化
        emotion = distance / MAX_DISTANCE
        return emotion

    def get_emotion_by_text(self, text):
        # ネガポジ値を[0,1]で得る
        point = self.__oseti.analyze(text)[0]
        # ネガポジ値を[-1,1]で得る
        emotion = ((2 * point - 1) / 2) * 2
        return emotion

    def __is_update_frame(self, frame):
        return self.__previous_situation_frame != frame

    def update_parameter(self, text):
        """テキストからキャラクタモデルのパラメーターを更新"""
        f = self._situation.frame

        # コンセプト毎に関心度を更新
        for key in f.keys():
            if f[key] != "":
                if key not in self.__concepts.keys():
                    continue
                concept_dic = self.__concepts[key]
                if f[key] not in concept_dic.keys():
                    continue
                concept = concept_dic[f[key]]
                self.emotion += concept["emotion"]
                self.interest += concept["interest"]
                self.intimacy += concept["interest"]

        if self.__is_update_frame(f):
            # フレーム情報が更新されるなら、場所から感情値の更新
            if "place" in f.keys():
                if f["place"] != "":
                    self.emotion -= self.get_emotion_by_distance()
        else:
            # フレーム情報が更新されない意味のない発話なら
            # その発話からネガポジ値を推定し感情値に反映
            self.emotion += self.get_emotion_by_text(text)

        # 値渡しで__previous_situation_frameに現在のフレームを更新
        self.__previous_situation_frame = copy.deepcopy(f)
