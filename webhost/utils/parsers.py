import re


class Extractor():

    def extract_work_money_value(self, message):
        line = message["embeds"][0]["description"]

        if "You cannot" in line:
            return None

        numbers = re.findall(r'\d+', f"{line}")
        return int(numbers[1])

    def extract_crime_money_value(self, message):
        line = message["embeds"][0]["description"]
        color_code = message["embeds"][0]["color"]

        numbers = re.findall(r'\d+', f"{line}")
        money_value = int(numbers[1])

        if color_code == 6732650:  # green
            success = True
        elif color_code == 15684432:  # red
            success = False
        else:
            raise Exception("Unknown color code")
        return success, money_value

    def extract_collect_money_value(self, message):
        fields = message["embeds"][0]["fields"]

        cash = fields[0]["value"]
        numbers_cash = re.findall(r'\d+', f"{cash}")
        clear_number_cash = numbers_cash[1:]
        cash_values = int("".join(clear_number_cash))

        bank = fields[1]["value"]
        numbers_bank = re.findall(r'\d+', f"{bank}")
        clear_number_bank = numbers_bank[1:]
        bank_values = int("".join(clear_number_bank))

        return cash_values, bank_values
