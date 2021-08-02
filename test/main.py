import os

os.environ['DJANGO_SETTINGS_MODULE'] = "test_hh_nii.settings"
import django

django.setup()

from test.models import Budget,GlavBudget
from test.serializers import get_ser

def preprocs_data(data:dict):
    ''' заменим пустые строчки на ноне '''
    for k,v in data.items():
        if v=='':
            data[k]=None
    return data

if __name__=='__main__':
    # входная модель
    input_model=Budget
    # входные данные для теста
    test_data={"guid":"ED50707B-21A4-43C3-B91D-FDF40BA305DA","status":"ACTIVE","code":"01021251","name":"Бюджет123 Республики Башкортостан","parentcode":"99010001","budglevelcode":"2","budgtypecode":"02","okatocode":"","oktmocode":"80000000","foorgcode":"","foorgcodeubp":"04381","tofkcode":"0100","opendate":"2014-01-01 00:00:00.0","closedate":"","startdate":"2014-01-01 00:00:00.0","enddate":"","filedate":"2021-07-24 00:34:50.0","loaddate":"2021-07-24 22:20:17.0"}
    test_data=preprocs_data(test_data)

    # найдем название пк модели
    pk_field_name=input_model._meta.pk.name
    # узнаем, есть ли уже с таким пк инстанс
    instance=input_model.objects.filter(**{pk_field_name:test_data[pk_field_name]}).first()
    # если нет, создадим, иначе апдейтим
    a=get_ser(Budget)(data=test_data,instance=instance)
    a.is_valid()
    print(a.errors)
    a.save()