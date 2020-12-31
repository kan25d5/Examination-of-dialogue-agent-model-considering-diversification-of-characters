from character.character_base import CharacterBase
from situation.situation_base import SituationBase


# 行動する／しないの閾値
THRESHOLD_POINT = 0.3


class CharacterPM(CharacterBase):
    """
    外交的男性のキャラクタモデル
    """

    def __init__(self, situation: SituationBase):
        super().__init__(situation, self.__str__())

        # 派生クラス内で定義するフィールド変数
        self.threshold_point = THRESHOLD_POINT  # 行動する／しないの閾値
        self.first_personal_pronoun = ""  # 一人称代名詞
        self.third_personal_pronoun = ""  # 三人称代名詞

    def reply(self, text):
        sys_da = self.get_sys_da(text, THRESHOLD_POINT)
        sys_utt = self.utt[sys_da]

        return self.convert_utt.convert_text(sys_utt)

    def __str__(self) -> str:
        return "character-pM"
