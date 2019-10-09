# Author: Trung Le
# Supported instrs:
# addi, sub, beq, ori, sw


def sim(program):
    finished = False  # Is the simulation finished?
    PC = 0  # Program Counter
    register = [0] * 32  # Let's initialize 32 empty registers
    mem = [0] * 12288  # Let's initialize 0x3000 or 12288 spaces in memory. I know this is inefficient...
    # But my machine has 16GB of RAM, its ok :)
    DIC = 0  # Dynamic Instr Count
    while (not (finished)):
        if PC == len(program) - 4:
            finished = True
        fetch = program[PC]
        DIC += 1
        # print(hex(int(fetch,2)), PC)
        if fetch[0:6] == '001000':  # ADDI
            PC += 4
            s = int(fetch[6:11], 2)
            t = int(fetch[11:16], 2)
            imm = -(65536 - int(fetch[16:], 2)) if fetch[16] == '1' else int(fetch[16:], 2)
            register[t] = register[s] + imm

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000100010':  # SUB
            PC += 4
            s = int(fetch[6:11], 2)
            t = int(fetch[11:16], 2)
            d = int(fetch[16:21], 2)
            register[d] = register[s] - register[t]

        elif fetch[0:6] == '000100':  # BEQ
            PC += 4
            s = int(fetch[6:11], 2)
            t = int(fetch[11:16], 2)
            imm = -(65536 - int(fetch[16:], 2)) if fetch[16] == '1' else int(fetch[16:], 2)
            # Compare the registers and decide if jumping or not
            if register[s] == register[t]:
                PC += imm * 4

        elif fetch[0:6] == '001101':  # ORI
            PC += 4
            s = int(fetch[6:11], 2)
            t = int(fetch[11:16], 2)
            imm = int(fetch[16:], 2)
            register[t] = register[s] | imm

        elif fetch[0:6] == '101011':  # SW
            PC += 4
            s = int(fetch[6:11], 2)
            t = int(fetch[11:16], 2)
            offset = -(65536 - int(fetch[16:], 2)) if fetch[16] == '1' else int(fetch[16:], 2)
            offset = offset + register[s]
            mem[offset] = register[t]
        #bne
        elif fetch[0:6] == '000101':  # BNE
            PC += 4
            rs = int(fetch[6:11], 2)
            rt = int(fetch[11:16], 2)
            imm = -(65536 - int(fetch[16:], 2)) if fetch[16] == '1' else int(fetch[16:], 2)
            # Compare the registers and decide if jumping or not
            if register[rs] != register[rt]:
                PC += imm * 4


        #srl
        elif fetch[0:6] == '000000' and fetch[26:32] == '000010':  # SRL
            PC += 4
            rs = int(fetch[6:11], 2)
            rt = int(fetch[11:16], 2)
            rd = int(fetch[16:21], 2)
            sh = int(fetch[21:26],2)

            register[rd] = rt/2**sh

        #lw
        elif fetch[0:6] == '100011':  # LW
            PC += 4
            rs = int(fetch[6:11], 2)
            rt = int(fetch[11:16], 2)
            imm = -(65536 - int(fetch[16:], 2)) if fetch[16] == '1' else int(fetch[16:], 2)

            register[rt] = mem[rs + imm]

        #andi
        elif fetch[0:6] == '000101':  # ANDI
            PC += 4
            rs = int(fetch[6:11], 2)
            rt = int(fetch[11:16], 2)
            imm = -(65536 - int(fetch[16:], 2)) if fetch[16] == '1' else int(fetch[16:], 2)

            rt = rs & imm

            #Jacob's Part

        #sltu
        elif fetch[0:6] == '000000' and fetch[26:32] == '101011':  # SLTU
            PC += 4
            rs = int(fetch[6:11], 2)
            rt = int(fetch[11:16], 2)
            rd = int(fetch[16:21], 2)

            if register[rs] < register[rt]:
                register[rd] = 1
            else:
                register[rd] = 0
           
        #lw            
        elif fetch[0:6] == '100011':  #LW
            PC += 4
            s = int(fetch[6:11], 2)
            t = int(fetch[11:16], 2)
            offset = -(65536 - int(fetch[16:], 2)) if fetch[16] == '1' else int(fetch[16:], 2)
            offset = offset + register[s]
            register[t] = mem[offset]

        #and
        elif fetch[0:6] == '000000' and fetch[26:32] == '100100':  #AND
            PC += 4
            rs = int(fetch[6:11], 2)
            rt = int(fetch[11:16], 2)
            rd = int(fetch[16:21], 2)

            register[rd] = register[rs] & register[rd]
        
        #sb
        elif fetch[0:6] == '101000':  #SB
            PC += 4
            rs = int(fetch[6:11], 2)
            rt = int(fetch[11:16], 2)
            offset = -(65536 - int(fetch[16:], 2)) if fetch[16] == '1' else int(fetch[16:], 2)
            offset = offset + register[rs]
            mem[offset] = register[rt]

        #lb
        elif fetch[0:6] == '100000':  #LB
            PC += 4
            rs = int(fetch[6:11], 2)
            rt = int(fetch[11:16], 2)
            offset = -(65536 - int(fetch[16:], 2)) if fetch[16] == '1' else int(fetch[16:], 2)
            offset = offset + register[rs]
            register[rt] = mem[offset]


        else:
            # This is not implemented on purpose
            PC = PC + 4
            print('Not implemented')

    # Finished simulations. Let's print out some stats
    print('***Simulation finished***')
    print('Registers $8 - $23 ', register[8:23])
    print('Dynamic Instr Count ', DIC)
    print('Memory contents 0x2000 - 0x2050 ', mem[8192:8272])

# Remember where each of the jump label is, and the target location
def saveJumpLabel(asm,labelIndex, labelName):
    lineCount = 0
    for line in asm:
        line = line.replace(" ","")
        if(line.count(":")):
            labelName.append(line[0:line.index(":")]) # append the label name
            labelIndex.append(lineCount) # append the label's index
            asm[lineCount] = line[line.index(":")+1:]
        lineCount += 1
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')


def main():
    # HW 4 part,Chris version
    #######################################################################################
    labelIndex = []
    labelName = []
    f = open("mc.txt", "w+")
    h = open("mips.asm", "r")
    asm = h.readlines()
    for item in range(asm.count('\n')):  # Remove all empty lines '\n'
        asm.remove('\n')

    saveJumpLabel(asm, labelIndex, labelName)  # Save all jump's destinations

    for line in asm:
        line = line.replace("\n", "")  # Removes extra chars
        line = line.replace("$", "")
        line = line.replace(" ", "")
        line = line.replace("zero", "0")  # assembly can also use both $zero and $0

        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        # ~ ~ ~ ~ ~ ~ ~ ~ GIVEN

        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        # ~ ~ ~ ~ ~ ~ ~ MY WORK

        # = = = = ADDIU = = = = = = = = (I)
        if (line[0:5] == "addiu"):
            line = line.replace("addiu", "")  # delete the addiu from the string.
            line = line.split(
                ",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.
            rt = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            rs = format(int(line[1]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            imm = format(int(line[2]), '016b') if (int(line[2]) > 0) else format(65536 + int(line[2]), '016b')
            f.write(str('001001') + str(rs) + str(rt) + str(imm) + '\n')

        # = = = = ADDI = = = = = = (I)
        elif (line[0:4] == "addi"):
            line = line.replace("addi", "")
            line = line.split(",")
            imm = format(int(line[2]), '016b') if (int(line[2]) > 0) else format(65536 + int(line[2]), '016b')
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            f.write(str('001000') + str(rs) + str(rt) + str(imm) + '\n')


        # = = = = ADD = = = = = = (R)
        elif (line[0:3] == "add"):
            line = line.replace("add", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            rs = format(int(line[1]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            rt = format(int(line[2]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000100000') + '\n')
            # the last part is actually accounting for sh = 00000 (5 zeroes)
            # and 6 bits for the func (0x20) = 100000

        # = = = = MULTU = = = = = = = = (R)
        elif (line[0:5] == "multu"):
            line = line.replace("multu", "")
            line = line.split(",")
            rs = format(int(line[0]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            rt = format(int(line[1]), '05b')  # make element 2 in the set, 'line' an int of 5 bits. (rt)
            f.write(str('000000') + str(rs) + str(rt) + str('00000') + str('00000') + str('011001') + '\n')


        # = = = = MULT = = = = = = = = (R)
        elif (line[0:4] == "mult"):
            line = line.replace("mult", "")
            line = line.split(",")
            rs = format(int(line[0]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            rt = format(int(line[1]), '05b')  # make element 2 in the set, 'line' an int of 5 bits. (rt)
            f.write(str('000000') + str(rs) + str(rt) + str('00000') + str('00000') + str('011000') + '\n')


        # = = = = SRL = = = = = = = = (R)
        elif (line[0:3] == "srl"):
            line = line.replace("srl", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            rt = format(int(line[1]), '05b')  # make element 2 in the set, 'line' an int of 5 bits. (rt)
            sh = format(int(line[2]), '05b')  # make element 3 in the set, 'line' an int of 5 bits. (sh)
            f.write(str('000000') + str('00000') + str(rt) + str(rd) + str(sh) + str('000010') + '\n')

            # question about splitting in python for the paranthesees?

        # = = = = LB = = = = = = = = = (I)
        elif (line[0:2] == "lb"):
            line = line.replace(")", "")  # remove the ) paran entirely.
            line = line.replace("(", ",")  # replace ( left paren with comma

            line = line.replace("lb", "")
            line = line.split(
                ",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.
            rt = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[2]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            f.write(str('100000') + str(rs) + str(rt) + str(imm) + '\n')


        # = = = = SB = = = = = = = = = (I)
        elif (line[0:2] == "sb"):
            line = line.replace(")", "")  # remove the ) paran entirely.
            line = line.replace("(", ",")  # replace ( left paren with comma

            line = line.replace("sb", "")
            line = line.split(
                ",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.

            rt = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[2]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            f.write(str('101000') + str(rs) + str(rt) + str(imm) + '\n')

        # = = = = LW = = = = = = = = = (I)
        elif (line[0:2] == "lw"):
            line = line.replace(")", "")  # remove the ) paran entirely.
            line = line.replace("(", ",")  # replace ( left paren with comma

            line = line.replace("lw", "")
            line = line.split(
                ",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.
            rt = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[2]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            f.write(str('100011') + str(rs) + str(rt) + str(imm) + '\n')

        # = = = = SW = = = = = = = = = (I)
        elif (line[0:2] == "sw"):
            line = line.replace(")", "")  # remove the ) paran entirely.
            line = line.replace("(", ",")  # replace ( left paren with comma

            line = line.replace("sw", "")
            line = line.split(
                ",")  # split the 1 string 'line' into a string array of many strings, broken at the comma.
            rt = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rt)
            imm = format(int(line[1]), '016b') if (int(line[1]) >= 0) else format(65536 + int(line[1]), '016b')
            rs = format(int(line[2]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            f.write(str('101011') + str(rs) + str(rt) + str(imm) + '\n')



        # = = = = BEQ = = = = = = = = = (I)
        elif (line[0:3] == "beq"):
            line = line.replace("beq", "")
            line = line.split(",")
            # print(line)
            rt = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            # imm = format(int(line[2]),'016b') if (int(line[2]) > 0) else format(65536 + int(line[2]),'016b')
            for i in range(len(labelName)):
                if (labelName[i] == line[0]):
                    f.write(str('000101') + str(rs) + str(rt) + str(format(int(labelIndex[i]), '016b')) + '\n')

            # f.write(str('000100') + str(rs) + str(rt) + str(imm) + '\n')


        # = = = = BNE = = = = = = = = = (I)
        elif (line[0:3] == "bne"):
            line = line.replace("bne", "")
            line = line.split(",")
            # print(line)
            rt = format(int(line[0]), '05b')
            rs = format(int(line[1]), '05b')
            # imm = format(int(line[2]),'016b') if (int(line[2]) > 0) else format(65536 + int(line[2]),'016b')
            for i in range(len(labelName)):
                if (labelName[i] == line[0]):
                    f.write(str('000101') + str(rs) + str(rt) + str(format(int(labelIndex[i]), '016b')) + '\n')

            # f.write(str('000101') + str(rs) + str(rt) + str(imm) + '\n')


        # = = = = SLTU = = = = = = = = = (R)
        elif (line[0:4] == "sltu"):
            line = line.replace("sltu", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            rs = format(int(line[1]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            rt = format(int(line[2]), '05b')  # make element 2 in the set, 'line' an int of 5 bits. (rt)

            for i in range(len(labelName)):
                if (labelName[i] == line[0]):
                    f.write(str('000101') + str(rs) + str(rt) + str(format(int(labelIndex[i]), '016b')) + '\n')

            # f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000') + str('101011') + '\n')


        # = = = = SLT = = = = = = = = = (R)
        elif (line[0:3] == "slt"):
            line = line.replace("slt", "")
            line = line.split(",")
            rd = format(int(line[0]), '05b')  # make element 0 in the set, 'line' an int of 5 bits. (rd)
            rs = format(int(line[1]), '05b')  # make element 1 in the set, 'line' an int of 5 bits. (rs)
            rt = format(int(line[2]), '05b')  # make element 2 in the set, 'line' an int of 5 bits. (rt)
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000') + str('101010') + '\n')


        # = = = = JUMP = = = = = = (J)

        elif (line[0:1] == "j"):
            line = line.replace("j", "")
            line = line.split(",")

            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location

            if (line[0].isdigit()):  # First,test to see if it's a label or a integer
                f.write(str('000010') + str(format(int(line[0]), '026b')) + '\n')

            else:  # Jumping to label
                for i in range(len(labelName)):
                    if (labelName[i] == line[0]):
                        f.write(str('000010') + str(format(int(labelIndex[i]), '026b')) + '\n')

    f.close()
    ########################################################################################
    file = open('mc.txt')
    program = []
    for line in file:

        if line.count('#'):
            line = list(line)
            line[line.index('#'):-1] = ''
            line = ''.join(line)
        if line[0] == '\n':
            continue
        line = line.replace('\n', '')
        instr = line[:]

        #instr = int(instr, 16)
        #instr = format(instr, '032b')
        program.append(instr)  # since PC increment by 4 every cycle,
        program.append(0)  # let's align the program code by every
        program.append(0)  # 4 lines
        program.append(0)

    # We SHALL start the simulation!
    sim(program)


if __name__ == '__main__':
    main()