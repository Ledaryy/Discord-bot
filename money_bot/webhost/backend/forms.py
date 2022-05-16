from django import forms

from .models import Bot, Money

class BotForm(forms.Form):
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea,
    )
    send_email = forms.BooleanField(
        required=False,
    )

class StartBot(BotForm):
    amount = forms.IntegerField(
        min_value=0,
        max_value=1000000,
        required=True,
        help_text='How much to withdraw?',
    )
    email_body_template = 'email/account/withdraw.txt'
    field_order = (
        'amount',
        'comment',
        'send_email',
    )
    def form_action(self, account, user):
        # return Account.withdraw(
        #     id=account.pk,
        #     user=account.user,
        #     amount=self.cleaned_data['amount'],
        #     withdrawn_by=user,
        #     comment=self.cleaned_data['comment'],
        #     asof=timezone.now(),
        # )
        return True
    
class StopBot(BotForm):
    amount = forms.IntegerField(
        min_value=0,
        max_value=1000000,
        required=True,
        help_text="How much to deposit?",
    )
    reference_type = forms.ChoiceField(
        required=True,
    )
    reference = forms.CharField(
        required=False,
    )
    email_body_template = 'email/account/deposit.txt'
    field_order = (
        'amount',
        'reference_type',
        'reference',
        'comment',
        'send_email',
    )
    def form_action(self, account, user):
        # return Account.deposit(
        #     id=account.pk,
        #     user=account.user,
        #     amount=self.cleaned_data['amount'],
        #     deposited_by=user,
        #     reference=self.cleaned_data['reference'],
        #     reference_type=self.cleaned_data['reference_type'],
        #     comment=self.cleaned_data['comment'],
        #     asof=timezone.now(),
        # )
        return True