import copy
from situation.situation_base import SituationBase


class SituationEat(SituationBase):
    """
    ご飯誘いシチュエーション
    """

    def __init__(self) -> None:
        self.pre_frame = {}
        super().__init__(self.__str__())

    def __update_sysda(self, text) -> str:
        if self.frame["date"] == "":
            self.is_update_frame = True
            return "ask-date"
        elif self.frame["place"] == "":
            return "ask-place"
        elif self.frame["type"] == "":
            return "ask-type"
        elif self.frame["genre"] == "":
            return "ask-genre"
        else:
            return "anser"

    def get_sysda(self, text):
        self._update_frame(text)
        self.sys_da = self.__update_sysda(text)
        return self.sys_da

    def __str__(self) -> str:
        return "situation-eat"
