import celery
from django.db import models


class Balance(models.Model):

    bot = models.OneToOneField(
        "Bot",
        related_name="balance",
        on_delete=models.CASCADE,
    )

    cash_balance = models.IntegerField(default=0)
    bank_balance = models.IntegerField(default=0)

    work_earned = models.IntegerField(default=0)
    text_earned = models.IntegerField(default=0)
    collect_earned = models.IntegerField(default=0)

    crime_earned = models.IntegerField(default=0)
    crime_loss = models.IntegerField(default=0)

    initialized = models.BooleanField(default=False)

    @property
    def total_balance(self):
        return self.cash_balance + self.bank_balance

    @property
    def total_earned(self):
        return self.work_earned + self.collect_earned + self.crime_earned - self.crime_loss + self.text_earned

    def get_balance_display(self):
        return f"Cash: {self.cash_balance}  \nBank: {self.bank_balance}  \nTotal: {self.total_balance} \nTotal Earned: {self.total_earned}"

    def __str__(self):
        return f"{self.bot} | C: {self.cash_balance}  |  B: {self.bank_balance}  |  T: {self.total_balance}"

    def transaction(self, value, transaction_type, receiver=None):
        # Sends money to the another account
        if transaction_type == "send":
            if self.total_balance < value:
                raise Exception("Not enough money")
            if self.cash_balance < value:
                self.withdraw(value - self.cash_balance)
            self.send(value, receiver)

        if transaction_type == "withdraw":
            if self.bank_balance < value:
                raise Exception("Not enough money in bank")
            self.withdraw(value)

        if transaction_type == "deposit":
            if self.cash_balance < value:
                raise Exception("Not enough money in cash")
            self.deposit(value)

    def withdraw(self, value):
        # Withdraws money from the bank account
        celery.current_app.send_task(
            "backend.tasks.transaction", args=(
                self.bot.id,
                value,
                "withdraw"
            )
        )

        self.cash_balance += value
        self.bank_balance -= value
        self.save()

    def deposit(self, value):
        # Deposits money to the bank account
        celery.current_app.send_task(
            "backend.tasks.transaction", args=(
                self.bot.id,
                value,
                "deposit"
            )
        )

        self.cash_balance -= value
        self.bank_balance += value
        self.save()

    def send(self, value, receiver):
        # Sends money to another account
        celery.current_app.send_task(
            "backend.tasks.transaction", args=(
                self.bot.id,
                value,
                "send",
                receiver
            )
        )

        self.cash_balance -= value
        self.save()


class MoneyLog(models.Model):

    owner = models.ForeignKey(
        "Bot",
        related_name="money_log",
        on_delete=models.CASCADE
    )
    value = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.owner} - {self.date} - {self.value} - {self.comment}"

    def save_work(owner, earned):

        log = MoneyLog(
            owner=owner,
            value=earned,
            comment="Earned by using [work] command"
        )

        log.save()

        balance = log.owner.balance
        balance.cash_balance += earned
        balance.work_earned += earned

        balance.save()

    def save_crime(owner, sucess, value):

        balance = owner.balance
        if sucess:
            log = MoneyLog(
                owner=owner,
                value=value,
                comment="Earned by using [crime] command"
            )
            balance.cash_balance += value
            balance.crime_earned += value
        else:
            log = MoneyLog(
                owner=owner,
                value=value,
                comment="Loss by using [crime] command"
            )
            balance.cash_balance -= value
            balance.crime_loss += value

        log.save()
        balance.save()

    def save_collect(owner, cash, bank):

        balance = owner.balance

        if balance.initialized:
            if cash != balance.cash_balance:
                earned = balance.cash_balance - cash
                log = MoneyLog(
                    owner=owner,
                    value=earned,
                    comment="Earned by texting in chat"
                )
                log.save()
                balance.cash_balance = cash
                balance.text_earned += earned
                balance.save()

            if bank != balance.bank_balance:
                earned = balance.bank_balance - bank
                log = MoneyLog(
                    owner=owner,
                    value=earned,
                    comment="Earned by collecting daily"
                )
                log.save()
                balance.bank_balance = bank
                balance.collect_earned += earned
                balance.save()

        else:
            balance.cash_balance = cash
            balance.bank_balance = bank
            balance.initialized = True
            balance.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
