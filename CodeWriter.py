"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        self.out_put = output_stream
        self.index = 0
        pass

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # self.out_put. = filename
        pass

    def write_arithmetic(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given 
        arithmetic command.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        translated_command = ""
        translated_command = self.sp_pop()  # POP X
        if command == "neg":
            translated_command += "D=-D\n"
        elif command == "not":
            translated_command += "D=!D\n"
        else:
            translated_command += "@SP\nAM=M-1\n"  # POP Y
            if command == "add":
                translated_command += "D=D+M\n"  # ADD
            elif command == "sub":
                translated_command += "D=M-D\n"  # sub
            elif command == "and":
                translated_command += "D=D&M\n"  # AND
            elif command == "or":
                translated_command += "D=D|M\n"  # OR
            else:
                if command == "eq":
                    jump_type = "JEQ"
                elif command == "gt":
                    jump_type = "JLT"
                    translated_command += "M=M<<\nD=D<<\nD=D-M\n"
                else:  # command == "lt":
                    jump_type = "JLT"
                    translated_command +="M=M<<\nD=D<<\nD=M-D\n"
                translated_command += "@TRUE.{0}\nD;{1}\nD=0\n@CONTINUE.{0}\n0;JMP\n(TRUE.{0})\nD=-1\n(CONTINUE.{0})\n".format(
                    str(self.index), jump_type)
                self.index += 1
        translated_command += "@SP\nA=M\nM=D\n"
        translated_command += "@SP\nM=M+1\n"  # sp = sp+1
        self.out_put.write(translated_command)

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes the assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        translated_code = ""
        if segment == "local":
            start = "LCL"
        elif segment == "argument":
            start = "ARG"
        elif segment == "this":
            start = "THIS"
        elif segment == "that":
            start = "THAT"
        else:
            start = None
            if segment == "pointer":
                if index == 0:
                    temp = "@THIS"
                else:
                    temp = "@THAT"
                if command == "C_PUSH":
                    translated_code = "{0}\nD=M\n{1}".format(temp, self.sp_push())  # here
                else:
                    translated_code = "{0}{1}\nM=D\n".format(self.sp_pop(), temp)
            elif segment == "constant":
                translated_code = "@{0}\nD=A\n{1}".format(str(index), self.sp_push())  # CHECK
            elif segment == "temp":
                if command == "C_PUSH":
                    translated_code += "{0}{1}".format("@5\nD=A\n@{0}\nA=D+A\nD=M\n".format(str(index)),
                                                       self.sp_push())  # CHECK here
                else:  # POP
                    translated_code += "@5\nD=A\n@{0}\nD=D+A\n@adder\nM=D\n{1)}@adder\nA=M\nM=D\n".format(
                        str(index), self.sp_pop())  # CHECK
            else:  # segment == STATIC
                if command == "C_PUSH":
                    translated_code += "{0}{1}".format("@f.{0}\nD=M\n@SP\n".format(str(index)), self.sp_push())  # CHECK
                else:
                    translated_code += "{1}@f.{0}\nM=D\n".format(str(index), self.sp_pop())  # CHECK
        if start is not None:
            translated_code += "@{1}\nD=M\n@{0}\nA=D+A\n".format(str(index), start)
            if command == "C_PUSH":
                translated_code += "D=M\n" + self.sp_push()  # CHECK
            else:  # POP
                translated_code += "@adder\nM=D\n{0}@adder\nA=M\nM=D\n".format(self.sp_pop())  # CHECK
        self.out_put.write(translated_code)


    def close(self) -> None:
        """Closes the output file."""
        # Your code goes here!
        #self.out_put.close()
        pass

    @staticmethod
    def sp_push():  # pushing to stack
        return "@SP\nA=M\nM=D\n@SP\nM=M+1\n"

    @staticmethod
    def sp_pop():  # poping from stack
        return "@SP\nAM=M-1\nD=M\n"

