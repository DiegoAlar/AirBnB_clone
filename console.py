#!/usr/bin/python3
""" This module contains out line command tnterpreter for the ABNB projecrt
"""

from ast import literal_eval
import models
from models import storage
from cmd import Cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage
import shlex


class HBNBCommand(Cmd):
    """ Class to create the command line interpreter
    """
    prompt = '(hbnb) '

    def precmd(self, line):
        """ retrieve all instances of a class by using: <class name>.all()"""
        st_sliced = line[-2:]
        line_cpy = line[:-2]
        count_objs = 0
        if line.count('.') == 1 and line.count(' ') == 0 and st_sliced == "()":
            splitted = line_cpy.split('.')
            return splitted[1] + ' ' + splitted[0]
        elif line.count('.') == 1 and line.count('(') == 1 and\
                line.count(')') == 1:
            lne = line[:]
            l1 = lne.split('.')
            l2 = l1[1].split('(')
            l2[1] = l2[1][:-1]
            str_t = l2[0] + ' ' + l1[0] + ' '
            l3 = l2[1].replace('"', '')
            for i in l3.split(','):
                str_t += i
            return str_t
        else:
            return line

    def default(self, line):
        """ Called on an input line when command prefix is not recognized"""
        line_split = line[:]
        all_objs = storage.all()
        split = line_split.split(' ')
        if len(split) > 1:
            split1 = split[0]
            split2 = split[1]
            count_objs = 0
            if split1 == "count" and split2 in globals().keys():
                for k, v in all_objs.items():
                    if k.split('.')[0] == split2:
                        count_objs += 1
                print(count_objs)

    def do_create(self, inp):
        """ Creates a new instance of BaseModel, saves it (to the JSON file)
            and prints the id. Ex: $ create BaseModel
        """
        if inp == "":
            print("** class name missing **")
        elif inp not in globals().keys():
            print("** class doesn't exist **")
        else:
            new_obj = globals()[inp]()
            new_obj.save()
            print(new_obj.id)

    def do_show(self, inp):
        """ Prints the string representation of an instance based on the class
            name and id.
        """
        flag = 0
        list_args = inp.split(' ')
        if list_args[0] == "":
            print("** class name missing **")
        elif list_args[0] not in globals().keys():
            print("** class doesn't exist **")
        elif len(list_args) <= 1:
            print("** instance id missing **")
        else:
            all_objs = storage.all()
            for k, v in all_objs.items():
                splitted = k.split('.')
                if splitted[1] == list_args[1] and list_args[0] == splitted[0]:
                    print(v)
                    flag = 1
            if flag == 0:
                print("** no instance found **")

    def do_destroy(self, inp):
        """Deletes an instance based on the class name and id (save the
           change into the JSON file).
        """
        flag = 0
        list_args = inp.split(' ')
        if list_args[0] == "":
            print("** class name missing **")
        elif list_args[0] not in globals().keys():
            print("** class doesn't exist **")
        elif len(list_args) <= 1:
            print("** instance id missing **")
        else:
            all_objs = storage.all()
            for k, v in all_objs.items():
                splitted = k.split('.')
                if splitted[1] == list_args[1] and list_args[0] == splitted[0]:
                    del all_objs[k]
                    flag = 1
                    storage.save()
                    break
            if flag == 0:
                print("** no instance found **")

    def do_all(self, inp):
        """Prints all string representation of all
           instances based or not on the class name.
        """

        my_list = []
        if inp != "" and inp.split(' ')[0] not in globals().keys():
            print("** class doesn't exist **")
        else:
            all_objs = storage.all()
            for k, v in all_objs.items():
                if inp == "":
                    my_list.append(v.__str__())
                elif k.split('.')[0] == inp.split(' ')[0]:
                    my_list.append(v.__str__())
            if len(my_list) > 0:
                print(my_list)

    def do_update(self, inp):
        """Updates an instance based on the class name and id by
           adding or updating attribute
        """

        flag = 0
        letters_count = 0
        list_args = shlex.split(inp)
        if len(list_args) == 0:
            print("** class name missing **")
        elif list_args[0] not in globals().keys():
            print("** class doesn't exist **")
        elif len(list_args) == 1:
            print("** instance id missing **")
        else:
            if len(list_args) >= 4:
                for i in list_args[3]:
                    if i.isalpha():
                        letters_count += 1
            all_objs = storage.all()
            for k, v in all_objs.items():
                splitted = k.split('.')
                if splitted[1] == list_args[1] and list_args[0] == splitted[0]:
                    flag = 1
                    if len(list_args) == 2:
                        print("** attribute name missing **")
                        break
                    elif len(list_args) <= 3:
                        print("** value missing **")
                        break
                    else:
                        if (list_args[3].isdigit()):
                            setattr(v, list_args[2], int(list_args[3]))
                        elif (list_args[3].isalpha() is False and
                                list_args[3].count('.') == 1 and
                                letters_count == 0):
                            setattr(v, list_args[2], float(list_args[3]))
                        else:
                            setattr(v, list_args[2], list_args[3])
                        storage.save()
                        break
            if flag == 0:
                print("** no instance found **")

    def do_quit(self, inp):
        """
        Quit command to exit the program
        """
        return True

    def help_quit(quit):
        """
        Describes the mode to quit the program
        """
        print('Quit command to exit the program')

    def emptyline(self):
        """Adds an empty line when program is closed
        """
        pass

    do_EOF = do_quit
    help_EOF = help_quit


if __name__ == '__main__':
    HBNBCommand().cmdloop()
