import oseti
from helper.cabocha_helper import USER_DIC
from helper.helper_functions import load_json
from situation.situation_base import SituationBase


MAX_DISTANCE = 40000
CHARACTER_PARAM_SET = "data/character_parameter_setting.json"
UTT_PATH = "data/character_utt.json"


class CharacterBase(object):
    """
    キャラクタモデルの基底クラス
    """

    def __init__(self, situation: SituationBase, character_label: str):
        # 派生クラス内で定義するフィールド変数
        self.emotion = 0.0  # 感情度
        self.interest = 0.5  # 関心度
        self.intimacy = 0.0  # 親身度
        self.threshold_point = 0.0  # 行動する／しないの閾値
        self.first_personal_pronoun = ""  # 一人称代名詞
        self.third_personal_pronoun = ""  # 三人称代名詞

        # 基底クラスが保持するフィールド変数
        self.situation = situation
        self.user_utt = ""
        self.sys_utt = ""
        self.character_label = character_label
        self.params_set = load_json(CHARACTER_PARAM_SET)[self.character_label]
        self.utt = load_json(UTT_PATH)[str(self.situation)][self.character_label]

        # 基底クラスが保持するプライベートフィールド変数
        self.__oseti = oseti.Analyzer(USER_DIC)

    def get_sys_da(self, text: str, threshold_point: float) -> str:
        self.situation.update_frame(text)

        if self.situation.check_update_frame():
            self._evaluate_param_by_frame()
        else:
            self._evaluate_param_by_text(text)

        point = self._caculate_point()
        sys_da = self.situation.get_sys_da(point, threshold_point)

        return sys_da

    def _evaluate_param_by_frame(self):
        if len(self.situation.frame_history) < 2:
            # 初回のフレーム更新はすべて属性値の関心度を加算する
            for key, item in self.situation.frame.items():
                if key not in self.params_set.keys():
                    continue
                if item in self.params_set[key]:
                    self.interest += self.params_set[key][item]
        else:
            frame = self.situation.frame
            pre_frame = self.situation.frame_history[-2]

            for key, item in frame.items():
                if frame[key] == "":
                    # 該当属性が空
                    continue
                if pre_frame[key] == frame[key]:
                    # 前回の属性値と変更なし
                    continue
                if pre_frame[key] != frame[key] and pre_frame[key] != "":
                    # 前回の属性値から更新された場合
                    # 前回の属性値の関心度は減算する
                    self.interest -= self.params_set[key][pre_frame[key]]
                self.interest += self.params_set[key][item]

    def _evaluate_param_by_text(self, text):
        self.emotion += sum([o for o in self.__oseti.analyze(text)])

    def _caculate_point(self) -> float:
        return self.interest + self.intimacy + self.emotion

    def _convert_text(self, sys_utt: str) -> str:
        frame = self.situation.frame

        for key in frame.keys():
            sys_utt = sys_utt.replace("__" + key + "__", frame[key])
        sys_utt = sys_utt.replace("__FPP__", self.first_personal_pronoun)
        sys_utt = sys_utt.replace("__TPP__", self.third_personal_pronoun)

        return sys_utt
