import sys

# operation (op) codes
PRINT_JAKE      = 1
HALT            = 2
PRINT_NUM       = 3
SAVE            = 4
PRINT_REGISTER  = 5
ADD             = 6

print_jake_program = [
    PRINT_JAKE,
    PRINT_JAKE,
    PRINT_JAKE,
    PRINT_JAKE,
    # HALT,
]

print_some_nums = [
    PRINT_NUM,
    10110010,
    PRINT_NUM,
    18,
    PRINT_NUM,
    24,
    PRINT_NUM,
    42,
    PRINT_JAKE,
    HALT
]

save_num_to_reg = [
    SAVE,   # SAVE, VAL, REG_NUM
    65,
    2,
    PRINT_REGISTER,
    2,
    SAVE,
    154334645,
    6,
    PRINT_REGISTER,
    2,
    PRINT_REGISTER,
    6,
    HALT
]

add_numbers = [
    SAVE,
    12,
    1,
    SAVE,
    45,
    2,
    ADD,
    1,
    2,
    PRINT_REGISTER,
    1,
    SAVE,
    10,
    2,
    ADD,
    1,
    2,
    PRINT_REGISTER,
    1,
    HALT
]

memory = add_numbers


running = True
pc = 0
registers = [0] * 8

while running:
    #  receive instructions, and execute them
    #  if command is PRINT_JAKE, print "Jake!"
    command = memory[pc]

    if command == PRINT_JAKE:
        print("Jake!")
        pc += 1

    # if command is HALT
    #     shutdown
    elif command == HALT:
        running = False
        pc += 1

    elif command == PRINT_NUM:
    #     look at the next line in mem, print that
        num = memory[pc + 1]
        print(num)
        pc += 2

    elif command == SAVE:
        num_to_save = memory[pc + 1]
        register = memory[pc + 2]
        registers[register] = num_to_save
        pc += 3

    elif command == PRINT_REGISTER:
        register = memory[pc + 1]
        print(registers[register])
        pc += 2

    elif command == ADD:
        register1 = memory[pc + 1]
        register2 = memory[pc + 2]
        val1 = registers[register1]
        val2 = registers[register2]
        registers[register1] = val1 + val2
        pc += 3


    # if command is non recognizable
    #     crash :(
    else:
        print(f"Unknown instruction {command}, at address {pc}")
        sys.exit(1)

