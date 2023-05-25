from address_book import AddressBook, Record, Phone, Birthday, Name
import datetime


def input_error(handler):
    def inner(name, *args):
        try:
            return handler(name, *args)
        except (KeyError, ValueError, IndexError) as error:
            return str(error)
    return inner


@input_error
def add_contact(contacts, name, phone, birthday=None):
    if birthday:
        birthday = datetime.datetime.strptime(birthday, "%d-%m-%Y").date()
    record = Record(Name(name), [Phone(phone)], Birthday(birthday))
    contacts.add_record(record)
    return f"Contact {name} added."


@input_error
def change_contact(contacts, name, phone, birthday=None):
    if name.lower() in contacts.data:
        record = contacts.data[name.lower()]
        if phone:
            record.phones[0].value = phone
        if birthday:
            record.birthday.value = datetime.datetime.strptime(
                birthday, "%d-%m-%Y").date()
        return f"Contact {name} updated."
    else:
        raise KeyError("Contact not found.")


@input_error
def find_contact(contacts, name):
    return contacts.data[name.lower()].phones[0].value


@input_error
def days_to_birthday(contacts, name):
    if name.lower() in contacts.data:
        record = contacts.data[name.lower()]
        return record.days_to_birthday()


@input_error
def show_all(contacts):
    result = ["Contacts:"]
    for name, record in contacts.data.items():
        result.append(f"{name}: {record.phones[0].value}")
    return "\n".join(result)


def main():
    contacts = AddressBook()
    print("Welcome to the assistant!")

    while True:
        user_input = input("\nEnter your command: ").strip().lower()
        words = user_input.split()

        if user_input in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        elif user_input == "hello":
            print("How can I help you?")
        elif words[0] == "add":
            print(add_contact(
                contacts, words[1], words[2], words[3] if len(words) > 3 else None))
        elif words[0] == "change":
            print(change_contact(
                contacts, words[1], words[2], words[3] if len(words) > 3 else None))
        elif words[0] == "phone":
            print(find_contact(contacts, words[1]))
        elif words[0] == "birthday":
            days = days_to_birthday(contacts, words[1])
            if days is not None:
                print(f"Days until next birthday: {days}")
            else:
                print("Birthday not set for this contact.")
        elif user_input == "show all":
            print(show_all(contacts))
        else:
            print("Command not recognized. Try again.")


if __name__ == "__main__":
    main()
