from collections import UserDict
import datetime
from typing import Optional
import re


class Field:
    def __init__(self, value=None):
        self.value = self.process_input(value)

    def process_input(self, value):
        return value


class Name(Field):
    pass


class Phone(Field):
    def process_input(self, value):
        if not re.match(r'^\+?1?\d{9,15}$', value):
            raise ValueError("Invalid phone number")
        return value


class Birthday(Field):
    def process_input(self, value: Optional[datetime.date]):
        if value is not None and not isinstance(value, datetime.date):
            raise ValueError("Invalid date")
        return value


class Record:
    def __init__(self, name, phones=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in (phones or [])]
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday.value is None:
            return None
        today = datetime.date.today()
        next_birthday = datetime.date(
            today.year, self.birthday.value.month, self.birthday.value.day)
        if today > next_birthday:
            next_birthday = datetime.date(
                today.year + 1, self.birthday.value.month, self.birthday.value.day)
        return (next_birthday - today).days


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def __iter__(self, n):
        records = list(self.data.values())
        while records:
            yield records[:n]
            records = records[n:]
