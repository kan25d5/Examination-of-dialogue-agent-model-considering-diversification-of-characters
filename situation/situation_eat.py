import re
from situation.situation_base import SituationBase


OTHER_UTT = ["他はいないよ", "他にはいないよ"]


class SituationEat(SituationBase):
    """
    食事会話シチュエーションモデル
    """

    def __init__(self) -> None:
        super().__init__(self.__str__())
        self.__re_nop = re.compile(r"\d+人")

    def update_frame(self, text):
        self._update_frame(text)

    def get_sys_da(self, point, threshold_point):
        if self.check_fill_frame():
            if not self.check_update_frame():
                self.user_da = "chatting"
            if point >= threshold_point:
                self.sys_da = "act"
            else:
                self.sys_da = "not-act"
        else:
            for key in self.frame.keys():
                if self.frame[key] == "":
                    self.sys_da = "ask-" + key

        return self.sys_da

    def __str__(self) -> str:
        return "situation-eat"
