"""CPU functionality."""

import sys
SP = 7
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
HLT = 0b00000001

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0b00000000] * 256 # base 10 indexing
        self.reg = [0b00000000] * 8 # by default, R7 is the stack pointer
        # SP points at the value at the top of the stack (most recently pushed), or at address 244 if the stack is empty
        self.running = False
        self.pc = 0
        self.reg[SP] = 244
        self.branch_table = {
            LDI: self.handle_LDI,
            PRN: self.handle_PRN,
            MUL: self.handle_MUL,
            PUSH: self.handle_PUSH,
            POP: self.handle_POP,
            HLT: self.handle_HLT
        }
        # self.fl -- mentioned inside trace()
        # self.ie -- mentioned inside trace()

    def handle_HLT(self, ir, operand1, operand2):
        self.running = False

    def handle_PUSH(self, ir, regnum, operand):
        # self.ram_write(val, self.reg[SP])
        num_operands = (ir & 0b11000000) >> 6
        self.reg[SP] -= 1
        self.ram[self.reg[SP]] = self.reg[regnum]
        self.pc += num_operands + 1
    
    def handle_POP(self, ir, regnum, operand):
        # val = self.ram[self.reg[SP]]
        num_operands = (ir & 0b11000000) >> 6
        self.reg[regnum] = self.ram[self.reg[SP]]
        self.reg[SP] += 1
        self.pc += num_operands + 1
        

    def handle_LDI(self, ir, reg, val):
        num_operands = (ir & 0b11000000) >> 6
        self.reg[reg] = val
        self.pc += num_operands + 1
        #self.pc += 3

    def handle_PRN(self, ir, regnum, operand):
        num_operands = (ir & 0b11000000) >> 6
        print(self.reg[regnum])
        self.pc += num_operands + 1
        #self.pc += 2

    def handle_MUL(self, ir, num1, num2):
        num_operands = (ir & 0b11000000) >> 6
        self.alu("MUL", num1, num2)
        self.pc += num_operands + 1
        #self.pc += 3

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
        self.running = True
        self.trace()
        while self.running:
            # initialize the stack pointer
            # using self.ram_read, read the bytes at pc+1 and pc+2 into variables operand_a and operand_b
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            try:
                self.branch_table[ir](ir, operand_a, operand_b)
            except:
                print(f"Unknown instruction {ir}")
                sys.exit(1)