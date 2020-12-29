from situation.situation_base import SituationBase


class SituationEat(SituationBase):
    """
    食事会話シチュエーションモデル
    """

    def __init__(self) -> None:
        super().__init__(self.__str__())

    def update_sys_da(self, text):
        """テキストからシステム対話行為を推定"""
        # フレーム情報を更新
        self._update_frame(text)
        # テキストからキャラクタパラメータを更新
        self.character.update_point(text)

        # フレーム情報が満タンな状態 → 行動する／しないを答える状態
        # 総合点が閾値を超えた → 行動する
        if self.__is_character_act():
            if not self._is_update_frame():
                # FIXME: act状態でchattingされた場合は、またactする
                if self.sys_da != "act":
                    # 断ったが、chattingで感情値が更新されactになったら
                    # re-actで「やっぱ行くよ」みたいなこと言う
                    self.sys_da = "re-act"
            else:
                self.sys_da = "act"
        # 総合点が閾値を下回った → 行動しない
        else:
            if self._is_fill_frame():
                if not self._is_update_frame():
                    # chattingで感情値が更新されたが、
                    # 行動には至らなかったら「でもごめんね」みたいなこと言う
                    self.sys_da = "re-not-act"
                else:
                    self.sys_da = "not-act"
            else:
                # 足らない属性があれば、それを尋ねる
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
        pass

    def __is_character_act(self):
        return self.character.threshold_point <= self.character.calculate_point()

    def __str__(self) -> str:
        return "situation-eat"
