"""CPU functionality."""

import sys
from datetime import datetime

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
        self.FL = [0] * 8
        # self.R5 = [0] * 8  # IM-interrupt mask
        # self.R6 = [0] * 8  # IS-interrupt status
        # self.R7 = [0] * 8  # SP-stack pointer

        # self.IR = [0] * 8
        # self.MAR = 0
        self.commands = {}

        self.PC = 0
        self.registers[7] = 0xF4

        self.commands[0b10000010] = self.LDI
        self.commands[0b01000111] = self.PRN
        self.commands[0b00000001] = self.HLT
        self.commands[0b10100000] = self.ADD
        self.commands[0b10100010] = self.MUL
        self.commands[0b01000101] = self.PUSH
        self.commands[0b01000110] = self.POP
        self.commands[0b01010000] = self.CALL
        self.commands[0b00010001] = self.RET
        self.commands[0b10000100] = self.ST
        self.commands[0b01010100] = self.JMP
        self.commands[0b01001000] = self.PRA
        self.commands[0b00010011] = self.IRET

        self.start = datetime.now().timetuple()[5]
        self.set_start = False
        self.count = 1

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, program):
        """Load a program into memory."""
        address = 0
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
        for instruction in instructions:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        elif op == "CMP":
            if reg_a == reg_b:
                self.FL = 1
            elif reg_a < reg_b:
                self.FL = 4
            elif reg_a > reg_b:
                self.FL = 2
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            now = datetime.now().timetuple()[5]

            if now > self.start:
                self.start = now
                self.registers[6] = 0b00000001
                if now == 59:
                    self.set_start = True
            if now == 0 and self.set_start:
                self.set_start = False
                self.start = now - 1

            IM = self.registers[5]
            IS = self.registers[6]
            masked_interrupts = IM & IS

            for i in range(8):
                interrupt_happened = (masked_interrupts >> i) & 1 == 1
                if interrupt_happened and i == 0:
                    self.handle_timer()
                elif interrupt_happened and i == 1:
                    print("Whoa!!!")
            IR = self.ram[self.PC]
            if IR in self.commands:
                self.commands[IR]()
            elif IR not in self.commands:
                print(f'unknown instruction {IR} at address {self.PC}')
                sys.exit(1)

    def sets_pointer(self, op_code):
        return False

    def handle_timer(self):
        self.registers[5] = 0
        self.registers[6] = 0
        self.push_thing(self.PC)
        self.push_thing(self.FL)
        for i in range(7):
            self.push_thing(self.registers[i])

        address = self.ram[0xF8]
        self.PC = address

    def push_thing(self, thing):
        self.registers[7] -= 1
        self.ram[self.registers[7]] = thing

    def finish_it(self):
        for i in reversed(range(7)):
            self.registers[i] = self.ram[self.registers[7]]
            self.registers[7] += 1
        self.FL = self.ram[self.registers[7]]
        self.registers[7] += 1
        self.PC = self.ram[self.registers[7]]
        self.registers[7] += 1
        self.registers[5] = 1

    def LDI(self):
        register = self.ram[self.PC + 1]
        value = self.ram[self.PC + 2]
        self.registers[register] = value
        self.PC += 3

    def ST(self):
        regB = self.registers[self.ram[self.PC + 2]]
        regA = self.registers[self.ram[self.PC + 1]]
        self.ram[regA] = regB
        self.PC += 3

    def PUSH(self):
        if self.registers[7] <= self.PC + 1:
            print("Stack Overflow")
            self.HLT()
        self.registers[7] -= 1
        self.ram[self.registers[7]] = self.registers[self.ram[self.PC + 1]]
        self.PC += 2

    def POP(self):
        if self.registers[7] > 0xF4:
            print("Stack Underflow")
            self.HLT()
        self.registers[self.ram[self.PC + 1]] = self.ram[self.registers[7]]
        self.registers[7] += 1
        self.PC += 2

    def JMP(self):
        self.PC = self.registers[self.ram[self.PC + 1]]

    def CALL(self):
        self.registers[7] -= 1
        self.ram[self.registers[7]] = self.PC + 2
        self.PC = self.registers[self.ram[self.PC + 1]]
        pass

    def RET(self):
        self.PC = self.ram[self.registers[7]]
        self.registers[7] += 1

    def IRET(self):
        self.finish_it()

    def HLT(self):
        self.running = False
        sys.exit(0)

    def PRN(self):
        value = self.registers[self.ram[self.PC + 1]]
        print(value)
        self.PC += 2

    def PRA(self):
        value = self.registers[self.ram[self.PC + 1]]
        text = chr(value)
        print(text)
        self.count += 1
        self.PC += 2

    def ADD(self):
        first_reg = self.ram[self.PC + 1]
        second_reg = self.ram[self.PC + 2]
        self.alu("ADD", first_reg, second_reg)
        self.PC += 3

    def MUL(self):
        first_reg = self.ram[self.PC + 1]
        second_reg = self.ram[self.PC + 2]
        self.alu("MUL", first_reg, second_reg)
        self.PC += 3

    def CMP(self):
        pass
