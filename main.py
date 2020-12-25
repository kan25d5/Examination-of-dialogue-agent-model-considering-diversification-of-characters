from situation.predict_dialog_act_type import PredictDialogActType
from helper.tokenizer import preprocess


def utt_input():
    text = input(":")
    text = preprocess(text)
    return text


def main():
    pda = PredictDialogActType("situation_predicter", True)

    user_utt = utt_input()
    situation = pda.get_situation(user_utt)()

    print(situation.get_sysda(user_utt))


if __name__ == "__main__":
    main()
