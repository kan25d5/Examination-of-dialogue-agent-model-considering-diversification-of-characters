from helper.helper_functions import load_json

SITUATION_CONCEPTS = "data/situation_concepts.json"


class SituationBase(object):
    """
    会話シチュエーションモデルの基底クラス
    """

    def __init__(self, situation_label: str):
        self.situation_concept = self.__get_situation_concept(situation_label)
        self.sys_da = ""
        self.user_da = ""
        self.user_utt = ""
        self.frame = {}
        self.frame_history = []
        self.init_frame()

    def init_frame(self):
        for key in self.situation_concept.keys():
            self.frame[key] = ""

    def _update_frame(self, text):
        self.user_utt = text
        for key in self.frame.keys():
            for concept in self.situation_concept[key]:
                if concept in text:
                    self.frame[key] = concept
                    self.user_da = "anser-concept"
        self.__add_frame_history(self.frame)
        return self.frame

    def diff_frame(self):
        if len(self.frame_history) < 2:
            return self.frame
        return dict(self.frame_history[-1].items() - self.frame_history[-2].items())

    def check_update_frame(self):
        return {} != self.diff_frame()

    def check_fill_frame(self):
        for key in self.frame.keys():
            if self.frame[key] == "":
                return False
        return True

    def __add_frame_history(self, frame):
        f = {}
        for key, item in frame.items():
            f[key] = item
        self.frame_history.append(f)

    def __get_situation_concept(self, situation_label) -> dict:
        return load_json(SITUATION_CONCEPTS)[situation_label]

