#Gabriel Groover (gtg3vv)
########## the PC and condition codes registers #############
register xF { pc:64 = 0; }


########## Fetch #############
pc = F_pc;

wire ifun:4, rA:4, rB:4;

d_icode = i10bytes[4..8];
ifun = i10bytes[0..4];
rA = i10bytes[12..16];
rB = i10bytes[8..12];

d_valC = [
	d_icode in { JXX } : i10bytes[8..72];
	1 : i10bytes[16..80];
];

wire offset:64,valP:64;
offset = [
	d_icode in { HALT, NOP, RET } : 1;
	d_icode in { RRMOVQ, OPQ, PUSHQ, POPQ } : 2;
	d_icode in { JXX, CALL } : 9;
	1 : 10;
];
valP = F_pc + offset;

d_Stat = [
	d_icode == HALT : STAT_HLT;
	d_icode > 0xb : STAT_INS;
	1 : STAT_AOK;
];

stall_F = [
	d_Stat in {STAT_HLT,STAT_INS} : 1;
	1 : 0;
	];
########## Decode #############

# source selection
reg_srcA = [
	d_icode in {RRMOVQ} : rA;
	1 : REG_NONE;
];

d_reg_outputA = [
	reg_dstE != REG_NONE && reg_dstE == reg_srcA : reg_inputE;
	1 : reg_outputA;
];

# destination selection
d_reg_dstE = [
	d_icode in {IRMOVQ, RRMOVQ} : rB;
	1 : REG_NONE;
];
########## Execute #############



########## Memory #############




########## Writeback #############
register dW {
    # todo: fill in the details here
	icode : 4 = NOP;
	reg_outputA : 64 = 0;
	valC : 64 = 0; 
	Stat : 3 = STAT_AOK;
	reg_dstE : 4 = REG_NONE;
}

reg_dstE = W_reg_dstE;
Stat = W_Stat;
reg_inputE = [ # unlike book, we handle the "forwarding" actions (something + 0) here
	W_icode == RRMOVQ : W_reg_outputA;
	W_icode in {IRMOVQ} : W_valC;
];


########## PC and Status updates #############



x_pc = valP;



