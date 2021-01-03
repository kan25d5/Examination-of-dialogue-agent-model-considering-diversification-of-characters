import re
import csv
import random
import xml.etree.ElementTree as ET
from helper.helper_functions import load_json

SITUATION_CONEPT_PATH = "data/situation_concepts.json"
TRAINING_BASE_PATH = "data/situation_predicter.xml"
TRAINING_PATH = "data/situation_predicter.csv"


class GenerateSamples(object):
    """
    訓練元データを増幅
    """

    def __init__(self):
        self.situation_concepts = load_json(SITUATION_CONEPT_PATH)

    def random_generate(self, root, situation_type):
        if len(root) == 0:
            return root.text

        buf = ""
        situation_concept = self.situation_concepts[situation_type]
        for elem in root:
            for key in situation_concept.keys():
                if elem.tag == key:
                    buf += random.choice(situation_concept[key])
            if elem.tail is not None:
                buf += elem.tail

        return buf

    def generate_samples(self):
        da = ""

        csv_lines = [["dialog_act_type", "utt"]]
        for line in open(TRAINING_BASE_PATH, "r"):
            line = line.rstrip()

            if re.search(r"^da=", line):
                da = line.replace("da=", "")
            elif line == "":
                continue
            else:
                root = ET.fromstring("<dummy>" + line + "</dummy>")
                for _ in range(100):
                    sample = self.random_generate(root, da)
                    csv_lines.append([da, sample])

        with open(TRAINING_PATH, "w", newline="\n") as f:
            w = csv.writer(f, delimiter=",")
            for csv_line in csv_lines:
                w.writerow(csv_line)


if __name__ == "__main__":
    gn = GenerateSamples()
    gn.generate_samples()
