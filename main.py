from situation.situation_domain_predict import SituationDomainPredict
from character.character_base import CharacterBase
from situation.situation_base import SituationBase

from character.pM import CharacterPM

FIRST_UTT = "今日飯行かない？"
UTTS = {
    "ask-number-of-people": "他はいないよ",
    "ask-genre": "ラーメンとかどう？",
    "ask-place": "本厚木でどう？",
}
CHARACTER = CharacterPM


character: CharacterBase
situation: SituationBase


def get_situation(first_utt):
    sdp = SituationDomainPredict()
    return sdp.get_situation(first_utt)


def display_character_info():
    print("user_utt", character.user_utt)
    print("sys_utt", character.sys_utt)
    print("emotion", character.emotion)
    print("interest", character.interest)
    print("intimacy", character.intimacy)
    print("point", character._caculate_point())


def display_situation_info():
    print("sys_da", situation.sys_da)
    print("user_da", situation.user_da)
    print("frame", situation.frame)


def utt_step(f, text):
    character.reply(text)
    display_situation_info()
    display_character_info()
    f.write("User : " + character.user_utt + "\n")
    f.write("System : " + character.sys_utt + "\n")

    print("-------------------------")


def main():
    global character
    global situation

    first_utt = FIRST_UTT
    situation = get_situation(first_utt)
    character = CharacterPM(situation)
    f = open(str(character), "w")

    utt_step(f, first_utt)
    while situation.sys_da.startswith("ask"):
        text = UTTS[situation.sys_da]
        utt_step(f, text)

    f.close()


if __name__ == "__main__":
    main()
