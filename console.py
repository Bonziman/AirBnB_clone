#!/usr/bin/python3
"""the console module that produces a shell like console to\
manage the project"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
import re
from shlex import split


def parse(arg):
    """parses the args and splits them"""
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """custpom interpreter for the HBNB project

    Args:
    cmd (str): commande
    """

    prompt = "(hbnb) "
    __classes = {
            "BaseModel",
            "User",
            "State",
            "City",
            "Place",
            "Amenity",
            "Review"
            }

    def do_quit(self, arg):
        """Use quit command to exit the program"""
        return True

    def emptyline(self):
        """An empty line + ENTER shouldn’t execute anything"""
        pass

    def do_EOF(self, arg):
        """Singal EOF to exit the program"""

        return True

    def do_create(self, arg):
        """Usage: create {class}
        creates a new class instance saves it into a JSON file, and print id
        """

        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argl[0])().id)
            storage.save()

    def do_show(self, arg):
        """Prints the string representation of an instance based on:
        the class name and id
        Usage: show <class> <id>
        """

        args = parse(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        elif len(args) == 1:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        if key in storage.all():
            instance = storage.all()[key]
            print(instance)
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """deletes an instance based on the classname and id
        Usage: destroy <class> <id>"""

        args = parse(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """prints all string representation of all instances based or\
        not on the class name.
        Usage: all <class>(optional)
        """
        args = parse(arg)
        if len(args) == 0:
            result = []
            for key, instance in storage.all().items():
                result.append(str(instance))
            print(result)
        elif len(args) == 1:
            class_name = args[0]
            if class_name not in HBNBCommand.__classes:
                print("** class doesn't exist **")
                return
            else:
                result = []
                for key, instance in storage.all().items():
                    if instance.__class__.__name__ == class_name:
                        result.append(str(instance))
                print(result)

    def do_update(self, arg):
        """Updates an instance based on class name and id b adding\
        or updating attributes.
        Usage: update <class> <id> <attribute name> "<attribute value>"
        """
        args = parse(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        if len(args) == 2:
            print("** attribute name missing **")
            return
        arg_name = args[2]
        if len(args) == 3:
            print("** value missing **")
            return
        arg_value = args[3]
        if key not in storage.all():
            print("** no instance found **")
            return
        else:
            instance = storage.all()[key]
            setattr(instance, arg_name, arg_value)
            storage.save()

    def default(self, line):
        """Called when the command is not recognized."""
        show_match = re.match(r'^(\w+)\.show\("([^"]+)"\)$', line)
        destroy_match = re.match(r'^(\w+)\.destroy\("([^"]+)"\)$', line)
        update_match = re.match(r'^(\w+)\.update\('
                                r'("[^"]+"),\s*'
                                r'"([^"]+)",\s*'
                                r'"([^"]+)"\)$', line)
        if line.endswith(".all()"):
            parts = line.split('.')
            class_name = parts[0]
            self.do_all(class_name)
        elif line.endswith(".count()"):
            parts = line.split('.')
            class_name = parts[0]
            count = 0
            if class_name in HBNBCommand.__classes:
                for key, instance in storage.all().items():
                    if instance.__class__.__name__ == class_name:
                        count += 1
                print(count)
            else:
                print("** class doesn't exist **")
        elif show_match:
            class_name = show_match.group(1)
            obj_id = show_match.group(2)
            arg = class_name + " " + obj_id
            self.do_show(arg)
        elif destroy_match:
            class_name = destroy_match.group(1)
            obj_id = destroy_match.group(2)
            arg = class_name + " " + obj_id
            self.do_destroy(arg)
        elif update_match:
            class_name = update_match.group(1)
            obj_id = update_match.group(2)
            attr_name = update_match.group(3)
            attr_value = update_match.group(4)
            ar = class_name + " " + obj_id + " " + attr_name + " " + attr_value
            self.do_update(ar)
        else:
            print("** Invalid syntax **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
