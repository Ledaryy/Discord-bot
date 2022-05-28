
import re


class Extractor():

    def extract_money_value(self, message):
        line = message["embeds"][0]["description"]

        if "You cannot" in line:
            return None

        numbers = re.findall(r'\d+', f"{line}")
        return int(numbers[1])
