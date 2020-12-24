import re
import csv
import random
import xml.etree.ElementTree as ET
from helper.helper_functions import load_json


SITUATION_CONEPT_PATH = "data/situation_concepts.json"


class GenerateSamples(object):
    """
    docstring
    """

    def __init__(self, base_training_path, training_path, situation_concepts):
        self.training_path = training_path
        self.base_training_path = base_training_path
        self.situation_concepts = situation_concepts

    def random_generate(self, root):
        if len(root) == 0:
            return root.text

        buf = ""
        for elem in root:
            for key in self.situation_concepts.keys():
                if elem.tag == key:
                    buf += random.choice(self.situation_concepts[key])
            if elem.tail is not None:
                buf += elem.tail

        return buf

    def generate_samples(self):
        da = ""

        csv_lines = [["dialog_act_type", "utt"]]
        for line in open(self.base_training_path, "r"):
            line = line.rstrip()

            if re.search(r"^da=", line):
                da = line.replace("da=", "")
            elif line == "":
                continue
            else:
                root = ET.fromstring("<dummy>" + line + "</dummy>")
                for _ in range(100):
                    sample = self.random_generate(root)
                    csv_lines.append([da, sample])

        with open(self.training_path, "w", newline="\n") as f:
            w = csv.writer(f, delimiter=",")
            for csv_line in csv_lines:
                w.writerow(csv_line)
