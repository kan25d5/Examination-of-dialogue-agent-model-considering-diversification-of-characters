from character.character_base import CharacterBase
from situation.situation_base import SituationBase


# 行動する／しないの閾値
THRESHOLD_POINT = 0.3


class CharacterPM(CharacterBase):
    """
    外交的男性のキャラクタモデル
    """

    def __init__(self):
        super().__init__(self.__str__())

        # 派生クラス内で定義するフィールド変数
        self.threshold_point = THRESHOLD_POINT  # 行動する／しないの閾値
        self.first_personal_pronoun = ""  # 一人称代名詞
        self.third_personal_pronoun = ""  # 三人称代名詞

    def reply(self, text):
        return self.utt[self.situation.sys_da]

    def __str__(self) -> str:
        return "character-pM"
