from _io import TextIOWrapper
from situation.situation_domain_predict import SituationDomainPredict
from character.character_base import CharacterBase
from situation.situation_base import SituationBase

from character.pM import CharacterPM
from character.pF import CharacterPF
from character.nM import CharacterNM
from character.nF import CharacterNF

FIRST_UTT = "今日の夜ご飯いかない？"
UTTS = {
    "situation-game": {
        "ask-number-of-people": "6人くらいでやるゲームだよ",
        "ask-genre": "人狼ゲームだよ",
        "ask-type": "人狼を見つけるゲームだよ",
    },
    "situation-eat": {
        "ask-genre": "横浜においしいラーメン屋があるんだ",
        "ask-place": "本厚木",
        "ask-date": "今日",
    },
}

character: CharacterBase
situation: SituationBase
f_file: TextIOWrapper


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


def utt_step(text):
    character.reply(text)
    display_situation_info()
    display_character_info()
    f_file.write("User : " + character.user_utt + "\n")
    f_file.write("System : " + character.sys_utt + "\n")

    print("-------------------------")


def make_dialog():
    global character
    global situation
    global f_file

    first_utt = FIRST_UTT
    situation = get_situation(first_utt)
    character = character(situation)
    filepath = "logs/" + str(situation)
    f_file = open(filepath, "a")
    f_file.write("character : " + str(character) + "\n")

    utt_step(first_utt)
    utts = UTTS[str(situation)]
    while situation.sys_da.startswith("ask"):
        text = utts[situation.sys_da]
        utt_step(text)


def main():
    global character

    character = CharacterNF
    make_dialog()

    f_file.write("\n")
    f_file.write("\n")
    f_file.close()

    character = CharacterNM
    make_dialog()

    f_file.write("\n")
    f_file.write("\n")
    f_file.close()

    character = CharacterPF
    make_dialog()

    f_file.write("\n")
    f_file.write("\n")
    f_file.close()

    character = CharacterPM
    make_dialog()

    f_file.write("\n")
    f_file.write("\n")
    f_file.close()


if __name__ == "__main__":
    main()
