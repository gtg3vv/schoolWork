// auto-generated HCL2 simulator; DO NOT EDIT THIS FILE
/+++++++++++++++++ generated from the following HCL: ++++++++++++++++++
###################### begin builtin signals ##########################

### constants:

const STAT_BUB = 0b000, STAT_AOK = 0b001, STAT_HLT = 0b010;  # expected behavior
const STAT_ADR = 0b011, STAT_INS = 0b100, STAT_PIP = 0b110;  # error conditions

const REG_RAX = 0b0000, REG_RCX = 0b0001, REG_RDX = 0b0010, REG_RBX = 0b0011;
const REG_RSP = 0b0100, REG_RBP = 0b0101, REG_RSI = 0b0110, REG_RDI = 0b0111;
const REG_R8  = 0b1000, REG_R9  = 0b1001, REG_R10 = 0b1010, REG_R11 = 0b1011;
const REG_R12 = 0b1100, REG_R13 = 0b1101, REG_R14 = 0b1110, REG_NONE= 0b1111;

# icodes; see figure 4.2
const HALT   = 0b0000, NOP    = 0b0001, RRMOVQ = 0b0010, IRMOVQ = 0b0011;
const RMMOVQ = 0b0100, MRMOVQ = 0b0101, OPQ    = 0b0110, JXX    = 0b0111;
const CALL   = 0b1000, RET    = 0b1001, PUSHQ  = 0b1010, POPQ   = 0b1011;
const CMOVXX = RRMOVQ;

# ifuns; see figure 4.3
const ALWAYS = 0b0000, LE   = 0b0001, LT   = 0b0010, EQ   = 0b0011;
const NE     = 0b0100, GE   = 0b0101, GT   = 0b0110;
const ADDQ   = 0b0000, SUBQ = 0b0001, ANDQ = 0b0010, XORQ = 0b0011;


### fixed-functionality inputs (things you should assign to in your HCL)

wire Stat:3;              # should be one of the STAT_... constants
wire pc:64;               # put the address of the next instruction into this

wire reg_srcA:4, reg_srcB:4;        # use to pick which program registers to read from
wire reg_dstE:4, reg_dstM:4;        # use to pick which program registers to write to
wire reg_inputE:64, reg_inputM:64;  # use to provide values to write to program registers

wire mem_writebit:1, mem_readbit:1; # set at most one of these two to 1 to access memory
wire mem_addr:64;                   # if accessing memory, put the address accessed here
wire mem_input:64;                  # if writing to memory, put the value to write here

### fixed-functionality outputs (things you should use but not assign to)

wire i10bytes:80;                     # output value of instruction read; linked to pc
wire reg_outputA:64, reg_outputB:64;  # values from registers; linked to reg_srcA and reg_srcB
wire mem_output:64;                   # value read from memory; linked to mem_readbit and mem_addr

####################### end builtin signals ###########################

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
++++++++++++++++++ generated from the preceeding HCL ++++++++++++++++++/




/////////////////////// int type bigger than long ///////////////////
private template negOneList(uint length) {
	static if (length == 1) enum negOneList = "-1";
	else enum negOneList = negOneList!(length-1)~", -1";
}

struct bvec(uint bits) if (bits != 0) {
	static enum words = (bits+31)/32;
	static enum min = bvec.init;
	mixin("static enum max = bvec(["~negOneList!words~"]);");
	uint[words] data;
	ubyte *data_bytes() { return cast(ubyte*)&(this.data[0]); }

	this(uint x) { data[0] = x; truncate; }
	this(ulong x) { data[0] = cast(uint)x; static if (words > 1) data[1] = cast(uint)(x>>32); truncate; }
	this(uint[] dat) { this.data[] = dat[]; truncate; }
	this(uint o)(bvec!o x) if (o < bits) { data[0..x.words] = x.data[]; truncate; }
	this(uint o)(bvec!o x) if (o > bits) { data[] = x.data[0..words]; truncate; }
	
	ref bvec opAssign(uint x) { data[0] = x; static if(words > 1) data[1..$] = 0; return truncate; }
	ref bvec opAssign(ulong x) { data[0] = cast(uint)x; static if (words > 1) data[1] = cast(uint)(x>>32); static if(words > 2) data[2..$] = 0; return truncate; }
	ref bvec opAssign(uint[] dat) { this.data[] = dat[]; return truncate; }
	ref bvec opAssign(uint o)(bvec!o x) if (o < bits) { data[0..x.words] = x.data[]; static if (x.words < words) data[x.words..$] = 0; return truncate; }
	ref bvec opAssign(uint o)(bvec!o x) if (o > bits) { data[] = x.data[0..words]; return truncate; }

	ref bvec truncate() {
		static if ((bits&31) != 0) {
			data[$-1] &= 0xffffffffU >> (32-(bits&31));
		}
		return this;
	}
	bvec!(bits+b1) cat(uint b2)(bvec!b2 other) {
		bvec!(bits+b1) ans;
		foreach(i,v; data) ans.data[i] = v;
		static if ((bits&31) == 0) {
			foreach(i,v; other.data) ans.data[i+words] = v;
		} else {
			foreach(i,v; other.data) {
				ans.data[i+words-1] |= (v<<(bits&31));
				if (i+words < ans.words) ans.data[i+words] = (v>>(32-(bits&31)));
			}
		}
		return ans;
	}
	bvec!(e-s) slice(uint s, uint e)() if (s <= e && e <= bits) {
		bvec!(e-s) ans;
		static if ((s&31) == 0) {
			ans.data[] = data[s/32 .. s/32+ans.words];
		} else {
			foreach(i; s/32..((e-s)+31)/32) {
				ans.data[i-s/32] = data[i]>>(s&31);
				if(i > s/32) ans.data[i-s/32-1] |= data[i]<<(32-(s&31));
			}
		}
		return ans.truncate;
	}
	string hex() {
		import std.format, std.range;
		static if (words > 0) {
			return format("%0"~format("%d",((bits&31)+3)/4)~"x%(%08x%)", data[$-1], retro(data[0..$-1]));
		} else {
			return format("%0"~format("%d",(bits+3)/4)~"x", data[0]);
		}
	}
	string smallhex() {
		auto ans = hex;
		while (ans.length > 1 && ans[0] == '0') ans = ans[1..$];
		return ans;
	}
	version (BigEndian) {
		pragma(msg, "hexbytes not implemented on big endian hardware");
	} else {
		string hexbytes() {
			import std.format;
			return format("%(%02x%| %)", data_bytes[0..((bits+7)/8)]);
		}
	}
	string toString() {
		return "0x"~smallhex;
	}
	string bin() {
		import std.format, std.range;
		ubyte[words*4] tmp = *(cast(ubyte[words*4]*)&data);
		static if (bits <= 8) {
			return format("%0"~format("%d",bits)~"b", tmp[0]);
		} else static if ((bits&7) != 0) {
			return format("%0"~format("%d",bits&7)~"b_%(%08b%|_%)", tmp[(bits-1)/8], retro(tmp[0..(bits-1)/8]));
		} else {
			return format("%(%08b%|_%)", retro(tmp[0..bits/8]));
		} 
	}
	static bvec hex(string s)
	in {
		assert(s.length <= (bits+3)/4, "too many hex digits for this type");
		foreach(c; s) assert((c >= '0' && c <= '9') || (c >= 'A' && c <= 'F') || (c >= 'a' && c <= 'f'), "expected a raw hex string");
		if (s.length > bits/4) assert(s[0]-'0' < (1<<(bits&3)), "most-significant digit too big for this type");
	} body {
		uint place = 0, shift = 0;
		bvec ans;
		foreach_reverse(c; s) {
			uint val = c - (c < 'Z' ? c < 'A' ? '0' : 'A'-10 : 'a'-10);
			ans.data[place] |= shift ? val<<shift : val;
			shift += 4;
			place += shift>=32;
			shift &= 31;
		}
		return ans; // no need to truncate; the in conditions take care of that
	}
	
	bool getBit(uint i) pure nothrow {
		return i >= bits ? false 
			: ((0==(i&31)) ? data[i/32]&1 : data[i/32]&(1<<(i&31))) != 0; 
	}
	
	ref bvec setBit(uint i, bool v) pure nothrow
	in { assert(i < bits, "illegal bit index"); }
	body { 
		if (v) if (0==(i&31)) data[i/32]|=1;
		       else           data[i/32]|=(1<<(i&31));
		else if (0==(i&31)) data[i/32]&=~1;
		     else           data[i/32]&=~(1<<(i&31));
		return this;
	}
	
	int opCmp(T)(T x) if (is(T : uint)) {
		foreach(i; 1..data.length) if (data[i] != 0) return 1;
		return data[0] < x ? -1 : data[0] == x ? 0 : 1;
	}
	int opCmp(uint b2)(bvec!b2 x) {
		static if (x.words == words) {
			foreach_reverse(i; 0..x.words) if (data[i] != x.data[i]) return data[i] < x.data[i] ? -1 : 1;
			return 0;
		} else static if (x.words < words) {
			foreach(i; x.words..words) if (data[i] != 0) return 1;
			foreach_reverse(i; 0..x.words) if (data[i] != x.data[i]) return data[i] < x.data[i] ? -1 : 1;
			return 0;
		} else {
			foreach(i; words..x.words) if (x.data[i] != 0) return -1;
			foreach_reverse(i; 0..words) if (data[i] != x.data[i]) return data[i] < x.data[i] ? -1 : 1;
			return 0;
		}
	}
	bool opEquals(T)(T x) { return this.opCmp(x) == 0; }
	T opCast(T)() if (is(T == bool)) { return opCmp!uint(0) != 0; }
	T opCast(T)() if (is(T == ulong)) { 
		static if (words > 1) return ((cast(ulong)data[1])<<32) | data[0];
		return data[0];
	}
	T opCast(T)() if (is(T == uint)) { return data[0]; }
	
	ref bvec opOpAssign(string op)(bvec s) pure nothrow if (op == "<<" || op == ">>") {
		if (s >= bits) data[] = 0;
		return this.opOpAssign!s(data[0]);
	}
	ref bvec opOpAssign(string op)(ulong s) pure nothrow if (op == "<<" || op == ">>") {
		return opOpAssign!op(cast(uint)s);
	}
	ref bvec opOpAssign(string op)(uint s) pure nothrow if (op == "<<") {
		if (s >= bits) data[] = 0;
		else {
			if (s >= 32) {
				auto ds = s/32;
				s &= 31;
				data[ds..$] = data[0..$-ds].dup;
				data[0..ds] = 0;
			}
			if (s != 0)
				foreach_reverse(i; 0..words)
					data[i] = (data[i]<<s) | (i > 0 ? data[i-1]>>(32-s) : 0);
		}
		return this.truncate;
	}
	ref bvec opOpAssign(string op)(uint s) pure nothrow if (op == ">>") {
		if (s >= bits) data[] = 0;
		else {
			if (s >= 32) {
				auto ds = s/32;
				s &= 31;
				data[0..$-ds] = data[ds..$].dup;
				data[$-ds..$] = 0;
			}
			if (s != 0)
				foreach(i; 0..words)
					data[i] = (data[i]>>s) | (i+1 < data.length ? data[i+1]<<(32-s) : 0);
		}
		return this.truncate;
	}
	ref bvec opOpAssign(string op)(bvec x) pure nothrow if (op == "&" || op == "|" || op == "^") {
		foreach(i,ref v; this.data) mixin("v "~op~"= x.data[i];");
		return this.truncate;
	}
	ref bvec opOpAssign(string s)(bvec x) pure nothrow if (s == "+" || s == "-") {
		ulong carry = s == "+" ? 0 : 1;
		foreach(i, ref v; data) {
			carry += v;
			carry += s == "+" ? x.data[i] : ~x.data[i];
			v = cast(uint)carry;
			carry >>= 32;
		}
		return this.truncate;
	}
	ref bvec opOpAssign(string op)(bvec x) pure nothrow if (op == "*") {
		bvec ans;
		ulong carry = 0;
		foreach(digit; 0..words) {
			ulong accum = carry&uint.max;
			carry >>= 32;
			foreach(i; 0..digit+1) {
				ulong tmp = data[i] * cast(ulong)x.data[digit-i];
				accum += tmp&uint.max;
				carry += tmp>>32;
			}
			ans.data[digit] = cast(uint)accum;
			carry += accum>>32;
		}
		this.data[] = ans.data[];
		return this.truncate;
	}
	ref bvec opOpAssign(string s)(bvec div) pure nothrow if (s == "/" || s == "%") {
		import std.stdio;
		bvec rem = this;
		bvec num;
		uint place = 0;
		while (div < rem && !div.getBit(bits-1)) { place += 1; div <<= 1; }
		while (true) {
			if (rem >= div) {
				num.setBit(place, true);
				rem -= div;
			}
			if (place == 0) break;
			div >>= 1;
			place -= 1;
		}
		static if (s == "/") this.data[] = num.data[];
		else this.data[] = rem.data[];
		return this;
	}
	ref bvec opOpAssign(string s)(ulong x) pure nothrow if (s != "<<" && s != ">>") {
		return this.opOpAssign!s(bvec(x));
	}
	ref bvec opOpAssign(string s)(uint x) pure nothrow if (s != "<<" && s != ">>") {
		return this.opOpAssign!s(bvec(x));
	}

	bvec opUnary(string s)() pure nothrow if (s == "~") {
		bvec ans = this;
		foreach(i,ref v; ans.data) v ^= max.data[i];
		return ans;
	}
	bvec opUnary(string s)() pure nothrow if (s == "-") { bvec ans; ans -= this; return ans; }

	bvec opBinary(string op, T)(T x) if (__traits(compiles, this.opOpAssign!op(x))) {
		bvec ans = this; return ans.opOpAssign!op(x);
	}
}
unittest { bvec!10 x = [-1]; assert(x.data[0] == 0x3ff,"expected 0x3ff"); }
unittest { bvec!40 x = [-1,-1]; assert(x.data == [0xffffffffU,0xffu]); }
unittest { bvec!64 x = [-1,-1]; assert(x.data == [0xffffffffU,0xffffffffu]); }
unittest { 
	bvec!35 x = [0x40000000,0x2]; 
	assert((x>>1).data == [0x20000000,0x1]); 
	assert((x<<1).data == [0x80000000,0x4]); 
	assert((x<<2).data == [0x00000000,0x1]); 
}
unittest { 
	bvec!128 x = [0x4,0x40000000,0x2, 0x4]; 
	assert((x<<33).data == [0,0x8,0x80000000,0x4]); 
	assert((x>>33).data == [0x20000000,0x1,0x2,0]); 
}alias bvec!80 ulonger;


/////////////////////////// register file ///////////////////////////
ulong[15] __regfile = [0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0];

////////////////////////////// memory ///////////////////////////////
ubyte[ulong] __memory;
bool __can_read_imem(ulong mem_addr) { return mem_addr < ulong.max-10; }
bool __can_read_dmem(ulong mem_addr) { return mem_addr < ulong.max-8; }
bool __can_write_dmem(ulong mem_addr) { return mem_addr < ulong.max-8; }
ubyte[] __read_bytes(ulong baseAddr, uint bytes) {
    ubyte[] ans = new ubyte[bytes];
    foreach_reverse(i; 0..bytes) {
        if ((baseAddr + i) in __memory) ans[i] = __memory[baseAddr+i];
        else ans[i] = 0;
    }
    return ans;
}
ulong __asUlong(ubyte[] arg) {
    ulong ans = 0;
    foreach_reverse(i; 0..8) if (i < arg.length) {
        ans <<= 8;
        ans |= arg[i];
    }
    return ans;
}
ulonger __asUlonger(ubyte[] arg) {
    ulonger ans = 0;
    foreach_reverse(i; 0..10) if (i < arg.length) {
        ans <<= 8;
        ans |= arg[i];
    }
    return ans;
}
void __write_bytes(ulong baseAddr, ulong value, uint bytes) {
    foreach(i; 0..bytes) {
        __memory[baseAddr+i] = cast(ubyte)value;
        value >>= 8;
    }
}
ulonger __read_imem(ulong mem_addr) { return __asUlonger(__read_bytes(mem_addr, 10)); }
ulong __read_dmem(ulong mem_addr) { return __asUlong(__read_bytes(mem_addr, 8)); }
void __write_dmem(ulong mem_addr, ulong value) { __write_bytes(mem_addr, value, 8); }

//////////////// pipeline registers' initial values ////////////////
// register bank D:
bool _HCL_bubble_D = false;
bool _HCL_stall_D  = false;
ulong _HCL_D_Stat = 1;
ulong _HCL_D_rB = 15;
ulong _HCL_D_icode = 1;
ulong _HCL_D_ifun = 0;
ulong _HCL_D_ValC = 0;
ulong _HCL_D_rA = 15;
// register bank W:
bool _HCL_bubble_W = false;
bool _HCL_stall_W  = false;
ulong _HCL_W_Stat = 1;
ulong _HCL_W_ValE = 0;
ulong _HCL_W_icode = 1;
ulong _HCL_W_dstE = 15;
// register bank M:
bool _HCL_bubble_M = false;
bool _HCL_stall_M  = false;
ulong _HCL_M_Stat = 1;
ulong _HCL_M_ValE = 0;
ulong _HCL_M_icode = 1;
ulong _HCL_M_conditionsMet = 0;
ulong _HCL_M_ValA = 0;
ulong _HCL_M_dstE = 15;
// register bank F:
bool _HCL_bubble_F = false;
bool _HCL_stall_F  = false;
ulong _HCL_F_pc = 0;
// register bank E:
bool _HCL_bubble_E = false;
bool _HCL_stall_E  = false;
ulong _HCL_E_Stat = 1;
ulong _HCL_E_ValB = 0;
ulong _HCL_E_ifun = 0;
ulong _HCL_E_dstE = 15;
ulong _HCL_E_ValC = 0;
ulong _HCL_E_icode = 1;
ulong _HCL_E_ValA = 0;
// register bank C:
bool _HCL_bubble_C = false;
bool _HCL_stall_C  = false;
ulong _HCL_C_ZF = 0;
ulong _HCL_C_SF = 0;

////////////////////////// disassembler /////////////////////////////

enum RNAMES = [ "%rax", "%rcx", "%rdx", "%rbx", "%rsp", "%rbp", "%rsi", "%rdi",
"%r8", "%r9", "%r10", "%r11", "%r12", "%r13", "%r14", "none"];
enum OPNAMES = [ "addq", "subq", "andq", "xorq", "op4", "op5", "op6", "op7",
"op8", "op9", "op10", "op11", "op12", "op13", "op14", "op15"];
enum JMPNAMES = [ "jmp", "jle", "jl", "je", "jne", "jge", "jg", "jXX",
"jXX", "jXX", "jXX", "jXX", "jXX", "jXX", "jXX", "jXX"];
enum RRMOVQNAMES = [ "rrmovq", "cmovle", "cmovl", "cmove", "cmovne", "cmovge", "cmovg", "cmovXX",
"cmovXX", "cmovXX", "cmovXX", "cmovXX", "cmovXX", "cmovXX", "cmovXX", "cmovXX"];
string disas(ulonger i10bytes) {
    auto b = i10bytes.data_bytes;
    auto s = i10bytes.hexbytes;
    switch((i10bytes.data[0]&0xf0)>>4) {
        case 0 : return s[0..3*1-1]~" : halt";
        case 1 : return s[0..3*1-1]~" : nop";
        case 2 : return s[0..3*2-1]~" : "~RRMOVQNAMES[b[0]&0xf]~" "~RNAMES[(b[1]>>4)&0xf]~", "~RNAMES[b[1]&0xf];
        case 3 : return s[0..3*10-1]~" : irmovq $0x"~(i10bytes.slice!(16,80).smallhex)~", "~RNAMES[b[1]&0xf];
        case 4 : return s[0..3*10-1]~" : rmmovq "~RNAMES[(b[1]>>4)&0xf]~", 0x"~(i10bytes.slice!(16,80).smallhex)~"("~RNAMES[b[1]&0xf]~")";
        case 5 : return s[0..3*10-1]~" : mrmovq 0x"~(i10bytes.slice!(16,80).smallhex)~"("~RNAMES[b[1]&0xf]~"), "~RNAMES[(b[1]>>4)&0xf];
        case 6 : return s[0..3*2-1]~" : "~OPNAMES[b[0]&0xf]~" "~RNAMES[(b[1]>>4)&0xf]~", "~RNAMES[b[1]&0xf];
        case 7 : return s[0..3*9-1]~" : "~JMPNAMES[b[0]&0xf]~" 0x"~(i10bytes.slice!(8,72).smallhex);
        case 8 : return s[0..3*9-1]~" : call  0x"~(i10bytes.slice!(8,72).smallhex);
        case 9 : return s[0..3*1-1]~" : ret";
        case 10 : return s[0..3*2-1]~" : pushq "~RNAMES[(b[1]>>4)&0xf];
        case 11 : return s[0..3*2-1]~" : popq "~RNAMES[(b[1]>>4)&0xf];
        default: return "unknown operation";
    }
}

////////////////////////// update cycle /////////////////////////////
int tick(bool showpc=true, bool showall=false) {
    ulong _HCL_pc = _HCL_F_pc;
    _HCL_pc &= 0xffffffffffffffff;
    if (showall) writefln("set pc to 0x%x",_HCL_pc);
    ulong _HCL_d_Stat = _HCL_D_Stat;
    _HCL_d_Stat &= 0x7;
    if (showall) writefln("set d_Stat to 0x%x",_HCL_d_Stat);
    ulong _HCL_d_icode = _HCL_D_icode;
    _HCL_d_icode &= 0xf;
    if (showall) writefln("set d_icode to 0x%x",_HCL_d_icode);
    ulong _HCL_d_ifun = _HCL_D_ifun;
    _HCL_d_ifun &= 0xf;
    if (showall) writefln("set d_ifun to 0x%x",_HCL_d_ifun);
    ulong _HCL_d_ValC = _HCL_D_ValC;
    _HCL_d_ValC &= 0xffffffffffffffff;
    if (showall) writefln("set d_ValC to 0x%x",_HCL_d_ValC);
    ulong _HCL_reg_srcA = (((((_HCL_D_icode)==(6)))||(((_HCL_D_icode)==(2)))) ? (_HCL_D_rA) :
		(15));
    _HCL_reg_srcA &= 0xf;
    if (showall) writefln("set reg_srcA to 0x%x",_HCL_reg_srcA);
    ulong _HCL_reg_srcB = (((((((_HCL_D_icode)==(11)))||(((_HCL_D_icode)==(10))))||(((_HCL_D_icode)==(8))))||(((_HCL_D_icode)==(9)))) ? (4) :
		(_HCL_D_rB));
    _HCL_reg_srcB &= 0xf;
    if (showall) writefln("set reg_srcB to 0x%x",_HCL_reg_srcB);
    ulong _HCL_d_dstE = ((((((_HCL_D_icode)==(3)))||(((_HCL_D_icode)==(2))))||(((_HCL_D_icode)==(6)))) ? (_HCL_D_rB) :
		(15));
    _HCL_d_dstE &= 0xf;
    if (showall) writefln("set d_dstE to 0x%x",_HCL_d_dstE);
    ulong _HCL_e_Stat = _HCL_E_Stat;
    _HCL_e_Stat &= 0x7;
    if (showall) writefln("set e_Stat to 0x%x",_HCL_e_Stat);
    ulong _HCL_e_icode = _HCL_E_icode;
    _HCL_e_icode &= 0xf;
    if (showall) writefln("set e_icode to 0x%x",_HCL_e_icode);
    ulong _HCL_e_ValA = _HCL_E_ValA;
    _HCL_e_ValA &= 0xffffffffffffffff;
    if (showall) writefln("set e_ValA to 0x%x",_HCL_e_ValA);
    ulong _HCL_e_ValE = ((((_HCL_E_icode)==(6))&&((_HCL_E_ifun)==(0))) ? ((_HCL_E_ValA)+(_HCL_E_ValB)) :
		(((_HCL_E_icode)==(6))&&((_HCL_E_ifun)==(1))) ? ((_HCL_E_ValB)-(_HCL_E_ValA)) :
		(((_HCL_E_icode)==(6))&&((_HCL_E_ifun)==(2))) ? ((_HCL_E_ValA)&(_HCL_E_ValB)) :
		(((_HCL_E_icode)==(6))&&((_HCL_E_ifun)==(3))) ? ((_HCL_E_ValA)^(_HCL_E_ValB)) :
		((((_HCL_E_icode)==(4)))||(((_HCL_E_icode)==(5)))) ? ((_HCL_E_ValB)+(_HCL_E_ValC)) :
		((((_HCL_E_icode)==(10)))||(((_HCL_E_icode)==(8)))) ? ((_HCL_E_ValB)-(8UL)) :
		((((_HCL_E_icode)==(11)))||(((_HCL_E_icode)==(9)))) ? ((_HCL_E_ValB)+(8UL)) :
		(((_HCL_E_icode)==(3))) ? (_HCL_E_ValC) :
		(((_HCL_E_icode)==(2))) ? (_HCL_E_ValA) :
		(0UL));
    _HCL_e_ValE &= 0xffffffffffffffff;
    if (showall) writefln("set e_ValE to 0x%x",_HCL_e_ValE);
    _HCL_stall_C = cast(bool)(((_HCL_E_icode)!=(6)));
    if (showall) writefln("set stall_C to %s",_HCL_stall_C);
    ulong _HCL_c_ZF = ((_HCL_e_ValE)==(0UL));
    _HCL_c_ZF &= 0x1;
    if (showall) writefln("set c_ZF to 0x%x",_HCL_c_ZF);
    ulong _HCL_c_SF = ((_HCL_e_ValE)>=(0x8000000000000000UL));
    _HCL_c_SF &= 0x1;
    if (showall) writefln("set c_SF to 0x%x",_HCL_c_SF);
    ulong _HCL_e_conditionsMet = (((_HCL_E_ifun)==(1)) ? ((_HCL_C_SF)||(_HCL_C_ZF)) :
		((_HCL_E_ifun)==(2)) ? (_HCL_C_SF) :
		((_HCL_E_ifun)==(3)) ? (_HCL_C_ZF) :
		((_HCL_E_ifun)==(4)) ? (!_HCL_C_ZF) :
		((_HCL_E_ifun)==(5)) ? ((!_HCL_C_SF)||(_HCL_C_ZF)) :
		((_HCL_E_ifun)==(6)) ? (!_HCL_C_SF) :
		((_HCL_E_ifun)==(0)) ? (1UL) :
		(0UL));
    _HCL_e_conditionsMet &= 0x1;
    if (showall) writefln("set e_conditionsMet to 0x%x",_HCL_e_conditionsMet);
    ulong _HCL_m_Stat = _HCL_M_Stat;
    _HCL_m_Stat &= 0x7;
    if (showall) writefln("set m_Stat to 0x%x",_HCL_m_Stat);
    ulong _HCL_m_icode = _HCL_M_icode;
    _HCL_m_icode &= 0xf;
    if (showall) writefln("set m_icode to 0x%x",_HCL_m_icode);
    ulong _HCL_m_ValE = _HCL_M_ValE;
    _HCL_m_ValE &= 0xffffffffffffffff;
    if (showall) writefln("set m_ValE to 0x%x",_HCL_m_ValE);
    ulong _HCL_m_dstE = _HCL_M_dstE;
    _HCL_m_dstE &= 0xf;
    if (showall) writefln("set m_dstE to 0x%x",_HCL_m_dstE);
    ulong _HCL_reg_dstE = _HCL_W_dstE;
    _HCL_reg_dstE &= 0xf;
    if (showall) writefln("set reg_dstE to 0x%x",_HCL_reg_dstE);
    ulong _HCL_Stat = _HCL_W_Stat;
    _HCL_Stat &= 0x7;
    if (showall) writefln("set Stat to 0x%x",_HCL_Stat);
    ulong _HCL_reg_inputE = (((_HCL_W_icode)==(2)) ? (_HCL_W_ValE) :
		((((_HCL_W_icode)==(3)))||(((_HCL_W_icode)==(6)))) ? (_HCL_W_ValE) :
		0);
    _HCL_reg_inputE &= 0xffffffffffffffff;
    if (showall) writefln("set reg_inputE to 0x%x",_HCL_reg_inputE);
    ulonger _HCL_i10bytes = __read_imem(_HCL_pc);
    if (showpc) writef(`pc = 0x%x; `, _HCL_pc);
    if (showall || showpc) writefln(`loaded [%s]`, disas(_HCL_i10bytes));
    ulong _HCL_reg_outputA = _HCL_reg_srcA < __regfile.length ? __regfile[cast(size_t)_HCL_reg_srcA] : 0;
    if (showall && _HCL_reg_srcA < __regfile.length) writefln("because reg_srcA was set to %x (%s), set reg_outputA to 0x%x", _HCL_reg_srcA, RNAMES[cast(size_t)_HCL_reg_srcA], _HCL_reg_outputA);
    ulong _HCL_reg_outputB = _HCL_reg_srcB < cast(ulong)__regfile.length ? __regfile[cast(size_t)_HCL_reg_srcB] : 0;
    if (showall && _HCL_reg_srcB < __regfile.length) writefln("because reg_srcB was set to %x (%s), set reg_outputB to 0x%x", _HCL_reg_srcB, RNAMES[cast(size_t)_HCL_reg_srcB], _HCL_reg_outputB);
    if (_HCL_reg_dstE < __regfile.length) { __regfile[cast(size_t)_HCL_reg_dstE] = cast(ulong)_HCL_reg_inputE; }
    if (showall && _HCL_reg_dstE < __regfile.length) writefln("wrote reg_inputE (0x%x) to register reg_dstE (%x, which is %s)", _HCL_reg_inputE, _HCL_reg_dstE, RNAMES[cast(size_t)_HCL_reg_dstE]);
    ulong _HCL_f_icode = cast(ulong)(((_HCL_i10bytes)>>4UL)&0xf);
    _HCL_f_icode &= 0xf;
    if (showall) writefln("set f_icode to 0x%x",_HCL_f_icode);
    ulong _HCL_f_ifun = cast(ulong)(((_HCL_i10bytes)>>0UL)&0xf);
    _HCL_f_ifun &= 0xf;
    if (showall) writefln("set f_ifun to 0x%x",_HCL_f_ifun);
    ulong _HCL_f_rA = cast(ulong)(((_HCL_i10bytes)>>12UL)&0xf);
    _HCL_f_rA &= 0xf;
    if (showall) writefln("set f_rA to 0x%x",_HCL_f_rA);
    ulong _HCL_f_rB = cast(ulong)(((_HCL_i10bytes)>>8UL)&0xf);
    _HCL_f_rB &= 0xf;
    if (showall) writefln("set f_rB to 0x%x",_HCL_f_rB);
    ulong _HCL_f_ValC = ((((_HCL_f_icode)==(7))) ? (cast(ulong)(((_HCL_i10bytes)>>8UL)&0xffffffffffffffff)) :
		(cast(ulong)(((_HCL_i10bytes)>>16UL)&0xffffffffffffffff)));
    _HCL_f_ValC &= 0xffffffffffffffff;
    if (showall) writefln("set f_ValC to 0x%x",_HCL_f_ValC);
    ulong _HCL_offset = ((((((_HCL_f_icode)==(0)))||(((_HCL_f_icode)==(1))))||(((_HCL_f_icode)==(9)))) ? (1UL) :
		((((((_HCL_f_icode)==(2)))||(((_HCL_f_icode)==(6))))||(((_HCL_f_icode)==(10))))||(((_HCL_f_icode)==(11)))) ? (2UL) :
		((((_HCL_f_icode)==(7)))||(((_HCL_f_icode)==(8)))) ? (9UL) :
		(10UL));
    _HCL_offset &= 0xffffffffffffffff;
    if (showall) writefln("set offset to 0x%x",_HCL_offset);
    ulong _HCL_valP = (_HCL_F_pc)+(_HCL_offset);
    _HCL_valP &= 0xffffffffffffffff;
    if (showall) writefln("set valP to 0x%x",_HCL_valP);
    ulong _HCL_f_Stat = (((_HCL_f_icode)==(0)) ? (2) :
		((_HCL_f_icode)>(0xbUL)) ? (4) :
		(1));
    _HCL_f_Stat &= 0x7;
    if (showall) writefln("set f_Stat to 0x%x",_HCL_f_Stat);
    _HCL_stall_F = cast(bool)((((((_HCL_f_Stat)==(2)))||(((_HCL_f_Stat)==(4)))) ? (1UL) :
		(0UL)));
    if (showall) writefln("set stall_F to %s",_HCL_stall_F);
    ulong _HCL_e_dstE = (((!_HCL_e_conditionsMet)&&((_HCL_E_icode)==(2))) ? (15) :
		(_HCL_E_dstE));
    _HCL_e_dstE &= 0xf;
    if (showall) writefln("set e_dstE to 0x%x",_HCL_e_dstE);
    ulong _HCL_x_pc = _HCL_valP;
    _HCL_x_pc &= 0xffffffffffffffff;
    if (showall) writefln("set x_pc to 0x%x",_HCL_x_pc);
    ulong _HCL_d_ValA = ((((_HCL_reg_dstE)!=(15))&&((_HCL_reg_dstE)==(_HCL_reg_srcA))) ? (_HCL_reg_inputE) :
		(((_HCL_m_dstE)!=(15))&&((_HCL_m_dstE)==(_HCL_reg_srcA))) ? (_HCL_m_ValE) :
		(((_HCL_e_dstE)!=(15))&&((_HCL_e_dstE)==(_HCL_reg_srcA))) ? (_HCL_e_ValE) :
		(_HCL_reg_outputA));
    _HCL_d_ValA &= 0xffffffffffffffff;
    if (showall) writefln("set d_ValA to 0x%x",_HCL_d_ValA);
    ulong _HCL_d_ValB = ((((_HCL_reg_dstE)!=(15))&&((_HCL_reg_dstE)==(_HCL_reg_srcB))) ? (_HCL_reg_inputE) :
		(((_HCL_m_dstE)!=(15))&&((_HCL_m_dstE)==(_HCL_reg_srcB))) ? (_HCL_m_ValE) :
		(((_HCL_e_dstE)!=(15))&&((_HCL_e_dstE)==(_HCL_reg_srcB))) ? (_HCL_e_ValE) :
		(_HCL_reg_outputB));
    _HCL_d_ValB &= 0xffffffffffffffff;
    if (showall) writefln("set d_ValB to 0x%x",_HCL_d_ValB);

	 // rising clock edge: lock register writes
    if (_HCL_bubble_D) _HCL_D_Stat = 1;
    else if (!_HCL_stall_D) _HCL_D_Stat = _HCL_f_Stat;
    if (_HCL_bubble_D) _HCL_D_rB = 15;
    else if (!_HCL_stall_D) _HCL_D_rB = _HCL_f_rB;
    if (_HCL_bubble_D) _HCL_D_icode = 1;
    else if (!_HCL_stall_D) _HCL_D_icode = _HCL_f_icode;
    if (_HCL_bubble_D) _HCL_D_ifun = 0;
    else if (!_HCL_stall_D) _HCL_D_ifun = _HCL_f_ifun;
    if (_HCL_bubble_D) _HCL_D_ValC = 0;
    else if (!_HCL_stall_D) _HCL_D_ValC = _HCL_f_ValC;
    if (_HCL_bubble_D) _HCL_D_rA = 15;
    else if (!_HCL_stall_D) _HCL_D_rA = _HCL_f_rA;
    if (_HCL_bubble_W) _HCL_W_Stat = 1;
    else if (!_HCL_stall_W) _HCL_W_Stat = _HCL_m_Stat;
    if (_HCL_bubble_W) _HCL_W_ValE = 0;
    else if (!_HCL_stall_W) _HCL_W_ValE = _HCL_m_ValE;
    if (_HCL_bubble_W) _HCL_W_icode = 1;
    else if (!_HCL_stall_W) _HCL_W_icode = _HCL_m_icode;
    if (_HCL_bubble_W) _HCL_W_dstE = 15;
    else if (!_HCL_stall_W) _HCL_W_dstE = _HCL_m_dstE;
    if (_HCL_bubble_M) _HCL_M_Stat = 1;
    else if (!_HCL_stall_M) _HCL_M_Stat = _HCL_e_Stat;
    if (_HCL_bubble_M) _HCL_M_ValE = 0;
    else if (!_HCL_stall_M) _HCL_M_ValE = _HCL_e_ValE;
    if (_HCL_bubble_M) _HCL_M_icode = 1;
    else if (!_HCL_stall_M) _HCL_M_icode = _HCL_e_icode;
    if (_HCL_bubble_M) _HCL_M_conditionsMet = 0;
    else if (!_HCL_stall_M) _HCL_M_conditionsMet = _HCL_e_conditionsMet;
    if (_HCL_bubble_M) _HCL_M_ValA = 0;
    else if (!_HCL_stall_M) _HCL_M_ValA = _HCL_e_ValA;
    if (_HCL_bubble_M) _HCL_M_dstE = 15;
    else if (!_HCL_stall_M) _HCL_M_dstE = _HCL_e_dstE;
    if (_HCL_bubble_F) _HCL_F_pc = 0;
    else if (!_HCL_stall_F) _HCL_F_pc = _HCL_x_pc;
    if (_HCL_bubble_E) _HCL_E_Stat = 1;
    else if (!_HCL_stall_E) _HCL_E_Stat = _HCL_d_Stat;
    if (_HCL_bubble_E) _HCL_E_ValB = 0;
    else if (!_HCL_stall_E) _HCL_E_ValB = _HCL_d_ValB;
    if (_HCL_bubble_E) _HCL_E_ifun = 0;
    else if (!_HCL_stall_E) _HCL_E_ifun = _HCL_d_ifun;
    if (_HCL_bubble_E) _HCL_E_dstE = 15;
    else if (!_HCL_stall_E) _HCL_E_dstE = _HCL_d_dstE;
    if (_HCL_bubble_E) _HCL_E_ValC = 0;
    else if (!_HCL_stall_E) _HCL_E_ValC = _HCL_d_ValC;
    if (_HCL_bubble_E) _HCL_E_icode = 1;
    else if (!_HCL_stall_E) _HCL_E_icode = _HCL_d_icode;
    if (_HCL_bubble_E) _HCL_E_ValA = 0;
    else if (!_HCL_stall_E) _HCL_E_ValA = _HCL_d_ValA;
    if (_HCL_bubble_C) _HCL_C_ZF = 0;
    else if (!_HCL_stall_C) _HCL_C_ZF = _HCL_c_ZF;
    if (_HCL_bubble_C) _HCL_C_SF = 0;
    else if (!_HCL_stall_C) _HCL_C_SF = _HCL_c_SF;
	pragma(msg,`INFO: did not specify mem_readbit/mem_writebit; disabling data memory`);
	pragma(msg,`INFO: did not specify reg_dstM; disabling register write port M`);

	return cast(int)_HCL_Stat;
}
pragma(msg,`Estimated clock delay: 54`);
enum tpt = 54;

import std.stdio, std.file, std.string, std.conv, std.algorithm;
int main(string[] args) {
    bool verbose = true;
    bool pause = false;
    bool showall = false;
    uint maxsteps = 10000;
    string fname;
    foreach(a; args[1..$]) {
        if      (a == "-i" || a == "--interactive") pause   = true;
        else if (a == "-d" || a == "--debug"      ) showall = true;
        else if (a == "-q" || a == "--quiet"      ) verbose = false;
        else if (exists(a)) {
            if (fname.length > 0)
                writeln("WARNING: multiple files; ignoring \"",a,"\" in preference of \"",fname,"\"");
            else
                fname = a;
        } else if (a[0] > '0' && a[0] <= '9') {
            maxsteps = to!uint(a);
        } else {
            writeln("ERROR: unexpected argument \"",a,"\"");
            return 1;
        }
    }
    if (showall && !verbose) {
        writeln("ERROR: cannot be in both quiet and debug mode");
        return 2;
    }
    if (fname.length == 0) {
        writeln("USAGE: ",args[0]," [options] somefile.yo");
        writeln("Options:");
        writefln("    [a number]       : time out after that many steps (default: %d)",maxsteps);
        writeln("    -i --interactive : pause every clock cycle");
        writeln("    -q --quiet       : only show final state");
        writeln("    -d --debug       : show every action during simulation");
        return 3;
    }
    // load .yo input
    auto f = File(fname,"r");
    foreach(string line; lines(f)) {
        // each line is 0xaddress : hex data | junk, or just junk
        // fixed width:
        //     01234567890123456789012345678...
        //     0x000: 30f40001000000000000 |    irmovq $0x100,%rsp  # Initialize stack pointer
        if (line[0..2] == "0x") {
            auto address = to!uint(line[2..5], 16);
            auto datas = line[7..27].strip;
            for(uint i=0; i < datas.length; i += 2) {
                __memory[address+(i>>1)] = to!ubyte(datas[i..i+2],16);
            }
        }
    }

    void dumpstate() {
        writefln("| RAX: % 16x   RCX: % 16x   RDX: % 16x |", __regfile[0], __regfile[1], __regfile[2]);
        writefln("| RBX: % 16x   RSP: % 16x   RBP: % 16x |", __regfile[3], __regfile[4], __regfile[5]);
        writefln("| RSI: % 16x   RDI: % 16x   R8:  % 16x |", __regfile[6], __regfile[7], __regfile[8]);
        writefln("| R9:  % 16x   R10: % 16x   R11: % 16x |", __regfile[9], __regfile[10], __regfile[11]);
        writefln("| R12: % 16x   R13: % 16x   R14: % 16x |", __regfile[12], __regfile[13], __regfile[14]);

	write(`| register xF(`,(_HCL_bubble_F?'B':_HCL_stall_F?'S':'N'));
		writefln(`) { pc=%016x }                                |`, _HCL_F_pc);


	write(`| register fD(`,(_HCL_bubble_D?'B':_HCL_stall_D?'S':'N'));
		writefln(`) { Stat=%01x ValC=%016x icode=%01x ifun=%01x rA=%01x     |`, _HCL_D_Stat, _HCL_D_ValC, _HCL_D_icode, _HCL_D_ifun, _HCL_D_rA);
		writefln(`|  rB=%01x }                                                               |`, _HCL_D_rB);


	write(`| register dE(`,(_HCL_bubble_E?'B':_HCL_stall_E?'S':'N'));
		writefln(`) { Stat=%01x ValA=%016x ValB=%016x   |`, _HCL_E_Stat, _HCL_E_ValA, _HCL_E_ValB);
		writefln(`|  ValC=%016x dstE=%01x icode=%01x ifun=%01x }                        |`, _HCL_E_ValC, _HCL_E_dstE, _HCL_E_icode, _HCL_E_ifun);


	write(`| register eM(`,(_HCL_bubble_M?'B':_HCL_stall_M?'S':'N'));
		writefln(`) { Stat=%01x ValA=%016x ValE=%016x   |`, _HCL_M_Stat, _HCL_M_ValA, _HCL_M_ValE);
		writefln(`|  conditionsMet=%01x dstE=%01x icode=%01x }                                     |`, _HCL_M_conditionsMet, _HCL_M_dstE, _HCL_M_icode);


	write(`| register mW(`,(_HCL_bubble_W?'B':_HCL_stall_W?'S':'N'));
		writefln(`) { Stat=%01x ValE=%016x dstE=%01x icode=%01x }        |`, _HCL_W_Stat, _HCL_W_ValE, _HCL_W_dstE, _HCL_W_icode);


	write(`| register cC(`,(_HCL_bubble_C?'B':_HCL_stall_C?'S':'N'));
		writefln(`) { SF=%01x ZF=%01x }                                          |`, _HCL_C_SF, _HCL_C_ZF);

        auto set = __memory.keys; sort(set);
        writeln("| used memory:   _0 _1 _2 _3  _4 _5 _6 _7   _8 _9 _a _b  _c _d _e _f    |");
        ulong last = 0;
        foreach(a; set) {
            if (a >= last) {
                last = ((a>>4)<<4);
                writef("|  0x%07x_:  ", last>>4);
                foreach(j; 0..16) {
                    if (last+j in __memory) { writef(" %02x", __memory[last+j]); }
                    else write("   ");
                    if (j == 7) write("  ");
                    if (j == 3 || j == 11) write(" ");
                }
                writeln("    |");
                if (last + 16 < last) break;
                last += 16;
            }
        }
    }
    
    // loop, possibly pausing
    foreach(i; 0..maxsteps) {
        if (verbose) {
            writefln("+------------------- between cycles %4d and %4d ----------------------+", i, i+1);
            dumpstate();
            writeln("+-----------------------------------------------------------------------+");
            if (pause) {
                write("(press enter to continue)");
                stdin.readln();
            }
        }
        auto code = tick(verbose, showall);
        if (code == 2) {
            writeln("+----------------------- halted in state: ------------------------------+");
            dumpstate();
            writeln("+--------------------- (end of halted state) ---------------------------+");
            writeln("Cycles run: ",i+1);
            writeln("Time used: ", (i+1)*tpt);
            return 0;
        }
        if (code > 2) {
            writeln("+------------------- error caused in state: ----------------------------+");
            dumpstate();
            writeln("+-------------------- (end of error state) -----------------------------+");
            writeln("Cycles run: ",i+1);
            writeln("Time used: ", (i+1)*tpt);
            write("Error code: ", code);
            if (code < 6) writeln(" (", ["Bubble","OK","Halt","Invalid Address", "Invalid Instruction", "Pipeline Error"][code],")");
            else writeln(" (user-defined status code)");
            return 0;
        }
    }
    writefln("+------------ timed out after %5d cycles in state: -------------------+", maxsteps);
    dumpstate();
    writeln("+-----------------------------------------------------------------------+");
    
    return 0;
}