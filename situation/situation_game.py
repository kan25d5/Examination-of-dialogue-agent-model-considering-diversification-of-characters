from situation.situation_base import SituationBase


class SituationGame(SituationBase):
    """
    ゲームに誘う会話シチュエーション
    """

    def __init__(self):
        super().__init__(self.__str__())

    def update_frame(self, text):
        self._update_frame(text)
        if self.__re_nop.match(text) is not None:
            v = self.__re_nop.match(text).group(0)
            self.frame["number-of-people"] = v

    def get_sys_da(self, point, threshold_point):
        if self.check_fill_frame():
            if not self.check_update_frame():
                self.user_da = "chatting"
            if point > threshold_point:
                self.sys_da = "act"
            else:
                self.sys_da = "not-act"
        else:
            for key in self.frame.keys():
                if self.frame[key] == "":
                    self.sys_da = "ask-" + key

        return self.sys_da

    def __str__(self) -> str:
        return "situation-game"
