"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256 # base 10 indexing
        self.reg = [0] * 8
        self.pc = 0
        # self.fl -- mentioned inside trace()
        # self.ie -- mentioned inside trace()


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

                    #increase address by 1
                    address += 1

        # catch errors if user doesn't send appropriate args
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
        # use command line arguments to open a file

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
    
    def ram_read(self, mar): # mar == memory address register (the address that is being read or written to)
        # get address to read
        # return the value stored at that address
        return self.ram[mar]
        # might set the initial value of the stack pointer here later

    def ram_write(self, mdr, mar): # mdr == memory data register (the data that was read, or to write)
        # set the value of mdr to the location associated with mar
        self.ram[mar] = mdr
        # might set the initial value of the stack pointer here later

    def run(self):
        running = True
        # read the memory address stored in self.pc
        # store that result in the IR (which can just be a local variable here)
        while running:
            ir = self.ram[self.pc]
            # using self.ram_read, read the bytes at pc+1 and pc+2 into variables operand_a and operand_b
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # depending on the value of the opcode, perform actions needed for each instruction
                # ex: if opcode == x, do this, elif opcode == y, do that, else: print(f"unknown instruction {command}")
            # if ir == HLT, increase pc by 1 and set running to False to close while
            if ir == 0b00000001:
                self.pc += 1
                running = False
            # if ir == LDI, set operand_a to the value of operand_b, and increase self.pc by 3
            elif ir == 0b10000010:
                self.reg[operand_a] = operand_b
                self.pc += 3
            # if ir == PRN, print the numeric value stored in operand_a
            elif ir == 0b01000111:
                print(self.reg[operand_a])
                self.pc += 2
            
            else:
                print(f"Unknown instruction {ir}")
                sys.exit(1)
            # ensure to increase pc the appropriate amount at the end of each instruction's execution
            # check the spec for the number of bytes used per instruction (determined from the "two high bits, ie 6-7")

