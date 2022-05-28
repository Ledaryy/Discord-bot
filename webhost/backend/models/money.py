from django.db import models


class Balance(models.Model):
    
    bot = models.OneToOneField(
        "Bot",
        related_name="balance",
        on_delete=models.CASCADE,
    )

    pocket_balance = models.IntegerField(default=0)
    bank_balance = models.IntegerField(default=0)

    work_earned = models.IntegerField(default=0)
    collect_earned = models.IntegerField(default=0)

    crime_earned = models.IntegerField(default=0)
    crime_loss = models.IntegerField(default=0)

    @property
    def total_balance(self):
        return self.pocket_balance + self.bank_balance
    
    @property
    def total_earned(self):
        return self.work_earned + self.collect_earned + self.crime_earned

    def get_balance_display(self):
        return f"Pocket: {self.pocket_balance}  \nBank: {self.bank_balance}  \nTotal: {self.total_balance} \nTotal Earned: {self.total_earned}"

    def __str__(self):
        return f"{self.bot} | P: {self.pocket_balance}  |  B: {self.bank_balance}  |  T: {self.total_balance}"


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
        return f"{self.owner} - {self.date} - {self.earned} - {self.comment}"

    def save_work(owner, earned):
        
        log = MoneyLog(
            owner=owner,
            value=earned,
            comment="Earned by using [work] command"
        )
        
        log.save()
        
        balance = log.owner.balance
        balance.pocket_balance += earned
        balance.work_earned += earned
        
        balance.save()
        
    def save_crime(owner, sucess, value):
        
        balance = log.owner.balance
        
        if sucess:
            log = MoneyLog(
                owner=owner,
                value=value,
                comment="Earned by using [crime] command"
            )
            balance.pocket_balance += value
            balance.crime_earned += value
        else:
            log = MoneyLog(
                owner=owner,
                value=value,
                comment="Loss by using [crime] command"
            )
            balance.pocket_balance -= value
            balance.crime_loss += value
            
        log.save()
        balance.save()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
