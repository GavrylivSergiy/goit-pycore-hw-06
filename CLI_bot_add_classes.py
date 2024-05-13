from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be a 10-digit number.")
        super().__init__(value)

class Record:
    def __init__(self, name, phone):
        self.name = Name(name)
        self.phones = [Phone(phone)]

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def find_phone(self, phone_number):
        for phone in self.phones:
                if str(phone) == phone_number:
                    return phone
        return None

    def edit_phone(self, old_phone, new_phone):
        original_phone = ";".join(str(phone) for phone in self.phones)
        self.delete_phone(old_phone)
        self.add_phone(new_phone)
        new_phone = ";".join(str(phone) for phone in self.phones)
        print (f"Contact updated. Original phone: {original_phone}, New phone {new_phone}")

        return self.__str__()

    def __str__(self):
        phone_numbers = ";".join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name}, phones: {';'.join(map(str, self.phones))}"
    
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete_record(self, name):
        if name in self.data:
            del self.data[name]
            return f"Record {name} deleted."
        else:
            return f"No record found for {name}."

    def find_record(self, name):
        return self.data.get(name)

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Name not found."
        except IndexError:
            return "Not enough arguments."

    return inner

@input_error
def add_contact(args, contacts):
    if len(args) < 2:
        return "Give me name and phone please."
    name = args[0]
    phone = args[1]
    
    record = Record(name, phone)
    contacts.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, contacts):
    name, old_phone, new_phone = args
    record = contacts.find_record(name)
    if record:
        original_phone = str(record.phones[0])
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        return "Error: Name not found."
    
@input_error
def delete_contact(args, contacts):
    if len(args) < 1:
        return "Give me a name to delete."
    name = args[0]
    return contacts.delete_record(name)

@input_error
def show_phone(args, contacts):
    name = args[0]
    record = contacts.find_record(name)
    if record:
        return str(record.phones[0])
    else:
        return "Error: Name not found."

@input_error
def show_all(contacts):
    if contacts:
        return "\n".join(str(record) for record in contacts.data.values())
    else:
        return "No contacts saved."

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        elif command == "delete":
            print(delete_contact(args, contacts))
        elif command == "find_phone":  # Додана команда для пошуку телефону
            if len(args) != 2:
                print("Invalid command. Please provide a name and a phone number.")
                continue
            name, phone_number = args
            record = contacts.find_record(name)
            if record:
                found_phone = record.find_phone(phone_number)
                if found_phone:
                    print(f"{record.name}: {found_phone}")
                else:
                    print("Phone number not found.")
            else:
                print(f"No record found for {name}.")
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
