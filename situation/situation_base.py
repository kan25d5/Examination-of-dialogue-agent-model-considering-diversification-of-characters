from helper.helper_functions import load_json


SITUATION_CONCEPTS = "data/situation_concepts.json"


class SituationBase(object):
    """
    会話シチュエーションモデル
    ------
    sys_da : str
        システム対話行為タイプ
    user_da : ste
        ユーザ対話行為タイプ
    frame : dict
        フレーム情報
    """

    def __init__(self, situation: str) -> None:
        self.situation = situation
        self.sys_da = "None"
        self.user_da = "None"
        self.frame = {}
        self.situation_concept = self.__get_situation_concept()
        self._init_frame()

    def __get_situation_concept(self) -> dict:
        return load_json(SITUATION_CONCEPTS)[self.situation]

    def _init_frame(self):
        for key in self.situation_concept.keys():
            self.frame[key] = ""

    def _update_frame(self, text):
        if (
            self.frame["date"] != ""
            and self.frame["place"] != ""
            and self.frame["genre"] != ""
        ):
            self.user_da = "chatting"
            return

        for concept_pair in self.situation_concept.items():
            concept_key = concept_pair[0]
            for concept_value in concept_pair[1]:
                if concept_value in text:
                    self.user_da = "anser-" + concept_key
                    self.frame[concept_key] = concept_value
