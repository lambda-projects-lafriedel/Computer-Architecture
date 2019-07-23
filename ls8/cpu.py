"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256 # base 10 indexing
        self.reg = [0] * 8
        self.pc = 0
        self.branch_table = {
            LDI: self.handle_LDI,
            PRN: self.handle_PRN,
            MUL: self.handle_MUL
        }
        # self.fl -- mentioned inside trace()
        # self.ie -- mentioned inside trace()

    def handle_LDI(self, reg, val):
        self.reg[reg] = val
        self.pc += 3

    def handle_PRN(self, reg):
        print(self.reg[reg])
        self.pc += 2

    def handle_MUL(self, num1, num2):
        self.alu("MUL", num1, num2)
        self.pc += 3

    def load(self):
        if len(sys.argv) != 2:
            print(f"usage: {sys.argv[0]} filename")
            sys.exit(1)
        try:
            with open(sys.argv[1]) as f:
                address = 0

                for line in f:
                    # read contents line by line
                    num = line.split("#", 1)[0]

                    if num.strip() == '':
                        continue
                    
                    # save appropriate data to RAM
                    # make sure to convert binary strings to ints
                    self.ram_write(int(num, 2), address)

                    # increase address by 1
                    address += 1

        # catch errors if user doesn't send appropriate args
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")

    def alu(self, op, reg_a, reg_b):
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        if op == "MUL":
            product = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = product
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
            print(" %02X" % self.reg[i], end='')

        print()
    
    def ram_read(self, mar): # mar == memory address register
        return self.ram[mar]
        # might set the initial value of the stack pointer here later

    def ram_write(self, mdr, mar): # mdr == memory data register
        self.ram[mar] = mdr
        # might set the initial value of the stack pointer here later

    def run(self):
        running = True

        while running:
            ir = self.ram[self.pc]
            # using self.ram_read, read the bytes at pc+1 and pc+2 into variables operand_a and operand_b
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # if ir == HLT, increase pc by 1 and set running to False to close while
            if ir == 0b00000001:
                self.pc += 1
                running = False
            # if ir == LDI, set operand_a to the value of operand_b, and increase self.pc by 3
            elif ir == LDI:
                self.handle_LDI(operand_a, operand_b)
            # if ir == PRN, print the numeric value stored in operand_a
            elif ir == PRN:
                self.handle_PRN(operand_a)
            # if ir == MUL, send to self.alu() and mult a * b
            elif ir == MUL:
                self.handle_MUL(operand_a, operand_b)
            else:
                print(f"Unknown instruction {ir}")
                sys.exit(1)

