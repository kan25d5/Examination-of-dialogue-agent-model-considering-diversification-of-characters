from helper.helper_functions import load_json


SITUATION_CONCEPTS = "data/situation_concepts.json"


class SituationBase(object):
    """
    会話シチュエーションモデル
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
        for concept_pair in self.situation_concept.items():
            concept_key = concept_pair[0]
            for concept_value in concept_pair[1]:
                if concept_value in text:
                    self.frame[concept_key] = concept_value
