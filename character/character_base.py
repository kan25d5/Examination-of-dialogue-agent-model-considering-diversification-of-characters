import oseti
from situation.situation_base import SituationBase


class CharacterModel(object):
    """
    キャラクタの基底モデル
    """

    def __init__(self, situation: SituationBase):
        # クラス内で共有するパラメータ
        self._reply_count = 0
        self._situation = situation
        self.__situation_frame = {}

        # キャラクタモデルのパラメータ
        self.emotion = 0.0  # 感情度
        self.interest = 0.0  # 関心度
        self.intimacy = 0.0  # 親密度

        # 派生クラスで定義するパラメータ
        self.personal_pronoun = ""  # 人称代名詞

    def __is_update_frame(self):
        return self.__situation_frame != self._situation.frame

    def parameter_analyzer(self, text):
        """テキストからキャラクタモデルのパラメーターを更新"""
        if self.__is_update_frame():
            # 関心度、親密度の更新
            pass
        else:
            # 感情度の更新
            pass
