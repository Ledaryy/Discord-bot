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
        'balance',
        'total_earned',
        'role',
        'is_active',
        'bot_actions',
    )
    readonly_fields = (
        'id',
        'total_earned',
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
        ]
        return custom_urls + urls

    def bot_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Start</a>&nbsp;'
            '<a class="button" href="{}">Stop</a>',
            reverse('admin:start-bot', args=[obj.id]),
            reverse('admin:stop-bot', args=[obj.id]),
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
