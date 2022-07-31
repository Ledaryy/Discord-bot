from django import forms

# from .models import Bot
from .models.bots import BotRoles


class BotForm(forms.Form):
    delay = forms.IntegerField(
        min_value=0,
        max_value=600,
        required=False,
        initial=0,
        help_text="Delay for current action in minutes",
    )

    def save(self, bot):
        try:
            self.form_action(bot)
        except Exception as e:
            error_message = str(e)
            self.add_error(None, error_message)
            raise e


class StartBot(BotForm):

    role = forms.ChoiceField(required=True, help_text="Starts diffrent type of the bot", choices=BotRoles.choices)

    field_order = (
        "delay",
        "role",
    )

    def form_action(self, bot):
        print(f"Start bot {bot}")
        if bot.is_active:
            raise Exception("Bot is already active")
        bot.role = self.cleaned_data["role"]
        bot.save()
        return bot.start(delay=self.cleaned_data["delay"])


class StopBot(BotForm):
    def form_action(self, bot):
        if not bot.is_active:
            raise Exception("Bot is already inactive")
        return bot.stop(delay=self.cleaned_data["delay"])


class SendMessage(BotForm):

    message = forms.CharField(max_length=255, required=True, help_text="Bot will send this message to the chat")

    def form_action(self, bot):
        return bot.send_message(
            message=self.cleaned_data["message"],
            delay=self.cleaned_data["delay"],
        )


class MoneyForm(forms.Form):
    amount = forms.IntegerField(
        min_value=1,
        max_value=10000000,
        required=True,
        initial=0,
        help_text="Amount of money",
    )

    def save(self, bot):
        try:
            self.form_action(bot)
        except Exception as e:
            error_message = str(e)
            self.add_error(None, error_message)
            raise e


class SendMoney(MoneyForm):

    receiver = forms.CharField(required=True, help_text="Receiver of the money (raw dicords ID)")

    def form_action(self, bot):
        return bot.balance.transaction(
            value=self.cleaned_data["amount"],
            receiver=self.cleaned_data["receiver"],
            transaction_type="send",
        )


class WithdrawMoney(MoneyForm):
    def form_action(self, bot):
        return bot.balance.transaction(
            value=self.cleaned_data["amount"],
            transaction_type="withdraw",
        )


class DepositMoney(MoneyForm):
    def form_action(self, bot):
        return bot.balance.transaction(
            value=self.cleaned_data["amount"],
            transaction_type="deposit",
        )
