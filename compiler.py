# Abstract pokemon compiler

REG_DEFAULT = {0: 0, 1: 0x080a3f25, 2: None, 3: 0x03005e28, 4: 0x020383f0, 7: None}
MOV = 'Mov'
ADD = 'Add'
SUB = 'Sub'
STR = 'Str'
LDR = 'Ldr'
STRB = 'Strb'
LDRB = 'Ldrb'


class MemFix:  # Fix address to value
    def __init__(self, addr, value, l=1):
        self.addr, self.value, self.l = addr, value, l


class IndirectMemFix:  # Fix addr1->addr2+offset to value
    def __init__(self, addr, offset, value, l=1):
        self.addr, self.offset, self.value, self.l = addr, offset, value, l


class Instruction:
    pass


class AddSub(Instruction):  # THUMB 2
    def __init__(self, rd, rs, rn, op, imm=False):
        self.rd, self.rs, self.rn, self.op, self.imm = rd, rs, rn, op, imm

    def __repr__(self):
        return '{} r{},r{},{}{}'.format(self.op, self.rd, self.rs, '#' if self.imm else 'r', self.rn)

    def assemble(self):
        op = 0x1800
        op |= (1 << 9) if self.op == SUB else 0
        op |= (2 << 9) if self.imm else 0
        op |= abs(self.rn) << 6
        op |= self.rs << 3
        op |= self.rd
        return op


class Mov(Instruction):  # THUMB 3
    def __init__(self, rd, nn, op):
        self.rd, self.nn, self.op = rd, nn, op

    def __repr__(self):
        return '{} r{},#{}'.format(self.op, self.rd, self.nn)

    def assemble(self):
        op = 0x2000
        if self.op == ADD:
            op |= (2 << 11)
        elif self.op == SUB:
            op |= (3 << 11)
        op |= self.rd << 8
        op |= abs(self.nn)
        return op


class MemImm(Instruction):  # THUMB 9
    def __init__(self, rd, rb, nn, op):
        self.rd, self.rb, self.nn, self.op = rd, rb, nn, op

    def __repr__(self):
        return '{} r{},[r{},#{}]'.format(self.op, self.rd, self.rb, self.nn)

    def assemble(self):
        op = 0x6000
        if self.op == LDR:
            op |= (1 << 11)
        elif self.op == STRB:
            op |= (2 << 11)
        elif self.op == LDRB:
            op |= (3 << 11)
        op |= self.nn << 6
        op |= self.rb << 3
        op |= self.rd
        return op


class Branch(Instruction):  # THUMB 18
    def __init__(self, offset):
        self.offset = offset

    def assemble(self):
        op = 0xe000
        op |= self.offset & 0x7ff
        return op


def value_fix(reg, restrict, value, l=1):  # Set up a value
    fixes = []  # (dest, reg, instrs)
    for r, r_value in reg.items():
        if r == 7 and 0 <= value < 256 and r_value is None:  # Priority fix
            reg_p = reg.copy()
            reg_p[r] = value
            fixes.append((r, reg_p, []))
        if r_value is None or type(r_value) is str:
            continue
        diff = value - r_value
        if diff == 0:
            reg_p = reg.copy()
            fixes.append((r, reg_p, []))
        if r in restrict:  # Cannot change r
            continue
        # Mov fix
        if value < 256:
            reg_p = reg.copy()
            reg_p[r] = value
            fixes.append((r, reg_p, [Mov(r, value, MOV)]))
        if abs(diff) < 8:  # THUMB 2 difference
            reg_p = reg.copy()
            reg_p[r] = value
            op = ADD if diff > 0 else SUB
            fixes.append((r, reg_p, [AddSub(r, r, diff, op, imm=True)]))
        if abs(diff) < 256:  # THUMB 3 difference
            reg_p = reg.copy()
            reg_p[r] = value
            op = ADD if diff > 0 else SUB
            fixes.append((r, reg_p, [Mov(r, diff, op)]))
    return fixes


def store_fix(reg, restrict, rd, addr, l):  # Find a way to store rd in addr
    fixes = []  # (reg, instrs)
    for r, r_value in reg.items():
        if r_value is None:
            continue
        diff = addr-r_value
        if l == 1 and 0 <= diff < 32:
            fixes.append((reg, [MemImm(rd, r, diff, STRB)]))
        elif l == 4 and diff % 4 == 0 and 0 <= diff < 125:
            fixes.append((reg, [MemImm(rd, r, diff, STR)]))
        elif True:  # TODO: Halfword
            pass
        if r in restrict:
            continue
        if abs(diff) < 256:  # THUMB 3 difference
            reg_p = reg.copy()
            reg_p[r] = addr
            op = ADD if diff > 0 else SUB
            instrs = [Mov(r, diff, op)]
            if l == 1:
                instrs.append(MemImm(rd, r, 0, STRB))
            elif l == 4:
                instrs.append(MemImm(rd, r, 0, STR))
            fixes.append((reg_p, instrs))
    return fixes


def load_fix(reg, restrict, addr):
    v_fixes = value_fix(reg, restrict, addr, 4)
    l_fixes = []  # (r, reg, instrs)
    for rv, reg_p, v_instrs in v_fixes:  # For each value fix, pick a register to load it into
        for r2 in reg:
            if r2 not in restrict:
                reg_pp = reg_p.copy()
                reg_pp[r2] = 'UNKNOWN'
                l_fixes.append((r2, reg_pp, v_instrs + [MemImm(r2, rv, 0, LDR)]))
    return l_fixes


def poke_compile(*requests, num_args=None, priority=None, reg=None, restrict=None):
    if reg is None:
        reg = REG_DEFAULT.copy()
    if restrict is None:
        restrict = set()
    request = requests[0]
    if isinstance(request, MemFix):
        # Get the value into the registers
        # Get the address+- offset into the registers
        # Store
        v_fixes = value_fix(reg, restrict, request.value, request.l)  # First fix the value
        fixes = []
        for r, reg_p, instrs in v_fixes:  # For each value fix, fix the memory address
            m_fixes = store_fix(reg_p, restrict | {r}, r, request.addr, request.l)
            for reg_final, m_instrs in m_fixes:
                fixes.append((reg_final, instrs+m_instrs))
    elif isinstance(request, IndirectMemFix):
        # Get the load address into the registers
        # Get the value into the registers
        # Store
        fixes = []
        l_fixes = load_fix(reg, restrict, request.addr)
        for rl, reg_l, l_instrs in l_fixes:
            v_fixes = value_fix(reg_l, restrict | {rl}, request.value, request.l)
            for rv, reg_v, v_instrs in v_fixes:
                #print(rv, l_instrs, v_instrs)
                if request.l == 1 and 0 <= request.offset < 32:
                    s_instrs = [MemImm(rv, rl, request.offset, STRB)]
                elif request.l == 4 and request.offset % 4 == 0 and 0 <= request.offset < 125:
                    s_instrs = [MemImm(rv, rl, request.offset, STR)]
                fixes.append((reg_v, l_instrs+v_instrs+s_instrs))


if __name__ == '__main__':
    poke_compile(IndirectMemFix(0x03005d8c, 4, 0x10))
