#!/usr/bin/python3
"the console module that produces a shell like console to manage the project"
import cmd
class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    def do_quit(self, arg):
        """Use quit command to exit the program"""
        return True
    def do_EOF(self, arg):
        """Singal EOF to exit the program"""
        return True
if __name__ == '__main__':
    HBNBCommand().cmdloop()
