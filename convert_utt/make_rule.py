import pandas as pd
from CaboCha import Token, Chunk
from helper.cabocha_helper import CaboChaHelper
from helper.helper_functions import columns, dependency_extract


CH = CaboChaHelper()


class MakeRule(object):
    """
    １文から書き換えルールを抽出する
    """

    def __init__(self) -> None:
        self.is_prefix = False
        self.df_rule = pd.DataFrame(columns=columns)
        self.sr_rule = pd.Series(index=columns)

    def __extract_expression_suffix(self, tok: Token, pre_tok: Token) -> None:
        """
        接尾要素を登録する
        """
        self.sr_rule["係り種別"] = "接尾"
        self.sr_rule["主辞品詞"] = ""
        self.sr_rule["書き換え元"] = pre_tok.surface
        self.sr_rule["書き換え先"] = tok.surface
        self.df_rule = self.df_rule.append(self.sr_rule, ignore_index=True)

    def __extract_expression_prefix(self, tok: Token, next_tok: Token) -> None:
        """
        接頭辞要素を登録する
        """
        self.sr_rule["係り種別"] = "接頭辞"
        self.sr_rule["主辞品詞"] = ""
        self.sr_rule["書き換え元"] = next_tok.surface
        self.sr_rule["書き換え先"] = tok.surface
        self.df_rule = self.df_rule.append(self.sr_rule, ignore_index=True)

    def __extract_expression(self, chunk0: Chunk, chunk1: Chunk) -> None:
        """
        機能語表現を抽出する
        """
        self.is_prefix = False
        i, j = 0, 0

        while i < len(chunk0.morphs) - 1 or j < len(chunk1.morphs) - 1:
            tok0 = chunk0.morphs[i]
            tok1 = chunk1.morphs[j]

            # 表層形が同一ならスキップ
            if tok0.surface == tok1.surface:
                i += 1
                j += 1
                continue

            # 文節内の形態素数がズレるため
            # 接頭詞もしくはが発見されたら、接頭詞・接尾以外は登録しない
            if tok1.pos == "接頭詞":
                self.__extract_expression_prefix(tok1, chunk1.morphs[j + 1])
                j += 1
                continue

            if tok1.pos_detail1 == "接尾":
                self.__extract_expression_suffix(tok1, chunk1.morphs[j - 1])
                j += 1
                continue

            # 書き換え元／先をそのまま保持する
            self.sr_rule["書き換え元"] = tok0.surface
            self.sr_rule["書き換え先"] = tok1.surface
            self.df_rule = self.df_rule.append(self.sr_rule, ignore_index=True)
            i += 1
            j += 1

    def extract_rule(self, text0, text1) -> pd.DataFrame:
        """
        ルールを抽出する
        """
        tree0 = CH.parse(text0)
        tree1 = CH.parse(text1)

        i, j = 0, 0

        while i < len(tree0) - 1 or j < len(tree1):
            chunk0 = tree0[i]
            chunk1 = tree1[j]

            # 表層形比較
            if chunk0.surface() == chunk1.surface():
                i, j = i + 1, j + 1
                continue

            # 主辞品詞
            if chunk0.head_pos != chunk1.head_pos:
                i, j = i + 1, j + 1
                continue
            self.sr_rule["主辞品詞"] = chunk0.head_pos

            # 係り種別
            chunk0_dp = dependency_extract(chunk0)
            chunk1_dp = dependency_extract(chunk1)
            if chunk0_dp != chunk1_dp:
                i, j = i + 1, j + 1
                continue

            self.sr_rule["係り種別"] = chunk0_dp
            self.__extract_expression(chunk0, chunk1)

            i, j = i + 1, j + 1

        return self.df_rule
