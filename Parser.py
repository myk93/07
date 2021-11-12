"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is:
        self.input_lines = input_file.read().splitlines()
        self.cleanup_code()
        self.current_line = -1

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        if len(self.input_lines) == self.current_line:
            return False
        return True

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        # Your code goes here!
        if self.has_more_commands():
            self.current_line += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        # Your code goes here!
        if self.input_lines[self.current_line].split(" ")[0] == "pop":
            return "C_POP"
        elif self.input_lines[self.current_line].split(" ")[0] == "push":
            return "C_PUSH"
        else:
            return "C_ARITHMETIC"
        pass

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        # Your code goes here!
        if self.command_type() == "C_ARITHMETIC":
            return self.input_lines[self.current_line].split("//")[0].replace(" ", "")
        else:
            return self.input_lines[self.current_line].split(" ")[1]
        pass

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        # Your code goes here!
        return int(self.input_lines[self.current_line].split(" ")[2])
        pass

    def cleanup_code(self):
        i = 0
        while i != len(self.input_lines):
            if len(self.input_lines[i].replace(" ", "")) == 0 or self.input_lines[i].replace(" ", "")[0] == "/":
                self.input_lines.pop(i)
            else:
                #removing tabs
                self.input_lines[i] = self.input_lines[i].replace("\t", "")
                ' '.join(self.input_lines[i].split())
                i += 1
