# An example file in our custom HCL variant, with lots of comments
#Gabriel Groover (gtg3vv)

register pP {  
    # our own internal register. P_pc is its output, p_pc is its input.
	pc:64 = 0; # 64-bits wide; 0 is its default value.
	
	# we could add other registers to the P register bank
	# register bank should be a lower-case letter and an upper-case letter, in that order.
	
	# there are also two other signals we can optionally use:
	# "bubble_P = true" resets every register in P to its default value
	# "stall_P = true" causes P_pc not to change, ignoring p_pc's value
} 

register cC {
    SF:1 = 0;
    ZF:1 = 0;
};

# we can define our own input/output "wires" of any number of 0<bits<=80
wire opcode:8, icode:4,ifun:4,regB:4,regA:4,valC:64,valE:64;
wire conditionsMet:1;

----------- Fetch -----------
# the x[i..j] means "just the bits between i and j".  x[0..1] is the 
# low-order bit, similar to what the c code "x&1" does; "x&7" is x[0..3]
opcode = i10bytes[0..8];   # first byte read from instruction memory
icode = opcode[4..8];      # top nibble of that byte
ifun = i10bytes[0..4];

# Stat is a built-in output; STAT_HLT means "stop", STAT_AOK means 
# "continue".  The following uses the mux syntax described in the 
# textbook
Stat = [
	icode == HALT : STAT_HLT;
	icode >= 0xb  : STAT_INS;
	1             : STAT_AOK;
];
----------- Decode -----------
valC = [
    icode == JXX : i10bytes[8..72];
    1 : i10bytes[16..80];
    ];
regB = i10bytes[8..12];
regA = i10bytes[12..16];
p_pc = [
    icode == RRMOVQ || icode == OPQ || icode == CMOVXX || icode == PUSHQ ||
    icode == POPQ : P_pc + 2;
    icode == IRMOVQ || icode == RMMOVQ || icode == MRMOVQ : P_pc + 10;
    icode == CALL : P_pc + 9;
    icode == JXX && conditionsMet: valC;
    1 : P_pc + 1;
];# you may use math ops directly...
----------- Execute -----------
valE = [
    icode == OPQ && ifun == ADDQ : reg_outputA + reg_outputB;
    icode == OPQ && ifun == SUBQ : reg_outputB - reg_outputA; 
    icode == OPQ && ifun == ANDQ : reg_outputA & reg_outputB; 
    icode == OPQ && ifun == XORQ : reg_outputA ^ reg_outputB;
    icode == RMMOVQ : reg_outputB + valC;
    1 : 0;
];
stall_C = (icode != OPQ);
c_ZF = (valE == 0);
c_SF = (valE >= 0x8000000000000000);

conditionsMet = [
    ifun == LE : C_SF || C_ZF;
    ifun == LT : C_SF;
    ifun == EQ : C_ZF;
    ifun == NE : !C_ZF;
    ifun == GE : !C_SF || C_ZF;
    ifun == GT : !C_SF;
    ifun == ALWAYS : 1;
    1 : 0;
];
----------- Memory -----------
mem_addr = valE;
mem_input = reg_outputA;
mem_writebit = [
    icode == RMMOVQ : 1;
    1 : 0;
];
mem_readbit = 0;

----------- Writeback -----------
reg_dstE = [
    !conditionsMet && icode == CMOVXX : REG_NONE;
    icode in {OPQ,IRMOVQ,RRMOVQ}: regB;
    1 : REG_NONE;
];
reg_srcA = regA;
reg_srcB = regB;
reg_inputE = [ 
    icode == RRMOVQ : reg_outputA;
    icode == IRMOVQ : valC;
    icode == OPQ : valE;
    1 : 0;
];
----------- PC Update -----------
# "pc" is a pre-defined input to the instruction memory and is the 
# address to fetch 6 bytes from (into pre-defined output "i10bytes").
pc = P_pc;