from logging import raiseExceptions
from django import forms

from .models import Bot
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
            raise
        # if self.cleaned_data.get('send_email', False):
        #     send_email(
        #         to=[account.user.email],
        #         subject_template=self.email_subject_template,
        #         body_template=self.email_body_template,
        #         context={
        #             "account": account,
        #             "action": action,
        #         }
        #     )
        # return account, action


class StartBot(BotForm):

    role = forms.ChoiceField(
        required=True,
        help_text="Starts diffrent type of the bot",
        choices=BotRoles.choices
    )

    field_order = (
        'delay',
        'role',
    )

    def form_action(self, bot):
        print(f"Start bot {bot}")
        if bot.is_active:
            raise Exception("Bot is already active")
        bot.role = self.cleaned_data['role']
        bot.save()
        return bot.start(delay=self.cleaned_data['delay'])


class StopBot(BotForm):

    def form_action(self, bot):
        if not bot.is_active:
            raise Exception('Bot is already inactive')
        return bot.stop(delay=self.cleaned_data['delay'])


class SendMessage(BotForm):

    message = forms.CharField(
        max_length=255,
        required=True,
        help_text="Bot will send this message to the chat"
    )

    def form_action(self, bot):
        return bot.send_message(
            message=self.cleaned_data['message'],
            delay=self.cleaned_data['delay'],
        )


class MoneyForm(forms.Form):
    amount = forms.IntegerField(
        min_value=0,
        max_value=100000,
        required=True,
        initial=0,
        help_text="This is just a template",
    )

    def save(self, bot):
        print("Save money")
        # return bot.add_money(self.cleaned_data['amount'])
