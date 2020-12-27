from numpy.core import _ufunc_reconstruct
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
            return "ask-date"
        elif self.frame["genre"] == "":
            return "ask-genre"
        elif self.frame["place"] == "":
            return "ask-place"
        else:
            if self.user_da == "chatting":
                return "chatting"
            else:
                return "anser"

    def anser_sysda(self, anser_type: str):
        """
        会話シチュエーションで「行かない」
        趣味シチュエーションで「同意しない」場合はnegative
        """
        if self.user_da == "chatting" and self.sys_da == "chatting":
            if anser_type == "negative":
                return "re-reject-invite"
            else:
                return "re-consent-invite"
        else:
            if anser_type == "negative":
                return "reject-invite"
            else:
                return "consent-invite"

    def get_sysda(self, text):
        self._update_frame(text)
        self.sys_da = self.__update_sysda(text)
        return self.sys_da

    def __str__(self) -> str:
        return "situation-eat"
