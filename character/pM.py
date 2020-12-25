from situation.situation_base import SituationBase
from character.character_base import CharacterModel


class CharacterPM(CharacterModel):
    """
    外交的男性のキャラクタモデル
    """

    def __init__(self, situation: SituationBase):
        super().__init__(situation, self.__str__())

        # 派生クラスで定義するパラメータ
        self.first_personal_pronoun = "俺"
        self.third_personal_pronoun = "お前"

    def reply(self, text):
        super().update_parameter(text)

    def __str__(self) -> str:
        return "character-pM"
