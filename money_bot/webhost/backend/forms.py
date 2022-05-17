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
        bot.bot_type = self.cleaned_data['role']
        bot.save()
        return bot.start(delay=self.cleaned_data['delay'])
    
class StopBot(BotForm):
    
    def form_action(self, bot):
        return bot.stop(delay=self.cleaned_data['delay'])
        