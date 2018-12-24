# -*-sh-*- # this line enables partial syntax highlighting in emacs

######### The PC #############
register xF { pc:64 = 0; }


########## Fetch #############
########## Fetch #############
pc = F_pc;

wire icode:4, ifun:4, rA:4, rB:4, valC:64;

icode = i10bytes[4..8];
ifun = i10bytes[0..4];
rA = i10bytes[12..16];
rB = i10bytes[8..12];

valC = [
	icode in { JXX } : i10bytes[8..72];
	1 : i10bytes[16..80];
];

wire offset:64, valP:64;
offset = [
	icode in { HALT, NOP, RET } : 1;
	icode in { RRMOVQ, OPQ, PUSHQ, POPQ } : 2;
	icode in { JXX, CALL } : 9;
	1 : 10;
];
valP = F_pc + offset;

########## Decode #############

reg_srcA = [
	icode in {RMMOVQ} : rA;
	1 : REG_NONE;
];
reg_srcB = [
	icode in {RMMOVQ, MRMOVQ} : rB;
	1 : REG_NONE;
];


########## Execute #############

wire operand1:64, operand2:64;

operand1 = [
	icode in { MRMOVQ, RMMOVQ } : valC;
	1: 0;
];
operand2 = [
	icode in { MRMOVQ, RMMOVQ } : reg_outputB;
	1: 0;
];

wire valE:64;

valE = [
	icode in { MRMOVQ, RMMOVQ } : operand1 + operand2;
	1 : 0;
];



########## Memory #############

mem_readbit = icode in { MRMOVQ };
mem_writebit = icode in { RMMOVQ };
mem_addr = [
	icode in { MRMOVQ, RMMOVQ } : valE;
];
mem_input = [
	icode in { RMMOVQ } : reg_outputA;
];

########## Writeback #############

reg_dstM = [ 
	icode in {MRMOVQ} : rA;
	1: REG_NONE;
];
reg_inputM = [
	icode in {MRMOVQ} : mem_output;
];


Stat = [
	icode == HALT : STAT_HLT;
	icode > 0xb : STAT_INS;
	x_pc > 0xfff : STAT_ADR;
	1 : STAT_AOK;
];

x_pc = valP;



