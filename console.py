#!/usr/bin/python3
"the console module that produces a shell like console to manage the project"
import cmd
from models.base_model import BaseModel
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
    """custpom interpreter for the HBNB project"""
    """prompt = "\033[1;32m(hbnb)\033[0m """
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

if __name__ == '__main__':
    HBNBCommand().cmdloop()
