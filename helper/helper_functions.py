import json

from helper.cabocha_helper import Chunk


columns = ["主辞品詞", "係り種別", "書き換え元", "書き換え先"]


def __check_interrogative(chunk: Chunk):
    """
    疑問文かどうか
    """
    text = "".join([m.surface for m in chunk.morphs])
    end_tok = text[-1]

    # 末尾記号が「？」
    if end_tok == "?" or end_tok == "？":
        return True

    # 基本形 + 「か」
    for i in range(len(chunk.morphs)):
        if chunk.morphs[i].inflected_form == "基本形":
            if chunk.morphs[i + 1].surface == "か":
                return True

    return False


def dependency_extract(chunk: Chunk):
    """
    係り種別を返す
    """
    if chunk.dst == -1:
        if __check_interrogative(chunk):
            return "文末（疑問）"
        else:
            return "文末（平叙）"
    else:
        if chunk.dst_chunk.head_pos == "名詞":
            return "連体修飾"
        else:
            return "連用修飾"


def load_json(filepath):
    with open(filepath, "r") as f:
        json_ = json.load(f)
    return json_


def select_character(self, i):
    if i == 0:
        from character.pM import CharacterPM

        return CharacterPM
    elif i == 1:
        from character.pF import CharacterPF

        return CharacterPF
    elif i == 2:
        from character.nM import CharacterNM

        return CharacterNM
    elif i == 3:
        from character.nF import CharacterNF

        return CharacterNF

