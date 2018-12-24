#Gabriel Groover (gtg3vv)
########## the PC and condition codes registers #############
register xF { pc:64 = 0; }
register cC {
    SF:1 = 0;
    ZF:1 = 0;
};

########## Fetch #############
pc = F_pc;

f_icode = i10bytes[4..8];
f_ifun = i10bytes[0..4];
f_rA = i10bytes[12..16];
f_rB = i10bytes[8..12];

f_ValC = [
	f_icode in { JXX } : i10bytes[8..72];
	1 : i10bytes[16..80];
];

wire offset:64,valP:64;
offset = [
	f_icode in { HALT, NOP, RET } : 1;
	f_icode in { RRMOVQ, OPQ, PUSHQ, POPQ } : 2;
	f_icode in { JXX, CALL } : 9;
	1 : 10;
];

valP = F_pc + offset;

f_Stat = [
	f_icode == HALT : STAT_HLT;
	f_icode > 0xb : STAT_INS;
	1 : STAT_AOK;
];

stall_F = [
	f_Stat in {STAT_HLT,STAT_INS} : 1;
	1 : 0;
	];
########## Decode #############
register fD{
    Stat : 3 = STAT_AOK;
    icode : 4 = NOP;
    rA : 4 = REG_NONE;
    rB : 4 = REG_NONE;
    ifun : 4 = ALWAYS;
    ValC : 64 = 0;
}

d_Stat = D_Stat;
d_icode = D_icode;
d_ifun = D_ifun;
d_ValC = D_ValC;

# source selection
reg_srcA = [
	D_icode in {OPQ,RRMOVQ} : D_rA;
	1 : REG_NONE;
];
reg_srcB = [
    D_icode in {POPQ,PUSHQ,CALL,RET} : REG_RSP;
    1 : D_rB;
    ];
# destination selection
d_dstE = [
	D_icode in {IRMOVQ, RRMOVQ,OPQ} : D_rB;
	1 : REG_NONE;
];

d_ValA = [
	reg_dstE != REG_NONE && reg_dstE == reg_srcA : reg_inputE;
	m_dstE != REG_NONE && m_dstE == reg_srcA : m_ValE;
	e_dstE != REG_NONE && e_dstE == reg_srcA : e_ValE;
	1 : reg_outputA;
];
d_ValB = [
	reg_dstE != REG_NONE && reg_dstE == reg_srcB : reg_inputE;
	m_dstE != REG_NONE && m_dstE == reg_srcB : m_ValE;
	e_dstE != REG_NONE && e_dstE == reg_srcB : e_ValE;
    1 : reg_outputB;
];

########## Execute #############
register dE{
    Stat : 3 = STAT_AOK;
    icode : 4 = NOP;
    ValA : 64 = 0;
    ValB : 64 = 0;
    ValC : 64 = 0;
    ifun : 4 = ALWAYS;
    dstE : 4 = REG_NONE;
    
}
e_Stat = E_Stat;
e_icode = E_icode;
e_ValA = E_ValA;
e_dstE = [
    !e_conditionsMet && E_icode == CMOVXX : REG_NONE;
    1 : E_dstE;
    ];

e_ValE = [
    E_icode == OPQ && E_ifun == ADDQ : E_ValA + E_ValB;
    E_icode == OPQ && E_ifun == SUBQ : E_ValB - E_ValA; 
    E_icode == OPQ && E_ifun == ANDQ :E_ValA & E_ValB; 
    E_icode == OPQ && E_ifun == XORQ : E_ValA ^ E_ValB;
    E_icode in {RMMOVQ,MRMOVQ} : E_ValB + E_ValC;
    E_icode in {PUSHQ,CALL} : E_ValB - 8;
    E_icode in {POPQ,RET} : E_ValB + 8;
    E_icode in {IRMOVQ} : E_ValC;
    E_icode in {RRMOVQ} : E_ValA;
    1 : 0;
];
stall_C = (E_icode != OPQ);
c_ZF = (e_ValE == 0);
c_SF = (e_ValE >= 0x8000000000000000);

e_conditionsMet = [
    E_ifun == LE : C_SF || C_ZF;
    E_ifun == LT : C_SF;
    E_ifun == EQ : C_ZF;
    E_ifun == NE : !C_ZF;
    E_ifun == GE : !C_SF || C_ZF;
    E_ifun == GT : !C_SF;
    E_ifun == ALWAYS : 1;
    1 : 0;
];

########## Memory #############
register eM{
    Stat : 3 = STAT_AOK;
    icode : 4 = NOP;
    ValA : 64 = 0;
    ValE : 64 = 0;
    dstE : 4 = REG_NONE;
    conditionsMet : 1 = 0;
}

m_Stat = M_Stat;
m_icode = M_icode;
m_ValE = M_ValE;
m_dstE = M_dstE;


########## Writeback #############
register mW {
    Stat : 3 = STAT_AOK;
    icode : 4 = NOP;
    ValE : 64 = 0;
    dstE : 4 = REG_NONE;
    
}




reg_dstE = W_dstE;
Stat = W_Stat;
reg_inputE = [ # unlike book, we handle the "forwarding" actions (something + 0) here
	W_icode == RRMOVQ : W_ValE;
	W_icode in {IRMOVQ,OPQ} : W_ValE;
];


########## PC and Status updates #############



x_pc = valP;