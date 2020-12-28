from situation.situation_domain_predict import SituationDomainPredict
from character.pM import CharacterPM

CM = CharacterPM()
UTTS = ["今日飯行かね？", "焼肉とかどう？", "海老名にあるんだけど", "美味しいって噂の店だよ"]


class DialogSystem(object):
    """
    対話システム全体を管理するクラス
    """

    def __init__(self) -> None:
        self.user_da = ""
        self.sys_da = ""
        self.is_init = True
        self.character = None
        self.situation = None

        self.__predict_situation = SituationDomainPredict()

    def reply(self, text):
        if self.is_init:
            self.situation = self.__predict_situation.get_situation(text)()
            self.situation.set_character(self.character)
            self.character.set_situation(self.situation)
            self.is_init = False

        self.user_da = self.situation.update_user_da()
        self.sys_da = self.situation.update_sys_da(text)
        reply = self.character.reply(text)

        print("user_utt :", text)
        print("sys_utt :", reply)
        print("frame", self.situation.frame)
        print("sys_da", self.sys_da)
        print("user_da", self.user_da)
        print("感情度", self.character.emotion)
        print("関心度", self.character.interest)
        print("親身度", self.character.intimacy)
        print("point", self.character.calculate_point())


if __name__ == "__main__":

    system = DialogSystem()
    system.character = CM

    utts = UTTS
    for text in utts:
        system.reply(text)
        print()
