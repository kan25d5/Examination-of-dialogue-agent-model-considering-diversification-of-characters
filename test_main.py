from situation.predict_dialog_act_type import PredictDialogActType
from character.pM import CharacterPM
from character.nM import CharacterNM
from helper.tokenizer import preprocess


def utt_input():
    text = input(":")
    text = preprocess(text)
    return text


utts = ["今日飯行かね？", "ラーメン屋行かない？", "海老名駅前", "美味しいよ"]


def pM():
    pda = PredictDialogActType("situation_predicter", True)

    utt = utts[0]

    situation = pda.get_situation(utt)()
    situation.get_sysda(utt)
    character = CharacterPM(situation)

    print("utt :", utt)
    print("reply :", character.reply(utt))
    print("システム対話行為推定", situation.sys_da)
    print("ユーザ対話行為推定", situation.user_da)
    print("フレーム", situation.frame)
    print("関心度", character.interest)
    print("感情度", character.emotion)
    print("親密度", character.intimacy)
    print("総合点", character.calculate_point())
    print("------------")

    for i in range(1, len(utts), 1):
        utt = utts[i]
        situation.get_sysda(utt)

        print("utt :", utt)
        print("reply :", character.reply(utt))
        print("フレーム", situation.frame)
        print("システム対話行為推定", situation.sys_da)
        print("ユーザ対話行為推定", situation.user_da)
        print("関心度", character.interest)
        print("感情度", character.emotion)
        print("親密度", character.intimacy)
        print("総合点", character.calculate_point())
        print("------------")


def nM():
    pda = PredictDialogActType("situation_predicter", True)

    utt = utts[0]

    situation = pda.get_situation(utt)()
    situation.get_sysda(utt)
    character = CharacterNM(situation)

    print("utt :", utt)
    print("reply :", character.reply(utt))
    print("システム対話行為推定", situation.sys_da)
    print("ユーザ対話行為推定", situation.user_da)
    print("フレーム", situation.frame)
    print("関心度", character.interest)
    print("感情度", character.emotion)
    print("親密度", character.intimacy)
    print("総合点", character.calculate_point())
    print("------------")

    for i in range(1, len(utts), 1):
        utt = utts[i]
        situation.get_sysda(utt)

        print("utt :", utt)
        print("reply :", character.reply(utt))
        print("フレーム", situation.frame)
        print("システム対話行為推定", situation.sys_da)
        print("ユーザ対話行為推定", situation.user_da)
        print("関心度", character.interest)
        print("感情度", character.emotion)
        print("親密度", character.intimacy)
        print("総合点", character.calculate_point())
        print("------------")


if __name__ == "__main__":
    print("外交的男性の会話シチュエーション：")
    pM()
    print()
    print("#################################")
    print()
    print("内向的男性の会話シチュエーション：")
    nM()
