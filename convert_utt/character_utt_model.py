import pandas as pd
from CaboCha import Chunk
from helper.cabocha_helper import CaboChaHelper
from helper.helper_functions import dependency_extract


CH = CaboChaHelper()


class CharacterUttModel(object):
    """
    docstring
    """

    def __init__(self, df_rule: pd.DataFrame):
        """
        df_rule : キャラクターの書き換えルール
        """
        self.df_rule = df_rule
        self.df_prefix_rule = df_rule[df_rule["係り種別"] == "接頭辞"]
        self.df_suffix_rule = df_rule[df_rule["係り種別"] == "接尾"]

    def __convert_suffix_expression(self, tok):
        """
        接尾辞表現を付与する
        """
        df_suffix = self.df_suffix_rule[self.df_suffix_rule["書き換え元"] == tok.surface]
        if len(df_suffix) <= 0:
            return ""
        else:
            return df_suffix["書き換え先"].iloc[0]

    def __convert_prefix_expression(self, tok):
        """
        接頭辞表現を付与する
        """
        df_prefix = self.df_prefix_rule[self.df_prefix_rule["書き換え元"] == tok.surface]
        if len(df_prefix) <= 0:
            return ""
        else:
            return df_prefix["書き換え先"].iloc[0]

    def __convert_expression(self, df_rule: pd.DataFrame, chunk: Chunk) -> str:
        """
        機能語表現の変換
        """
        text = ""

        for tok in chunk.morphs:
            tok_surface = tok.surface
            convert_df_rule = df_rule[df_rule["書き換え元"] == tok_surface]

            if len(convert_df_rule) > 0:
                convert_sr_s = convert_df_rule["書き換え元"].iloc[0]
                convert_sr_c = convert_df_rule["書き換え先"].iloc[0]

                if convert_sr_s == tok_surface:
                    tok_surface = convert_sr_c

            tok_surface = self.__convert_prefix_expression(tok) + tok_surface
            tok_surface = tok_surface + self.__convert_suffix_expression(tok)

            text += tok_surface

        return text

    def convert_text(self, text) -> str:
        """
        テキストを受け取ったルールに則り変換
        """
        tree = CH.parse(text)
        converted_text = ""

        for chunk in tree:
            head_pos = chunk.head_pos
            dp = dependency_extract(chunk)

            convert_df_rule = self.df_rule[self.df_rule["主辞品詞"] == head_pos]
            convert_df_rule = convert_df_rule[convert_df_rule["係り種別"] == dp]
            if len(convert_df_rule) > 0:
                converted_text += self.__convert_expression(convert_df_rule, chunk)
            else:
                converted_text += chunk.surface().replace(" ", "")

        return converted_text
