from django.contrib import admin
from backend.models import Bot, Balance, MoneyLog, ErrorLog, TaskSchedule

from django.utils.html import format_html
from django.urls import path, reverse

from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from .forms import StartBot, StopBot, SendMessage, MoneyForm

admin.site.register(MoneyLog)
admin.site.register(ErrorLog)
admin.site.register(Balance)
admin.site.register(TaskSchedule)


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    date_heirarchy = (
        'modified',
    )
    list_display = (
        'id',
        'name',
        'role',
        'is_active',
        'bot_actions',
        'display_balance',
        'balance_actions',
        'display_task_schedule',
    )
    readonly_fields = (
        'id',
        'is_active',
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:bot_id>/start/',
                self.admin_site.admin_view(self.start_bot),
                name='start-bot',
            ),
            path(
                '<int:bot_id>/stop/',
                self.admin_site.admin_view(self.stop_bot),
                name='stop-bot',
            ),
            path(
                '<int:bot_id>/send-message/',
                self.admin_site.admin_view(self.send_message),
                name='send-message',
            ),
            path(
                '<int:bot_id>/deposit/',
                self.admin_site.admin_view(self.deposit_balance),
                name='deposit-balance',
            ),
            path(
                '<int:bot_id>/withdraw/',
                self.admin_site.admin_view(self.withdraw_balance),
                name='withdraw-balance',
            ),
            path(
                '<int:bot_id>/transfer/',
                self.admin_site.admin_view(self.transfer_balance),
                name='transfer-balance',
            )
        ]
        return custom_urls + urls

    def display_balance(self, obj):
        if obj.balance:
            return format_html(
                '<textarea style="height: 5em; width: 15em;" readonly>{}</textarea>',
                obj.balance.get_balance_display(),
            )
        else:
            return '-'
    display_balance.short_description = 'Bot Balance'

    def display_task_schedule(self, obj):
        if obj.task_schedule:
            return format_html(
                '<textarea style="height: 5em; width: 15em;" readonly>{}</textarea>',
                obj.task_schedule.get_schedule_display(),
            )
        else:
            return '-'
    display_task_schedule.short_description = 'Tasks Schedule'

    def balance_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Deposit</a>'
            '<br>'
            '<br>'
            '<a class="button" href="{}">Withdraw</a>'
            '<br>'
            '<br>'
            '<a class="button" href="{}">Transfer</a>',
            reverse('admin:deposit-balance', args=[obj.id]),
            reverse('admin:withdraw-balance', args=[obj.id]),
            reverse('admin:transfer-balance', args=[obj.id]),
        )

    balance_actions.short_description = 'Balance Actions'
    balance_actions.allow_tags = True

    def deposit_balance(self, request, bot_id, *args, **kwargs):
        return self.process_action(
            request=request,
            bot_id=bot_id,
            action_title='Deposit',
            action_form=MoneyForm,
        )

    def withdraw_balance(self, request, bot_id, *args, **kwargs):
        return self.process_action(
            request=request,
            bot_id=bot_id,
            action_title='Withdraw',
            action_form=MoneyForm,
        )

    def transfer_balance(self, request, bot_id, *args, **kwargs):
        return self.process_action(
            request=request,
            bot_id=bot_id,
            action_title='Transfer',
            action_form=MoneyForm,
        )

    def bot_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Start</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
            '<a class="button" href="{}">Stop</a>'
            '<br>'
            '<br>'
            '<a class="button" href="{}">Send Message</a>',
            reverse('admin:start-bot', args=[obj.id]),
            reverse('admin:stop-bot', args=[obj.id]),
            reverse('admin:send-message', args=[obj.id]),
        )
    bot_actions.short_description = 'Bot Actions'
    bot_actions.allow_tags = True

    def start_bot(self, request, bot_id, *args, **kwargs):
        return self.process_action(
            request=request,
            bot_id=bot_id,
            action_form=StartBot,
            action_title='Start',
        )

    def stop_bot(self, request, bot_id, *args, **kwargs):
        return self.process_action(
            request=request,
            bot_id=bot_id,
            action_form=StopBot,
            action_title='Stop',
        )

    def send_message(self, request, bot_id, *args, **kwargs):
        return self.process_action(
            request=request,
            bot_id=bot_id,
            action_form=SendMessage,
            action_title='Send Message',
        )

    def process_action(
            self,
            request,
            bot_id,
            action_form,
            action_title
    ):
        bot = self.get_object(request, bot_id)

        if request.method != 'POST':
            form = action_form()
        else:
            form = action_form(request.POST)
            if form.is_valid():
                try:
                    form.save(bot)
                except Exception as e:
                    print(e)
                else:
                    self.message_user(request, 'Success')
                    url = reverse(
                        'admin:backend_bot_changelist',
                        current_app=self.admin_site.name,
                    )
                    return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['bot_id'] = bot.id
        context['title'] = action_title
        return TemplateResponse(
            request,
            'admin/account/bot_action.html',
            context,
        )
