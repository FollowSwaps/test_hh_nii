import datetime

from django.db import models

# Create your models here.
class KBKStatus(models.TextChoices):
   ACTIVE              = "ACTIVE", 'Актуальная запись'
   ARCHIVE             = "ARCHIVE", 'Архивная запись'


class BudgetType(models.TextChoices):
   """Код типа бюджета"""
   OTHER = "00", 'Прочие бюджеты'
   FEDERAL = "01", 'Федеральный бюджет'
   SUBJECT = "02", 'Бюджет субъекта РФ'
   CAPITALS = "03", 'Бюджеты внутригородских МО г. Москвы и г. Санкт-Петербурга'
   CITY = "04", 'Бюджет городского округа'
   MUNICIPAL = "05", 'Бюджет муниципального района'
   PENSION = "06", 'Бюджет Пенсионного фонда РФ'
   FSS = "07", 'Бюджет ФСС РФ'
   FFOMS = "08", 'Бюджет ФФОМС'
   TFOMS = "09", 'Бюджет ТФОМС'
   LOCAL = "10", 'Бюджет поселения'
   #Есть 13 код в документации не описан, возможно есть и другие
   DISTRIBUTED = "98", 'Распределяемый доход'
   ORGANIZATION = "99", 'Доход организации (только для ПДИ)'

   __empty__ = '(Unknown)'

# исправил code на пк, либо это как минимум должно быть уникальным полем
# потому что у нас идет ссылка в parentcode на себя, то есть на пк
# тут либо я не понял чего то, либо действительно что то не так
class Budget(models.Model):
   # guid                = models.CharField("Глобально-уникальный идентификатор записи", max_length=36)  # ! Не берем при импорте
   code                = models.CharField("Код", max_length=8, blank=False, null=False,primary_key=True)
   name                = models.TextField("Полное наименование", max_length=2000, blank=False, null=False)
   parentcode          = models.ForeignKey('self', verbose_name="Вышестоящий бюджет", blank=True, null=True, on_delete=models.SET_NULL)
   startdate           = models.DateTimeField("Дата начала действия записи", blank=False, null=False, default=datetime.datetime.now)
   enddate             = models.DateTimeField("Дата окончания действия записи", blank=True, null=True)
   status              = models.CharField("Статус записи", max_length=7, choices=KBKStatus.choices, blank=False, null=False, default=KBKStatus.ACTIVE)
   budgettype          = models.CharField("Тип бюджета", max_length=2, choices=BudgetType.choices, blank=False, null=False, default=BudgetType.OTHER)

   class Meta:
       verbose_name    = 'Справочник бюджетов'
       verbose_name_plural = 'Справочники бюджетов'

   def __str__(self):
       return f"{self.code}: {self.name}"

class GlavBudget(models.Model):
   """Справочник главы по бюджетной классификации."""

   # guid                = models.CharField("Глобально-уникальный идентификатор записи", max_length=36)
   code                = models.CharField("Код",max_length=3, blank=False, null=False)  # ! если не будут пересекаться добавить: , unique=True
   name                = models.TextField("Сокращенное наименование", max_length=254, blank=True, null=True)
   startdate           = models.DateTimeField("Дата начала действия записи", blank=False, null=False, default=datetime.datetime.now,)
   enddate             = models.DateTimeField("Дата окончания действия записи", null=True)
   budget              = models.ForeignKey(Budget, verbose_name="Бюджет", blank=False, null=False, on_delete=models.CASCADE)
   # tofkcode
   # ppocode
   #dateinclusion       = models.DateTimeField("Дата включения кода", blank=False, null=False, default=datetime.datetime.now)
   #dateexclusion       = models.DateTimeField("Дата исключения кода")
   # year                = models.DateField("Год")

   class Meta:
       verbose_name = 'Справочник главы по бюджетной классификации'
       verbose_name_plural = 'Справочники главы по бюджетной классификации'

   def __str__(self):
       return f"{self.code}: {self.name}"
