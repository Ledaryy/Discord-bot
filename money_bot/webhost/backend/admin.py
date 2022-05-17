from django.contrib import admin
from .models import Bot, MoneyLog

from django.utils.html import format_html
from django.urls import path, reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse

from .forms import StartBot, StopBot

admin.site.register(MoneyLog)

@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    date_heirarchy = (
        'modified',
    )
    list_display = (
        'id',
        'name',
        'token',
        'is_active', 
    )
    # readonly_fields = (
    #     'id',
    #     'name',
    #     'token',
    #     'money',
    #     'is_active', 
    # )
     
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                r'^(?P<account_id>.+)/deposit/$',
                self.admin_site.admin_view(self.process_deposit),
                name='account-deposit',
            ),
            path(
                r'^(?P<account_id>.+)/withdraw/$',
                self.admin_site.admin_view(self.process_withdraw),
                name='account-withdraw',
            ),
        ]
        return custom_urls + urls
    def account_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Deposit</a>&nbsp;'
            '<a class="button" href="{}">Withdraw</a>',
            reverse('admin:account-deposit', args=[obj.pk]),
            reverse('admin:account-withdraw', args=[obj.pk]),
        )
    account_actions.short_description = 'Account Actions'
    account_actions.allow_tags = True
    
    
    def process_deposit(self, request, account_id, *args, **kwargs):
        return self.process_action(
            request=request,
            account_id=account_id,
            action_form=StartBot,
            action_title='Deposit',
        )
    def process_withdraw(self, request, account_id, *args, **kwargs):
            return self.process_action(
                request=request,
                account_id=account_id,
                action_form=StopBot,
                action_title='Withdraw',
            )
        
    def process_action(
            self,
            request,
            account_id,
            action_form,
            action_title
    ):
            account = self.get_object(request, account_id)
            if request.method != 'POST':
                form = action_form()
            else:
                form = action_form(request.POST)
                if form.is_valid():
                    try:
                        form.save(account, request.user)
                    except errors.Error as e:
                        # If save() raised, the form will a have a non
                        # field error containing an informative message.
                        pass
                    else:
                        self.message_user(request, 'Success')
                        url = reverse(
                            'admin:account_account_change',
                        args=[account.pk],
                            current_app=self.admin_site.name,
                        )
                        return HttpResponseRedirect(url)
            context = self.admin_site.each_context(request)
            context['opts'] = self.model._meta
            context['form'] = form
            context['account'] = account
            context['title'] = action_title
            return HttpResponse(
                code = 500
            )