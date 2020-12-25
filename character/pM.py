from character.user import User
from character.character_base import CharacterModel


class CharacterPM(CharacterModel):
    """
    外交的男性のキャラクタモデル
    """

    def __init__(self, user: User):
        super().__init__(user)
        self.personal_pronoun = "俺"

    def __str__(self) -> str:
        return "character-pM"
