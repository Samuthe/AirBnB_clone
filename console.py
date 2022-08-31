#!/usr/bin/python3
""" Command line interpreter module
"""
import cmd
from models import storage
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """ Command line interpreter class
        Private attributes:
            __classes: list of classes
        Public class attributes:
            cmd.Comd.prompt: prompt to display for interactive mode
        Public instance methods:
            Command methods:
                do_create, do_show, do_destroy, do_upate, do_all, do_EOF,
                do_quit
            Help methods:
                help_create, help_show, help_destroy,help_update,
                help_all, help_EOF, help_quit, help_help
    """

    cmd.Cmd.prompt = '(hbnb) '
    __classes = ["BaseModel", "User", "State", "City",
                 "Amenity", "Place", "Review"]

    def do_create(self, line):
        """ Creates new BaseModel instance,
            saves it to JSON file and print its id
            Args:
                line (str)
            Return: nothing
        """
        if line:
            class_name = line.split()[0].strip('"')
            if class_name in HBNBCommand.__classes:
                new_object = BaseModel()
                new_object.save()
                print(new_object.id)
            else:
                HBNBCommand.class_exists()
        else:
            HBNBCommand.class_missing()

    def do_show(self, line):
        """ Display string representation of an instance based
            on the class name and id
            Args:
                line (str): instance's class name and id
            Return: nothing
        """
        if HBNBCommand.validate(line):
            obj_id = line.split()[1].strip('"')
            for key in storage._FileStorage__objects.keys():
                if storage._FileStorage__objects[key].id == obj_id:
                    print(storage._FileStorage__objects[key])
                    break

    def do_destroy(self, line):
        """ Search and destroy object using its class name and id
            Args:
                line (str): object's class name and id
            Return: nothing
        """
        if HBNBCommand.validate(line):
            obj_id = line.split()[1].strip('"')
            for key in storage._FileStorage__objects.keys():
                if storage._FileStorage__objects[key].id == obj_id:
                    del(storage._FileStorage__objects[key])
                    storage.save()
                    break

    def do_all(self, line):
        """ Display a list of string representations of all objects
            of a specific class
            Args:
                line (str): class name
            Return: nothing
        """
        if line:
            class_name = line.split()[0].strip('"')
            if class_name in HBNBCommand.__classes:
                my_objects = []
                for i in storage._FileStorage__objects.keys():
                    if storage._FileStorage__objects[i].__class__.__name__ == \
                       class_name:
                        my_objects.append(str(
                            storage._FileStorage__objects[i]))
            else:
                HBNBCommand.class_exists()
                return
        else:
            my_objects = [str(storage._FileStorage__objects[i])
                          for i in storage._FileStorage__objects.keys()]
        print(my_objects)

    def do_update(self, line):
        """ Update an object's existing attribute or add new
            attribute to the object
            Args:
                line (str): class name, object's id, attribute name,
                            attribute value
            Return: nothing
        """
        if HBNBCommand.validate(line) and \
           HBNBCommand.validate_attr(line.split()):
            class_name, obj_id, attr_name, attr_val = line.split()[:4]
            for i in storage._FileStorage__objects.keys():
                if storage._FileStorage__objects[i].id == obj_id.strip('"'):
                    obj = storage._FileStorage__objects[i]
                    setattr(obj, attr_name.strip('"'), attr_val.strip('"'))
                    obj.save()
                    break

    def do_quit(self, line):
        """ Exit program gracefully
            Args: none
            Return: nothing
        """
        exit()

    def do_EOF(self, line):
        """ Exit program when receiving terminated signal
            Args: none
            Return: True
        """
        print()
        return True

    def emptyline(self):
        """ Print new line when user enters no command
            Args: none
            Return: self
        """

    def help_create(self):
        """ Help function for create command """
        print("Usage: create <class name>\n" +
              "Create command to create new object instance.\n")

    def help_show(self):
        """ Help function for show command """
        print("Usage: show <class name> <id>\n" +
              "Show command to search for object instance by",
              "class and id, and print it.\n")

    def help_destroy(self):
        """ Help function for destroy command """
        print("Usage: destroy <class name > <id>\n" +
              "Destroy command to search for object instance by",
              "class and id, and delete it\n")

    def help_all(self):
        """ Help function for all command """
        print("Usage: all [class name]\n" +
              "Display all objects or all objects of a specific",
              "class\n")

    def help_update(self):
        """ Help function for update command """
        print("Usage: update <class name> <id> <attribute name>",
              '"<attribute value>"\n' + "Update command to search for",
              "object by id and update it using passed",
              "attribute name and value\n")

    def help_quit(self):
        """ Help function for quit command """
        print("Quit command to exit the program gracefully\n")

    def help_EOF(self):
        """ Help function for EOF command """
        print("Exit program when Ctrl + D is entered\n")

    def help_help(self):
        """ Help function for help command """
        print("Usage: help [topic/command]\nHelp command to display",
              "information about a commands\n")

    @staticmethod
    def class_exists():
        """ Print error message when a class doesn't exist
            Args: none
            Return: nothing
        """
        print("** class doesn't exist **")

    @staticmethod
    def class_missing():
        """ Display error message when user doesn't provide class name
            Args: none
            Return: nothing
        """
        print("** class name missing **")

    @staticmethod
    def id_missing():
        """ Display error message when user doesn't provide object's id
            Args: none
            Return: nothing
        """
        print("** instance id missing **")

    @staticmethod
    def not_found():
        """ Display error message an object's id is missing
            Arg: none
            Return: nothing
        """
        print("** no instance found **")

    @staticmethod
    def validate(line):
        """ Checks for errors in user input user input
            Args:
                line (str): user input
            Return: True if input passes all validation
                    False if input fails one of the checks
        """
        if line:
            args = line.split()
            class_name = args[0].strip('"')
            if class_name in HBNBCommand.__classes:
                if len(args) > 1:
                    obj_id = args[1].strip('"')
                    if any(storage._FileStorage__objects[i].id == obj_id
                           for i in storage._FileStorage__objects.keys()):
                        return True
                    else:
                        HBNBCommand.not_found()
                else:
                    HBNBCommand.id_missing()
            else:
                HBNBCommand.class_exists()
        else:
            HBNBCommand.class_missing()
        return False

    @staticmethod
    def validate_attr(args):
        """ Checks if attribute name and value are passed
            in do_upate method
            Args:
                args: list of arguments
            Return: nothing
        """
        if len(args) < 3:
            print("** attribute name missing **")
        elif len(args) < 4:
            print("** value missing **")
        else:
            return True
        return False


if __name__ == "__main__":
    HBNBCommand().cmdloop()
