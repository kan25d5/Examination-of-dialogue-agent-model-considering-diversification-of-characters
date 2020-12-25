from situation.situation_base import SituationBase


class SituationEat(SituationBase):
    """
    docstring
    """

    def __init__(self) -> None:
        super().__init__(self.__str__())

    def __update_sysda(self, text) -> str:
        return "test"

    def get_sysda(self, text):
        self._update_frame(text)
        self.sys_da = self.__update_sysda(text)
        return self.sys_da

    def __str__(self) -> str:
        return "situation-eat"
