#Gabriel Groover (gtg3vv)
########## the PC and condition codes registers #############
register xF { 
    //pc:64 = 0;
    predPC:64 = 0;
}
register cC {
    SF:1 = 0;
    ZF:1 = 0;
};

########## Fetch #############
pc = [
    W_icode == RET : W_ValM;
    M_icode == JXX && !M_conditionsMet : M_ValP;
    1 : F_predPC;
    ];

f_icode = i10bytes[4..8];
f_ifun = i10bytes[0..4];
f_rA = i10bytes[12..16];
f_rB = i10bytes[8..12];

f_ValC = [
	f_icode in { JXX,CALL } : i10bytes[8..72];
	1 : i10bytes[16..80];
];

wire offset:64;
offset = [
	f_icode in { HALT, NOP, RET } : 1;
	f_icode in { RRMOVQ, OPQ, PUSHQ, POPQ } : 2;
	f_icode in {CALL,JXX} : 9;
	1 : 10;
];

f_ValP = pc + offset;
x_predPC = [
    f_icode in {JXX,CALL} : f_ValC;
    1 : f_ValP;
];

f_Stat = [
	f_icode == HALT : STAT_HLT;
	f_icode > 0xb : STAT_INS;
	1 : STAT_AOK;
];

########## Decode #############
register fD{
    Stat : 3 = STAT_BUB;
    icode : 4 = NOP;
    rA : 4 = REG_NONE;
    rB : 4 = REG_NONE;
    ifun : 4 = ALWAYS;
    ValC : 64 = 0;
    ValP : 64 = 0;
}

d_Stat = D_Stat;
d_icode = D_icode;
d_ifun = D_ifun;
d_ValC = D_ValC;
d_ValP = D_ValP;


#Detecting data load-use hazard
wire loadUse:1;
loadUse = (reg_srcA == e_dstM || reg_srcB == e_dstM) && (e_icode in {MRMOVQ,POPQ});

stall_F = loadUse || f_Stat != STAT_AOK || (D_icode == RET) || (f_icode == RET) || (E_icode == RET);
stall_D = loadUse;
bubble_E = loadUse || ((e_icode == JXX) && (!e_conditionsMet));
bubble_D = (e_icode == JXX && !e_conditionsMet) || (((D_icode == RET) || (M_icode == RET) || (E_icode == RET)) && !loadUse);


# source selection
reg_srcA = [
	D_icode in {OPQ,RRMOVQ,RMMOVQ,PUSHQ} : D_rA;
	D_icode in {POPQ,RET} : REG_RSP;
	1 : REG_NONE;
];
reg_srcB = [
    D_icode in {POPQ,PUSHQ,CALL,RET} : REG_RSP;
    D_icode in {OPQ,RMMOVQ,MRMOVQ} : D_rB;
    1 : REG_NONE;
    ];
# destination selection
d_dstE = [
	D_icode in {IRMOVQ, RRMOVQ, OPQ} : D_rB;
	D_icode in {PUSHQ,POPQ,CALL,RET} : REG_RSP;
	1 : REG_NONE;
];
d_dstM = [
    D_icode in {MRMOVQ,POPQ} : D_rA;
    1 : REG_NONE;
];

d_ValA = [
	e_dstE != REG_NONE && e_dstE == reg_srcA : e_ValE;
	reg_srcA != REG_NONE && reg_srcA == M_dstM : m_ValM;
	M_dstE != REG_NONE && M_dstE == reg_srcA : M_ValE;
	reg_srcA != REG_NONE && reg_srcA == W_dstM : W_ValM;
	W_dstE != REG_NONE && W_dstE == reg_srcA : W_ValE;
	1 : reg_outputA;
];
d_ValB = [
	e_dstE != REG_NONE && e_dstE == reg_srcB : e_ValE;
	reg_srcB != REG_NONE && reg_srcB == M_dstM : m_ValM;
	M_dstE != REG_NONE && M_dstE == reg_srcB : M_ValE;
	reg_srcB != REG_NONE && reg_srcB == W_dstM : W_ValM;
	W_dstE != REG_NONE && W_dstE == reg_srcB : W_ValE;
    1 : reg_outputB;
];

########## Execute #############
register dE{
    Stat : 3 = STAT_BUB;
    icode : 4 = NOP;
    ValA : 64 = 0;
    ValB : 64 = 0;
    ValC : 64 = 0;
    ValP : 64 = 0;
    ifun : 4 = ALWAYS;
    dstE : 4 = REG_NONE;
    dstM : 4 = REG_NONE;
    
}
e_Stat = E_Stat;
e_icode = E_icode;
e_ValA = E_ValA;
e_ValP = E_ValP;

e_dstE = [
    !e_conditionsMet && E_icode == CMOVXX : REG_NONE;
    1 : E_dstE;
    ];
e_dstM = E_dstM;

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
    Stat : 3 = STAT_BUB;
    icode : 4 = NOP;
    ValA : 64 = 0;
    ValE : 64 = 0;
    ValP : 64 = 0;
    dstE : 4 = REG_NONE;
    dstM : 4 = REG_NONE;
    conditionsMet : 1 = 0;
}

m_Stat = M_Stat;
m_icode = M_icode;
m_ValE = M_ValE;
m_dstE = M_dstE;
m_dstM = M_dstM;

mem_addr = [
    M_icode in {POPQ,RET} : M_ValA;
    1 : M_ValE;
   ];
mem_input = [
    M_icode == CALL : M_ValP;
    1 : M_ValA;
];
mem_writebit = [
    M_icode in {RMMOVQ,PUSHQ,CALL} : 1;
    1 : 0;
];
mem_readbit = [
    M_icode in {MRMOVQ,POPQ,RET} : 1;
    1 : 0;
];
m_ValM = mem_output;

########## Writeback #############
register mW{
    Stat : 3 = STAT_BUB;
    icode : 4 = NOP;
    ValE : 64 = 0;
    ValM : 64 = 0;
    dstE : 4 = REG_NONE;
    dstM : 4 = REG_NONE;
}

reg_dstE = [
    W_icode in {RRMOVQ,IRMOVQ,OPQ,PUSHQ,POPQ,CALL,RET} : W_dstE;
    1 : REG_NONE;
];

reg_dstM = W_dstM;

Stat = W_Stat;

reg_inputE = [ # unlike book, we handle the "forwarding" actions (something + 0) here
	W_icode in {IRMOVQ,OPQ,RRMOVQ,MRMOVQ,PUSHQ,POPQ,CALL,RET} : W_ValE;
];
reg_inputM = W_ValM;


########## PC and Status updates #############
