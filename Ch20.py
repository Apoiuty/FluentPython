import abc


class AutoStorage:
    __cnt = 0

    def __init__(self):
        cls_name = self.__class__.__name__
        index = self.__class__.__cnt
        self.storage_name = f'__{cls_name}#{index}'
        self.__class__.__cnt += 1

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        return getattr(instance, self.storage_name)


class Validated(abc.ABC, AutoStorage):
    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        """return validated value or raise ValueError"""


class Quantity(Validated):

    def validate(self, instance, value):
        if value >= 0:
            return value
        else:
            raise ValueError


class NoBlank(Validated):

    def validate(self, instance, value):
        value = value.strip()

        if len(value) == 0:
            raise ValueError
        else:
            return value


class LineItem:
    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


print(LineItem.__dict__)
