"""CPU functionality."""

import sys
"""
the spec tells you what numbers = what instructions
"""
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.running = True
        self.ram = [0] * 256
        self.registers = [0] * 8
        # self.R0 = [0] * 8
        # self.R1 = [0] * 8
        # self.R2 = [0] * 8
        # self.R3 = [0] * 8
        # self.R4 = [0] * 8
        # self.R5 = [0] * 8  # IM-interrupt mask
        # self.R6 = [0] * 8  # IS-interrupt status
        # self.R7 = [0] * 8  # SP-stack pointer
        self.PC = 0  # PC
        # self.IR = [0] * 8
        # self.MAR = 0
        self.commands = {}
        self.FL = [0] * 8
        self.commands[0b10000010] = self.LDI  # "LDI"
        self.commands[0b01000111] = self.PRN  # "PRN"
        self.commands[0b00000001] = self.HLT  # "HLT"
        self.commands[0b10100010] = self.MUL  # "MUL"

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, program):
        """Load a program into memory."""

        address = 0
        # print("load")
        with open(program) as p:
            data = p.read()

        lines = data.split("\n")
        instructions = []
        for line in lines:
            new_line = line.split("#")[0].strip()
            if new_line == "":
                continue
            new_line = int(new_line, 2)
            instructions.append(new_line)
        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        # print("Program:", program)
        # print("RAM", self.ram)
        for instruction in instructions:
            self.ram[address] = instruction
            address += 1
        # print("RAM", self.ram)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            IR = self.ram[self.PC]
            # print("run", IR)
            if IR in self.commands:
                # print("running")
                self.commands[IR]()
            # if self.commands[IR] == "LDI":
            #     register = self.ram[self.PC + 1]
            #     value = self.ram[self.PC + 2]
            #     self.registers[register] = value
            #     self.PC += 3
            # elif self.commands[IR] == "PRN":
            #     value = self.registers[self.ram[self.PC + 1]]
            #     print(value)
            #     self.PC += 2
            # elif self.commands[IR] == "HLT":
            #     self.running = False
            #     # self.PC += 1
            #     sys.exit(0)
            # elif self.commands[IR] == "MUL":
            #     first_reg = self.ram[self.PC + 1]
            #     second_reg = self.ram[self.PC + 2]
            #     self.alu(self.commands[IR], first_reg, second_reg)
            #     self.PC += 3
            else:
                print(f'unknown instruction {IR} at address {self.PC}')
                sys.exit(1)

    def LDI(self):
        # print("LDI", self.PC)
        register = self.ram[self.PC + 1]
        # print(register)
        value = self.ram[self.PC + 2]
        # print(value, self.PC + 2)
        self.registers[register] = value
        # print(self.registers[register])
        self.PC += 3

    def PRN(self):
        # print("PRN")
        value = self.registers[self.ram[self.PC + 1]]
        print(value)
        self.PC += 2

    def HLT(self):
        # print("HLT")
        self.running = False
        # self.PC += 1
        sys.exit(0)

    def MUL(self):
        # print("MUL")
        first_reg = self.ram[self.PC + 1]
        second_reg = self.ram[self.PC + 2]
        self.alu("MUL", first_reg, second_reg)
        self.PC += 3