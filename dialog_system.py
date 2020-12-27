from situation.situation_domain_predict import SituationDomainPredict


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

        print("user_utt :", text)
        print("frame", self.situation.frame)
        print("sys_da", self.sys_da)
        print("user_da", self.user_da)


if __name__ == "__main__":
    from character.pM import CharacterPM

    system = DialogSystem()
    system.character = CharacterPM()

    utts = ["今日飯行かね？", "牛丼とかどう？", "海老名にあるんだけど", "美味しいって噂の店だよ"]
    for text in utts:
        system.reply(text)
        print()
