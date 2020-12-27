import copy
from helper.helper_functions import load_json
from character.character_base import CharacterBase

SITUATION_CONCEPTS = "data/situation_concepts.json"


class SituationBase(object):
    """
    会話シチュエーションモデルの基底クラス
    """

    def __init__(self, situation_str: str) -> None:
        self.situation_str = situation_str
        self.sys_da = ""
        self.user_da = ""
        self.frame = {}
        self.pre_frame = {}
        self.chatting_flag = False
        self.character = None
        self.situation_concept = self.__get_situation_concept()
        self._init_frame()

    def set_character(self, character: CharacterBase):
        self.character = character

    def _init_frame(self):
        for key in self.situation_concept.keys():
            self.frame[key] = ""

    def _update_frame(self, text):
        self.pre_frame = copy.deepcopy(self.frame)

        for key in self.situation_concept.keys():
            for concept in self.situation_concept[key]:
                if concept in text:
                    self.frame[key] = concept
                    self.user_da = "anser-" + key
        return self.user_da

    def _is_update_frame(self):
        return self.pre_frame != self.frame

    def _is_fill_frame(self):
        for key in self.frame.keys():
            if self.frame[key] == "":
                return False
        return True

    def _is_init_frame(self):
        for key in self.frame.keys():
            if self.frame[key] != "":
                return False
        return True

    def __get_situation_concept(self) -> dict:
        return load_json(SITUATION_CONCEPTS)[self.situation_str]

