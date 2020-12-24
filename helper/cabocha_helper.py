import re
import CaboCha


USER_DIC = "-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/"


class Morph(object):
    """
    形態素情報を保持するクラス
    ==========
    Parameters
    ----------
    lattice_line : str
        形態素情報行
    Attributes
    ----------
    surface : str
        表層形
    pos : str
        品詞
    pos_detail1 : str
        品詞詳細分類
    pos_detail2 : str
        品詞詳細分類2
    pos_detail3 : str
        品詞詳細分類3
    utilization_type : str
        活用型
    inflected_form : str
        活用形
    original : str
        原形
    """

    def __init__(self, lattice_line: str):
        self.parce_lattice(lattice_line)

    def parce_lattice(self, lattice_line):
        vs = lattice_line.split("\t")
        vs2 = vs[1].split(",")
        self.surface = vs[0]
        self.pos = vs2[0]
        self.pos_detail1 = vs2[1]
        self.pos_detail2 = vs2[2]
        self.pos_detail3 = vs2[3]
        self.utilization_type = vs2[4]
        self.inflected_form = vs2[5]
        self.original = vs2[6]

    def __str__(self):
        return "{} : {},{},{}".format(
            self.surface, self.pos, self.pos_detail1, self.original
        )


class Chunk(object):
    """
    文節情報を保持するクラス
    ==========
    Parameters
    ----------
    lattice_line : str
        文節情報行
    Attributes
    ----------
    morphs : [Morph]
        形態素リスト（初期状態：[None]）
    idx : int
        文節番号
    dst : int
        係り受け番号
    dts_chunk : Chunk
        係り受け先のChunk要素（初期状態：None）
    head : int
        主辞形態素の係り受け番号
    func : int
        機能語形態素の係り受け番号
    """

    def __init__(self, lattice_line: str):
        self.__re_src = re.compile(r"[-]?\d")
        self.parce_lattice(lattice_line)
        self.morphs = []
        self.dst_chunk = None
        self.head_pos = None

    def parce_lattice(self, lattice_line):
        vs = lattice_line.split(" ")
        self.idx = int(vs[1])
        self.dst = int(self.__re_src.match(vs[2]).group(0))
        self.head = int(vs[3].split("/")[0])
        self.func = int(vs[3].split("/")[1])

    def add_morph(self, morph: Morph):
        self.morphs.append(morph)

    def add_morphs(self, morphs: Morph):
        self.morphs = morphs

    def surface(self) -> str:
        return " ".join([m.surface for m in self.morphs])

    def __str__(self):
        return "{}:{}, dst:{}, {}/{}".format(
            self.idx, self.surface(), self.dst, self.head, self.func
        )


class CaboChaHelper(object):
    """
    CaboChaヘルパークラス
    """

    def __init__(self):
        self.c = CaboCha.Parser(USER_DIC)
        self.tree = None

    def format_lattice(self, sentence: str) -> str:
        """
        文節区切りレイヤ構造を持つ出力フォーマットを返す
        """
        self.tree = self.c.parse(sentence)
        return self.tree.toString(CaboCha.FORMAT_LATTICE)

    def parse(self, sentence: str) -> [Chunk]:
        """
        文節情報をパースして文節番号をキーとした辞書型に変換
        """
        idx = 0
        chunks = []
        toks = []

        lattice = self.format_lattice(sentence)
        lines = lattice.split("\n")

        # 文節情報
        for line in lines:
            if line.startswith("*"):
                if len(chunks) > 0:
                    chunks[idx].add_morphs(toks)
                    toks = []
                    idx += 1
                chunks.append(Chunk(line))
            elif line.startswith("EOS"):
                chunks[idx].add_morphs(toks)
                break
            else:
                toks.append(Morph(line))

        # 係り受け先の文節情報を追加
        for chunk in chunks:
            chunk.head_pos = chunk.morphs[chunk.head].pos
            if chunk.dst == -1:
                continue
            chunk.dst_chunk = chunks[chunk.dst]

        return chunks


if __name__ == "__main__":
    text = "駅の傍に美味しい寿司屋があります。"
    cabocha_helper = CaboChaHelper()
    for item in cabocha_helper.parse(text):
        if item.dst == -1:
            break
        print(item.surface(), "->", item.dst_chunk.surface())
        print(item.head_pos, "->", item.dst_chunk.head_pos)
        print()