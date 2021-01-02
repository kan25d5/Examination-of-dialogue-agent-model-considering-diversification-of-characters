from character.character_base import CharacterBase
from situation.situation_base import SituationBase

# 行動する／しないの閾値
THRESHOLD_POINT = 0.7


class CharacterPF(CharacterBase):
    """
    外交的女性のキャラクタモデル
    """

    def __init__(self, situation: SituationBase):
        super().__init__(situation, self.__str__())

        # 派生クラス内で定義するフィールド変数
        self.threshold_point = THRESHOLD_POINT  # 行動する／しないの閾値
        self.first_personal_pronoun = "私"  # 一人称代名詞
        self.second_personal_pronoun = "君"  # 二人称代名詞

    def reply(self, text):
        self.user_utt = text
        sys_da = self.get_sys_da(self.user_utt, THRESHOLD_POINT)
        self.sys_utt = self.utt[sys_da]
        self.sys_utt = self._convert_text(self.sys_utt)

        return self.sys_utt

    def __str__(self) -> str:
        return "character-pF"
