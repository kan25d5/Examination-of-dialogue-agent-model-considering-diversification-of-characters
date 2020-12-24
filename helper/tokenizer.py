import MeCab
import unicodedata
import neologdn


USER_DIC = ""
tagger = MeCab.Tagger()


def preprocess(text):
    text = text.strip()
    text = unicodedata.normalize("NFKC", text)
    text = neologdn.normalize(text)

    return text


def tokenizer(text):
    text = preprocess(text)

    words = []
    node = tagger.parseToNode(text)
    while node:
        surface = node.surface
        # features = node.feature.split(",")

        # 品詞制限など
        # 規則があれば記述する

        words.append(surface)
        node = node.next

    return words
