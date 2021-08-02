import datetime

from rest_framework import serializers
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from test.models import Budget,GlavBudget

def get_func(field):
    ''' возвращаем переписанный метод to_internal_value
     для foreign_key полей, на случай, когда
     дочерний элемент ссылается на несуществующий родительский'''
    def fk_to_internal_value(data=None):
        self = field
        if self.pk_field is not None:
            data = self.pk_field.to_internal_value(data)
        queryset = self.get_queryset()
        try:
            if isinstance(data, bool):
                raise TypeError
            return queryset.get(pk=data)
        except ObjectDoesNotExist:
            # та самая строчка, создадим объект,
            # если попадется с таким же пк, обновим его правильно
            return queryset.create(pk=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)
    return fk_to_internal_value


def get_ser(model):
    ''' возвращаем сериализатор для нашей модели
    так как модель заранее неизвестна, то и сериализатор неизвестен
    подкидываем на вход модельку и делаем под нее сер'''
    class ParseModelSerizer (serializers.ModelSerializer):
        class Meta:
            fields='__all__'

        def get_fields(self):
            ''' переопределим метод для fk полей,
            если они ссылаются на несуществующий инстанс'''
            fields=super().get_fields()
            for field in fields.values():
                if isinstance(field,serializers.PrimaryKeyRelatedField):
                    field.to_internal_value=get_func(field)
            return fields
    ParseModelSerizer.Meta.model=model
    return ParseModelSerizer