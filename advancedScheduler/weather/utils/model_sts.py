from django.db import models


class Enum(models.IntegerChoices):
    @classmethod
    def attr_list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def attr_dict(cls):
        return {i.value: i.name for i in cls}


class BitwiseNumber:
    BIT_1 = 1
    BIT_2 = 2
    BIT_3 = 4
    BIT_4 = 8
    BIT_5 = 16


class Status(Enum):
    DRAFT = BitwiseNumber.BIT_1
    NEW = BitwiseNumber.BIT_2
    ACCEPT = BitwiseNumber.BIT_3
    PICKUP = BitwiseNumber.BIT_4