from passlib.hash import bcrypt
from tortoise import fields, models, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator


class CargoType(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=256, null=False, unique=True)


class Rate(models.Model):
    id = fields.IntField(pk=True)
    date = fields.DateField(null=False)
    rate = fields.FloatField(null=False)
    cargo_type = fields.ForeignKeyField('models.CargoType', related_name='rates')

    class Meta:
        unique_together = ('id', 'date')


class Role(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=32, null=False)


class User(models.Model):
    id = fields.IntField(pk=True)
    login = fields.CharField(max_length=32, null=False, unique=True)
    password_hash = fields.CharField(max_length=256, null=False)
    role = fields.ForeignKeyField('models.Role', related_name='users')

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.password_hash)

    class PydanticMeta:
        exclude = ["password_hash"]
