from situation.situation_base import SituationBase
from character.character_base import CharacterModel


# パラメータの初期値
INITIAL_EMOTION = 0.3
INITIAL_INTERST = 0.0
INITIAL_INTIMACY = 0.0
THRESHOLD = 0.6


class CharacterNM(CharacterModel):
    """
    内向的男性のキャラクタモデル
    """

    def __init__(self, situation: SituationBase):
        super().__init__(situation, self.__str__())

        # 派生クラス内で利用するフィールド変数
        self.emotion = INITIAL_EMOTION
        self.interest = INITIAL_INTERST
        self.intimacy = INITIAL_INTIMACY

        # 更新されたか感知するため、前のパラメータを保持
        self.pre_emotion = INITIAL_EMOTION
        self.pre_interest = INITIAL_INTERST
        self.pre_intimacy = INITIAL_INTIMACY

        # 派生クラスで定義するパラメータ
        self.first_personal_pronoun = "僕"  # 一人称代名詞
        self.third_personal_pronoun = "君"  # 三人称代名詞
        self.check_concept = "__concept__だね。"  # コンセプトを確認するセリフ

    def __convert_check_concept_utt(self):
        text = ""
        f = self._situation.frame
        user_da = self._situation.user_da

        for key in f.keys():
            utt_type = "anser-" + key
            if user_da == utt_type:
                text += self.check_concept.replace("__concept__", f[key])
        return text

    def reply(self, text):
        super()._update_parameter(text)
        if self._situation.sys_da == "anser" or self._situation.sys_da == "chatting":
            utt_type = super()._get_sysda_by_anser(THRESHOLD)
            sysda = self._situation.anser_sysda(utt_type)
            return self.utt[sysda]
        else:
            utt = self.utt[self._situation.sys_da]
            return self.__convert_check_concept_utt() + utt

    def __str__(self) -> str:
        return "character-nM"
