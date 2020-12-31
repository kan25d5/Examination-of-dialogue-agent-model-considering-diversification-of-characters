from situation.situation_domain_predict import SituationDomainPredict
from character.pM import CharacterPM

UTTS = ["今日飯行かない？", "焼肉とかどう？", "横浜", "じゃあ本厚木で食べよ", "美味しいよ"]
CHARACTER = CharacterPM


def get_situation(first_utt):
    sdp = SituationDomainPredict()
    return sdp.get_situation(first_utt)


def display_character_info(character):
    print("emotion", character.emotion)
    print("interest", character.interest)
    print("intimacy", character.intimacy)
    print("point", character._caculate_point())


def display_situation_info(situation):
    print("user_utt", situation.user_utt)
    print("sys_da", situation.sys_da)
    print("user_da", situation.user_da)
    print("frame", situation.frame)


def main():
    situation = get_situation(UTTS[0])
    character = CharacterPM(situation)

    for utt in UTTS:
        print("reply", character.reply(utt))
        display_situation_info(situation)
        display_character_info(character)
        print("---------------------")


if __name__ == "__main__":
    main()
