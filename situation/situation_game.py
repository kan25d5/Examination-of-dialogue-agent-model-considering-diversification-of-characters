from situation.situation_base import SituationBase


class SituationGame(SituationBase):
    """
    ゲームに誘う会話シチュエーション
    """

    def __init__(self):
        super().__init__(self.__str__())

    def update_frame(self, text):
        pass

    def get_sys_da(self, point, threshold_point):
        pass

    def __str__(self) -> str:
        return "situation-game"
