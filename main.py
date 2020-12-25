from situation.predict_dialog_act_type import PredictDialogActType
from character.pM import CharacterPM
from helper.tokenizer import preprocess


def utt_input():
    text = input(":")
    text = preprocess(text)
    return text


def main():
    pda = PredictDialogActType("situation_predicter", True)

    user_utt = "今日本厚木でご飯行きませんか？"

    situation = pda.get_situation(user_utt)()
    situation.get_sysda(user_utt)

    character = CharacterPM(situation)
    character.reply(user_utt)
    print("関心度", character.interest)
    print("感情度", character.emotion)
    print("親密度", character.intimacy)
    print("------------")

    user_utt = "牛丼とかどう？"
    situation.get_sysda(user_utt)

    character.reply(user_utt)
    print("関心度", character.interest)
    print("感情度", character.emotion)
    print("親密度", character.intimacy)
    print("------------")

    user_utt = "凄い美味しいよ"
    situation.get_sysda(user_utt)

    character.reply(user_utt)
    print("関心度", character.interest)
    print("感情度", character.emotion)
    print("親密度", character.intimacy)


if __name__ == "__main__":
    main()
