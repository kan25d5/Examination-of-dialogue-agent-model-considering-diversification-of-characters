import pandas as pd
from situation.situation_base import SituationBase
from numpy import sqrt

MAX_DISTANCE = 40000
STATION_FILE_PATH = "data/stations-simplify.csv"


class SituationEat(SituationBase):
    """
    食事会話シチュエーションモデル
    """

    def __init__(self) -> None:
        self.__sation_df = pd.read_csv(STATION_FILE_PATH)
        super().__init__(self.__str__())

    def update_sys_da(self, text):
        """テキストからシステム対話行為を推定"""
        # フレーム情報を更新
        self._update_frame(text)
        # テキストからキャラクタパラメータを更新
        self.character.update_point(text)

        # フレーム情報が満タンな状態 → 行動する／しないを答える状態
        if self._is_fill_frame():
            # 総合点が閾値を超えた → 行動する
            if self.__is_character_act():
                if not self._is_update_frame():
                    self.sys_da = "re-act"
                else:
                    self.sys_da = "act"
            # 総合点が閾値を下回った → 行動しない
            else:
                if not self._is_update_frame():
                    self.sys_da = "re-not-act"
                else:
                    self.sys_da = "not-act"
        else:
            if self.frame["date"] == "":
                self.sys_da = "ask-date"
            elif self.frame["genre"] == "":
                self.sys_da = "ask-genre"
            elif self.frame["place"] == "":
                self.sys_da = "ask-place"

        return self.sys_da

    def update_user_da(self):
        """フレーム情報からユーザー対話行為を推定"""
        if self.sys_da.startswith("ask-"):
            return self.user_da
        else:
            self.user_da = "chatting"
            return self.user_da

    def update_parameter_by_frame(self):
        """フレーム情報から感情度を算出"""
        if self.user_da == "anser-place":
            self.__update_emotion_by_distance(self.frame["place"])

    def __is_character_act(self):
        return self.character.threshold_point <= self.character.calculate_point()

    def __get_distance(self, dest):
        """神奈川工科大学から場所までの距離を算出"""
        ox, oy = -44662, -56845
        dx, dy = (
            self.__sation_df[self.__sation_df.station == dest].iloc[0, :].values[1:3]
        )
        return int(round(sqrt((ox - dx) ** 2 + (oy - dy) ** 2)))

    def __update_emotion_by_distance(self, place):
        """近いとの距離から感情度を加算"""
        # ２駅間の距離を算出
        distance = self.__get_distance(place)
        # 距離をMAX_DISTANCE以上にしない
        distance = distance if distance < MAX_DISTANCE else MAX_DISTANCE
        # [0,1]で正規化
        emotion = distance / MAX_DISTANCE

        self.character.emotion -= emotion

    def __str__(self) -> str:
        return "situation-eat"
