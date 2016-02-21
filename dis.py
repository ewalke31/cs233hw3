# dis.py - Really simple disassembler for binary .scram files.
#
# Hacked by Peter H. Froehlich <phf@acm.org> for
# 600.333/433: Computer Systems Fundamentals, Fall 2012.
# Released into the public domain.
#
# Usage: python dis.py <input.scram

import sys

# the bit pattern for each SCRAM instruction
encoding = {
    "HLT": 0b0000, "LDA": 0b0001, "LDI": 0b0010,
    "STA": 0b0011, "STI": 0b0100, "ADD": 0b0101,
    "SUB": 0b0110, "JMP": 0b0111, "JMZ": 0b1000,
}

# reverse mapping from bit patterns to SCRAM instructions
decoding = dict([[v, k] for k, v in encoding.items()])

# size of main memory in bytes
SIZE = 16

# content of main memory, we load the binary program here
MEMORY = [0x00 for _ in range(SIZE)]


def upper(b):
    """Return upper four bits of byte b."""
    return (b >> 4) & 0x0f


def lower(b):
    """Return lower four bits of byte b."""
    return b & 0x0f


def disassemble(address):
    """Disassemble instruction at given address to stdout."""
    assert 0 <= address < SIZE

    inst = MEMORY[address]
    code = upper(inst)
    addr = lower(inst)

    if code in decoding:
        print "0x%02x: %s 0x%02x" % (address, decoding[code], addr)
    else:
        print "0x%02x: ??? [0x%02x]" % (address, inst)


def main():
    """Read binary program from stdin and disassemble to stdout."""
    binary = sys.stdin.read()

    if len(binary) > SIZE:
        print "Program too long, truncated from %d to %d bytes." % \
            (len(binary), SIZE)
        binary = binary[:SIZE]

    for i in range(len(binary)):
        MEMORY[i] = int(ord(binary[i])) & 0xff

    for i in range(len(binary)):
        disassemble(i)


if __name__ == "__main__":
    main()
