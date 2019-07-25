"""CPU functionality."""

import sys
SP = 7
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
HLT = 0b00000001
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0b00000000] * 256 # base 10 indexing
        self.reg = [0b00000000] * 8
        self.running = False
        self.pc = 0
        self.reg[SP] = 244
        self.branch_table = {
            LDI: self.handle_LDI,
            PRN: self.handle_PRN,
            MUL: self.handle_MUL,
            ADD: self.handle_ADD,
            PUSH: self.handle_PUSH,
            POP: self.handle_POP,
            HLT: self.handle_HLT,
            CALL: self.handle_CALL,
            RET: self.handle_RET
        }
        # self.fl -- mentioned inside trace()
        # self.ie -- mentioned inside trace()
    def handle_RET(self, ir, operand1, operand2):
        pass
        # purpose: return from subroutine
        # pop the value from the top of the stack
        # store it in self.pc
    
    def handle_CALL(self, ir, operand1, operand2):
        pass
        # purpose: call a subroutine (func) at the address stored in the register -- operand1
        # push the address of the instruction DIRECTLY AFTER call to the stack
        # self.pc is set to the address stored in the reg (operand1)
        # jump to the location of self.pc in RAM and execute the first instruction

    def handle_HLT(self, ir, operand1, operand2):
        self.running = False

    def handle_PUSH(self, ir, regnum, operand):
        self.reg[SP] -= 1
        self.ram_write(self.reg[regnum], self.reg[SP])
    
    def handle_POP(self, ir, regnum, operand):
        self.reg[regnum] = self.ram_read(self.reg[SP])
        self.reg[SP] += 1
        
    def handle_LDI(self, ir, regnum, val):
        self.reg[regnum] = val

    def handle_PRN(self, ir, regnum, operand):
        print(self.reg[regnum])

    def handle_MUL(self, ir, num1, num2):
        self.alu("MUL", num1, num2)

    def handle_ADD(self, ir, num1, num2):
        self.alu("ADD", num1, num2)

    def num_operands(self, ir):
        return (ir & 0b11000000) >> 6

    def load(self):
        if len(sys.argv) != 2:
            print(f"usage: {sys.argv[0]} filename")
            sys.exit(1)
        try:
            with open(sys.argv[1]) as f:
                address = 0

                for line in f:
                    num = line.split("#", 1)[0]

                    if num.strip() == '':
                        continue
                    
                    self.ram_write(int(num, 2), address)
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")

    def alu(self, op, reg_a, reg_b):
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def ram_write(self, mdr, mar): # mdr == memory data register
        self.ram[mar] = mdr

    def run(self):
        self.running = True
        while self.running:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            try:
                self.branch_table[ir](ir, operand_a, operand_b)
                self.pc += ((ir & 0b11000000) >> 6) + 1
            except:
                print(f"Unknown instruction {ir}")
                sys.exit(1)