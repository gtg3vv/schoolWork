/**
 * HCL2, a hardware description language inspired by the HCL language
 * described in Computer Systems: A Programmer's Perspective by 
 * R. Bryant and D. O'Hallaron.
 * 
 * Version: 2016-10-28
 * 
 * License:
 * Copyright (c) 2016 Luther Tychonievich. 
 * Released into the public domain.  
 * Attribution is appreciated but not required.
 * 
 */
module hcl2d;

import pegged.grammar;
import std.stdio, std.conv, std.string : format, join;

import grammar;

/// The following is the public interface to the built-in functionality:
enum builtins = `
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

`;

enum bvec_src = `private template negOneList(uint length) {
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
}`;

mixin(bvec_src);
// private static import bvec;
alias bvec!80 ulonger;


/// For error messages: creates a string describing the location of the 
/// provided parse tree node.  Starts counting after the builtins.
string location(ParseTree p) {
    
    // parsing errors are [0..last ok parse]
    if (builtins.length > p.begin) {
        if (p.end >= builtins.length) {
            int sl=1, sc=0;
            foreach(i,c; p.input[builtins.length..p.end]) {
                if (c == '\n') {
                    if (i==0 || p.input[builtins.length+i-1] != '\r') { sl += 1; sc = 0; }
                } else if (c == '\r')                                 { sl += 1; sc = 0; }
                else sc += 1;
            }
            return format(" (starting at line %d:%d)", sl, sc);
        } else {
            return " (in the builtin code)";
        }
    }

    int sl=1, sc=0;
    foreach(i,c; p.input[builtins.length..p.begin]) {
        if (c == '\n') {
            if (i==0 || p.input[builtins.length+i-1] != '\r') { sl += 1; sc = 0; }
        } else if (c == '\r')                                 { sl += 1; sc = 0; }
        else sc += 1;
    }
    size_t si,ei;
    size_t i = p.begin;
    for(; i<p.end; i+=1) {
        auto c = p.input[i];
        if (c == ' ' || c == '\t' || c == '\n' || c == '\r') {
            if (c == '\n') {
                if (i==0 || p.input[i-1] != '\r') { sl += 1; sc = 0; }
            } else if (c == '\r')                 { sl += 1; sc = 0; }
            else sc += 1;
        } else { break; }
    }
    si = i;
    int el=sl, ec=sc;
    int dl=sl, dc=sc;
    for(; i<p.end; i+=1) {
        auto c = p.input[i];
        if (c == ' ' || c == '\t' || c == '\n' || c == '\r') {
            if (c == '\n') {
                if (i==0 || p.input[i-1] != '\r') { sl += 1; sc = 0; }
            } else if (c == '\r')                 { sl += 1; sc = 0; }
            else dc += 1;
        } else {
            dc += 1;
            el = dl;
            ec = dc;
            ei = i+1;
        }
    }
    
    if (sl < el) return format(" (lines %d-%d)", sl, el);
    return format(" (line %d:%d-%d \"%s\")", sl, sc, ec, p.input[si..ei]);
}

/// For error messages: creates a string describing the location of the 
/// provided parse tree node.  Starts counting after the builtins.
string justLocation(ParseTree p) {
    
    // parsing errors are [0..last ok parse]
    if (builtins.length > p.begin) {
        if (p.end >= builtins.length) {
            int sl=1, sc=0;
            foreach(i,c; p.input[builtins.length..p.end]) {
                if (c == '\n') {
                    if (i==0 || p.input[i-1] != '\r') { sl += 1; sc = 0; }
                } else if (c == '\r')                 { sl += 1; sc = 0; }
                else sc += 1;
            }
            return format("(ending at %d:%d)", sl, sc);
        } else {
            return "(in builtin code)";
        }
    }

    int sl=1, sc=0;
    foreach(i,c; p.input[builtins.length..p.begin]) {
        if (c == '\n') {
            if (i==0 || p.input[i-1] != '\r') { sl += 1; sc = 0; }
        } else if (c == '\r')                 { sl += 1; sc = 0; }
        else sc += 1;
    }
    size_t si,ei;
    size_t i = p.begin;
    for(; i<p.end; i+=1) {
        auto c = p.input[i];
        if (c == ' ' || c == '\t' || c == '\n' || c == '\r') {
            if (c == '\n') {
                if (i==0 || p.input[i-1] != '\r') { sl += 1; sc = 0; }
            } else if (c == '\r')                 { sl += 1; sc = 0; }
            else sc += 1;
        } else { break; }
    }
    si = i;
    int el=sl, ec=sc;
    int dl=sl, dc=sc;
    for(; i<p.end; i+=1) {
        auto c = p.input[i];
        if (c == ' ' || c == '\t' || c == '\n' || c == '\r') {
            if (c == '\n') {
                if (i==0 || p.input[i-1] != '\r') { dl += 1; dc = 0; }
            } else if (c == '\r')                 { dl += 1; dc = 0; }
            else dc += 1;
        } else {
            dc += 1;
            el = dl;
            ec = dc;
            ei = i+1;
        }
    }
    
    if (sl < el) return format("%d-%d", sl, el);
    return format("%d:%d-%d", sl, sc, ec);
}







/// The precidence of various C operators, for constant evaluation
enum BIN_PREC = [
    ["*","/","%"], // trash size
    ["+","-"],     // trash size
    ["<","<=",">",">=","==","!="], // always size 1
    ["&"], // same size as inputs if same, else trash
    ["^"], // same size as inputs if same, else trash
    ["|"], // same size as inputs if same, else trash
    ["&&"], // same size as inputs if same, else trash
    ["||"], // same size as inputs if same, else trash
];
enum MASK = [
    "0x0",
    "0x1",                  "0x3",                  "0x7",                  "0xf",
    "0x1f",                 "0x3f",                 "0x7f",                 "0xff",
    "0x1ff",                "0x3ff",                "0x7ff",                "0xfff",
    "0x1fff",               "0x3fff",               "0x7fff",               "0xffff",
    "0x1ffff",              "0x3ffff",              "0x7ffff",              "0xfffff",
    "0x1fffff",             "0x3fffff",             "0x7fffff",             "0xffffff",
    "0x1ffffff",            "0x3ffffff",            "0x7ffffff",            "0xfffffff",
    "0x1fffffff",           "0x3fffffff",           "0x7fffffff",           "0xffffffff",
    "0x1ffffffff",          "0x3ffffffff",          "0x7ffffffff",          "0xfffffffff",
    "0x1fffffffff",         "0x3fffffffff",         "0x7fffffffff",         "0xffffffffff",
    "0x1ffffffffff",        "0x3ffffffffff",        "0x7ffffffffff",        "0xfffffffffff",
    "0x1fffffffffff",       "0x3fffffffffff",       "0x7fffffffffff",       "0xffffffffffff",
    "0x1ffffffffffff",      "0x3ffffffffffff",      "0x7ffffffffffff",      "0xfffffffffffff",
    "0x1fffffffffffff",     "0x3fffffffffffff",     "0x7fffffffffffff",     "0xffffffffffffff",
    "0x1ffffffffffffff",    "0x3ffffffffffffff",    "0x7ffffffffffffff",    "0xfffffffffffffff",
    "0x1fffffffffffffff",   "0x3fffffffffffffff",   "0x7fffffffffffffff",   "0xffffffffffffffff",
];

/// helper methods: treat an array like a set
bool contains(string[] lst, string key) {
    foreach(string s; lst) if (s == key) return true;
    return false;
}
/// ditto
string[] without(string[] array, string key) {
    foreach(i,e; array) if (e == key) { return array[0..i]~array[i+1..$]; }
    return array;
}

int[string] wireWidths; // for storing the declared size of wires and register parts
ulong[string] constValues; // for storing the computed meaning of constants
bool[string] initialized; // for storing if each wire is given a value
struct regpart { int width; ulong init; }
regpart[string][char] plRegisters; // for storing the set of declared registers
char[char] plRegsInputLetterOf;
char[char] plRegsOutputLetterOf;

/// Walks a tree representing a compile-time constant value, which it
/// returns.  Adds any errors to the errors parameter
ulong evalConst(ParseTree p, ref string[] errors) {
    switch(p.name) {
        case "HCL.Math1":
            // a string of binary operators; evaluate by merging
            // inefficient, but simple
            ulong[] ans = new ulong[(p.children.length+1)/2];
            string[] ops = new string[(p.children.length-1)/2];
            for(int i = 0; i < p.children.length; i += 2)
                ans[i/2] = evalConst(p.children[i], errors);
            for(int i = 1; i < p.children.length; i += 2)
                ops[(i-1)/2] = p.children[i].matches[0];
            foreach(preclist; BIN_PREC) {
                for(int i=0; i<ops.length; i+=1) {
                    if (preclist.contains(ops[i])) {
                        ulong tmp;
                        switch(ops[i]) {
                            case "*":  tmp = ans[i] *  ans[i+1]; break;
                            case "/":  tmp = ans[i] /  ans[i+1]; break;
                            case "%":  tmp = ans[i] %  ans[i+1]; break;
                            case "+":  tmp = ans[i] +  ans[i+1]; break;
                            case "-":  tmp = ans[i] -  ans[i+1]; break;
                            case "<":  tmp = ans[i] <  ans[i+1]; break;
                            case ">":  tmp = ans[i] >  ans[i+1]; break;
                            case "<=": tmp = ans[i] <= ans[i+1]; break;
                            case ">=": tmp = ans[i] >= ans[i+1]; break;
                            case "==": tmp = ans[i] == ans[i+1]; break;
                            case "!=": tmp = ans[i] != ans[i+1]; break;
                            case "|":  tmp = ans[i] |  ans[i+1]; break;
                            case "^":  tmp = ans[i] ^  ans[i+1]; break;
                            case "&":  tmp = ans[i] &  ans[i+1]; break;
                            case "||": tmp = ans[i] || ans[i+1]; break;
                            case "&&": tmp = ans[i] && ans[i+1]; break;
                            default: errors ~= "unexpected binary operator "~ops[i]~location(p);
                        }
                        ans = ans[0..i] ~ tmp ~ ans[i+2..$];
                        ops = ops[0..i] ~ ops[i+1..$];
                        i -= 1;
                    }
                }
            }
            return ans[0];
        case "HCL.Math2":
            // unary operators
            ulong ans = evalConst(p.children[$-1], errors);
            foreach_reverse(op; p.children[0..$-1]) {
                switch (op.matches[0]) {
                    case "!" : ans = !ans; break;
                    case "-" : ans = -ans; break;
                    case "~" : ans = ~ans; break;
                    default: errors ~= "unexpected unary operator "~op.matches[0]~location(p);
                }
            }
            return ans;
        case "HCL.WireCat":
            // wire concatenation via mask and shift
            ulong ans = evalConst(p.children[0], errors);
            int bits = wireWidth(p.children[0]);
            if (bits <= 0) { errors ~= "cannot concatenate unsized values"~location(p); return ulong.max; }
            foreach(c; p.children[1..$]) {
                int b2 = wireWidth(c);
                if (b2 <= 0) { errors ~= "cannot concatenate unsized values"~location(p); return ulong.max; }
                bits += b2;
                ans <<= b2;
                ans |= evalConst(c, errors) & (~(ulong.max<<b2));
                if (bits > 64) { errors ~= "cannot concatenate constants past 64 bits"~location(p); return ulong.max; }
            }
            return ans;
        case "HCL.Slice":
            // wire slicing via mask and shift
            ulong ans = evalConst(p.children[0], errors);
            if (p.children.length > 1) {
                auto sidx = to!int(p.children[1].matches[0]);
                auto eidx = to!int(p.children[2].matches[0]);
                if (eidx <= sidx) {
                    errors ~= "ending slice index must be greater than starting slice index"~location(p);
                } else if (ans > 0 && eidx > ans) {
                    errors ~= "ending slice index cannot be larger than # wires in input"~location(p);
                } else if (eidx >= 64) {
                    errors ~= "ending slice index cannot be larger than maximum constant width of 64"~location(p);
                }
                if (sidx > 0) { ans >>= sidx; eidx -= sidx; }
                if (eidx < 64) ans &= ~((~0L)<<eidx);
            }
            return ans;

        case "HCL.BinLit":
            return to!ulong(p.matches[1], 2);
        case "HCL.HexLit":
            return to!ulong(p.matches[1], 16);
        case "HCL.DecLit":
            return to!ulong(p.matches[0]);
        case "HCL.BoolLit":
            return 5 - p.matches[0].length; // "true" vs "false"

        case "HCL.Variable":
            if (p.matches[0] in constValues) return constValues[p.matches[0]];
            errors ~= "cannot use non-constant "~p.matches[0]~" in constant expression"~location(p);
            return ulong.max;

        default: break;
    }
    return (p.children.length == 1) ? evalConst(p.children[0], errors) : ulong.max;
}

/// Computes the width of a parse tree node; <0 means an unspecfied width
int wireWidth(ParseTree p) {
    switch(p.name) {
        case "HCL.BinLit" : return cast(int)p.matches[1].length;
        
        case "HCL.DecLit":
        case "HCL.HexLit": return -1;
        
        case "HCL.Slice": 
            if (p.children.length == 0) goto default;
            return to!int(p.children[2].matches[0]) - to!int(p.children[1].matches[0]);
        
        case "HCL.Variable":
            if (p.matches[0] in wireWidths) return wireWidths[p.matches[0]];
            return -1;
        
        case "HCL.WireCat":
            int ans = 0;
            foreach(child; p.children) ans += wireWidth(child);
            return ans;
        
        case "HCL.Math2":
            int ans = wireWidth(p.children[$-1]);
            foreach_reverse(op; p.children[0..$-1]) {
                if (op.matches[0] == "-") ans = -1;
                else if (op.matches[0] == "!") ans = 1;
                else { /* ~ does not change size; no-op */ }
            }
            return ans;
        
        case "HCL.Math1":
            // some binary operators change sizes, others create them
            int[] ans = new int[(p.children.length+1)/2];
            string[] ops = new string[(p.children.length-1)/2];
            for(int i = 0; i < p.children.length; i += 2)
                ans[i/2] = wireWidth(p.children[i]);
            for(int i = 1; i < p.children.length; i += 2)
                ops[(i-1)/2] = p.children[i].matches[0];
            foreach(k,preclist; BIN_PREC) {
                for(int i=0; i<ops.length; i+=1) {
                    if (preclist.contains(ops[i])) {
                        if (k <= 1) { // */%  or  +-
                            ans = ans[0..i] ~ -1 ~ ans[i+2..$];
                        } else if (k <= 2) { // <>=
                            ans = ans[0..i] ~ 1 ~ ans[i+2..$];
                        } else { // |^& || &&
                            if (ans[i] == ans[i+1])
                                ans = ans[0..i] ~ ans[i+1..$];
                            else
                                ans = ans[0..i] ~ -1 ~ ans[i+2..$];
                        } 
                        ops = ops[0..i] ~ ops[i+1..$];
                        i -= 1;
                    }
                }
            }
            return ans[0];
        case "HCL.MuxRow":
            return wireWidth(p.children[1]);
        case "HCL.MuxExp":
            return wireWidth(p.children[0]);
        default: break;
    }
    return (p.children.length == 1) ? wireWidth(p.children[0]) : -1;
}


/// typecheck pass 1: the names, widths, etc, of the declared values
private bool typecheck_decls(ParseTree p, ref string[] errors) {
    switch(p.name) {
        case "HCL.ConstDef":
            // ok if the name is ok
            for(int i=0; i<p.children.length; i+=2) {
                auto n = p.children[i+0].matches[0];
                auto val = evalConst(p.children[i+1], errors);
                if (n in ["true":0,"false":0,"True":0,"False":0,"TRUE":0,"FALSE":0,
                    "wire":0,"register":0,"const":0]) {
                    errors ~= `Reserved words cannot be defined as constants`~location(p.children[i]);
                } else if (n in constValues) {
                    errors ~= `Cannot redefine constants`~location(p.children[i]);
                } else if (n in wireWidths) {
                    errors ~= `Cannot redefine wires as constants`~location(p.children[i]);
                } else if (n.length == 1 && n[0] >= 'A' && n[0] <= 'Z') {
                    errors ~= `Single capital letters reserved for register banks`~location(p.children[i]);
                } else if (n.length >1 && n[1] == '_' && n[0] != '_') {
                    errors ~= `letter-underscore reserved for register bank I/O`~location(p.children[i]);
                } else {
                    constValues[n] = val;
                }
            }
            break;
        case "HCL.WireDef":
            // ok if the name is ok and the width legal
            for(int i=0; i<p.children.length; i+=2) {
                auto n = p.children[i+0].matches[0];
                auto width = to!int(p.children[i+1].matches[0]);
                if (n in ["true":0,"false":0,"True":0,"False":0,"TRUE":0,"FALSE":0,
                    "wire":0,"register":0,"const":0]) {
                    errors ~= `Reserved words cannot be used as a wire names`~location(p.children[i]);
                } else if (n in constValues) {
                    errors ~= `Cannot redeclare constants as wires`~location(p.children[i]);
                } else if (n in wireWidths) {
                    errors ~= `Cannot redeclare wire `~n~` `~location(p.children[i]);
                } else if (n.length == 1 && n[0] >= 'A' && n[0] <= 'Z') {
                    errors ~= `Single capital letters reserved for register banks`~location(p.children[i]);
                } else if (n.length >1 && n[1] == '_' && n[0] != '_') {
                    errors ~= `letter-underscore reserved for register bank I/O`~location(p.children[i]);
                } else if (width < 1 || width > 80) {
                    errors ~= `wires must be between 1 and 80 bits wide`~location(p);
                } else {
                    wireWidths[n] = width;
                }
            }
            break;
        case "HCL.RegDef":
            // ok if the name is unique and the parts have sane widths and initial values
            char letter = p.matches[1][$-1];
            if (letter in plRegisters) {
                errors ~= `cannot redefine register `~letter~location(p);
                break;
            }
            char inLetter = cast(char)(p.matches[1].length > 1 ? p.matches[1][0] : p.matches[1][$-1]+'a'-'A');
            if (inLetter in plRegsOutputLetterOf) {
                errors ~= `cannot redefine register input `~inLetter~location(p);
                break;
            }
            plRegsInputLetterOf[letter] = inLetter;
            plRegsOutputLetterOf[inLetter] = letter;
            plRegisters[letter] = null;
            foreach(rp; p.children) {
                string name = rp.children[0].matches[0];
                if (name in plRegisters[letter]) {
                    errors ~= `cannot redefine register parts`~location(rp);
                } else {
                    regpart pt = { cast(int)evalConst(rp.children[1], errors), evalConst(rp.children[2], errors) };
                    auto vw = wireWidth(rp.children[2]);
                    if (pt.width <= 0) errors ~= `cannot have register width <= 0`~location(rp.children[1]);
                    else if (pt.width > 64) errors ~= `cannot have register width > 64`~location(rp.children[1]);
                    else if (vw >= 0 && vw != pt.width)
                        errors ~= format(`cannot initialize a %d-bit register part to a %d-bit value%s`,pt.width, vw, location(p));
                    else {
                        plRegisters[letter][name] = pt;
                        wireWidths[letter~"_"~name] = pt.width;
                        if (letter~"_"~name in initialized)
                            errors ~= `cannot assign values to register outputs`~location(p);
                        initialized[letter~"_"~name] = true;
                        wireWidths[inLetter~"_"~name] = pt.width;
                    }
                }
            }
            wireWidths[`stall_`~letter] = 1;
            wireWidths[`bubble_`~letter] = 1;
            break;
        default:
            // ok if all parts are ok
            bool ok = true;
            foreach(c; p.children) ok &= typecheck_decls(c, errors);
            return ok;
    }
    return errors.length == 0;
}

/// typecheck pass 2: the gates that use the declared wires and registers
private bool typecheck_gates(ParseTree p, ref string[] errors) {
    switch(p.name) {
        case "HCL.ConstDef": break;
        case "HCL.RegDef": break;
        case "HCL.WireDef": break;
        case "HCL.Initialize":
            // ok if the expression is ok, the name exists, and the widths are compatible
            for(int i=0; i<p.children.length; i+=2) {
                auto n = p.children[i+0].matches[0];
                {
                    auto tmp = errors.length;
                    typecheck_gates(p.children[i+1], errors);
                    if (errors.length > tmp) continue;
                }
                if (n in constValues) {
                    errors ~= `cannot redefine a constant as if it were a wire`~location(p.children[i]);
                } else if (n !in wireWidths) {
                    errors ~= `cannot define an undeclared wire`~location(p.children[i]);
                } else if (n in initialized && initialized[n]) {
                    errors ~= `cannot define the same wire multiple times`~location(p.children[i]);
                } else {
                    auto vw = wireWidth(p.children[i+1]);
                    if (vw >= 0 && vw != wireWidths[n]) {
                        errors ~= format(`cannot set a %d-bit wire to a %d-bit value%s`,wireWidths[n], vw, location(p));
                    } else {
                        initialized[n] = true;
                    }
                }
            }
            break;
        case "HCL.Slice":
            // ok if the expression is ok and the indices are in order and not too big
            if (p.children.length <= 1) goto default;
            typecheck_gates(p.children[0], errors);
            auto ww = wireWidth(p.children[0]);
            auto ei = to!int(p.children[2].matches[0]);
            auto bi = to!int(p.children[1].matches[0]);
            if (ww > 0 && ei > ww) errors ~= `cannot slice past the end of a value`~location(p);
//          else if (ei > 64) errors ~= `cannot slice past index 64`~location(p.children[2]);
            else if (bi >= ei) errors ~= `cannot have starting slice >= ending slice`~location(p);
            if (bi < 0) errors ~= `cannot slice with a negative index`~location(p.children[1]);
            break;
        case "HCL.Variable":
            // ok if it refers to something defined sometime by someone
            auto name = p.matches[0];
            if (name in constValues) break;
            if (name in initialized) break;
            if (name in wireWidths) break; // errors ~= `use of value before initialization`~location(p); // not needed, covered in code generation
            else errors ~= `use of undeclared identifier`~location(p);
            break;
        case "HCL.WireCat":
            // ok if parts have widths and do no become too big to store
            bool ok = true;
            foreach(c; p.children) ok &= typecheck_gates(c, errors);
            if (!ok) return ok;
            int w = 0;
            foreach(child; p.children) {
                int ww = wireWidth(child);
                if (ww < 0)
                    errors ~= `cannot use .. operator on unwidthed values`~location(child);
                else w += ww;
            }
            if (w > 80)
                errors ~= `cannot use .. operator to create values of more than 80 bits`~location(p);
            break;
        case "HCL.MuxExp":
            bool ok = true;
            auto wid = wireWidth(p.children[0]);
            foreach(child; p.children) {
                ok &= typecheck_gates(child, errors);
                auto w = wireWidth(child);
                if (w < 0) continue;
                if (wid < 0) wid = w;
                if (wireWidth(child) != wid) {
                    errors ~= `all entries in a mux must have the same wire width`~location(p);
                    ok = false;
                    break;
                }
            }
            if (ok && wid > 64) {
                errors ~= `muxes must evalaute to 64-bit values or less`~location(p);
                ok = false;
            }
            return ok;
        default:
            // ok if all parts are ok
            bool ok = true;
            foreach(c; p.children) ok &= typecheck_gates(c, errors);
            return ok;
    }
    return errors.length == 0;
}


/// creates graphviz code for an initializer
private void loop_finder_helper(ParseTree p, ref string[][string] digraph) {
    switch(p.name) {
        case "HCL.Initialize":
            for(int i=0; i<p.children.length; i += 2) {
                foreach(name; inputWires!false(p.children[i+1])) {
                    if(name !in digraph) digraph[name] = null;
                    digraph[name] ~= p.matches[0];
                }
                foreach(name; selectorWires!false(p.children[i+1])) {
                    if(name !in digraph) digraph[name] = null;
                    digraph[name] ~= p.matches[0];
                }
            }
            break;
        default: 
            foreach(c; p.children) loop_finder_helper(c, digraph);
            break;
    }
}

private string[] find_cycles(string[][string] graph) {
    
    void pop(T)(ref T[] x) {
        x.length = x.length - 1;
    }

    void sospop(ref string[][] sos) {
        pop(sos[$-1]);
        while (sos.length > 0 && sos[$-1].length == 0) {
            pop(sos);
            if (sos.length > 0) pop(sos[$-1]);
        }
    }

    string findLoop(string root, string[][] sos, string leaf) {
        if (root == leaf) {
            string ans = "Cyclic dependency: "~root;
            foreach(i; 0..sos.length) { ans ~= " -> " ~ sos[i][$-1]; if (sos[i][$-1] == leaf) break; }
            return ans;
        }
        foreach(j; 0..sos.length-1) { 
            if (sos[j][$-1] == leaf) {
                string ans = "Cyclic dependency: "~sos[j][$-1];
                foreach(i; j+1..sos.length) { ans ~= " -> " ~ sos[i][$-1]; if (sos[i][$-1] == leaf) break; }
                return ans;
            }
        }
        return null;
    }

    
    string[][] sos; // stack of stacks
    bool[string] visited;
    string[] ans;
    foreach(n,kids; graph) {
        if(n in visited) continue;
        visited[n] = true;
        sos = [kids.dup];
        while(sos.length > 0 && sos[0].length > 0) {
            string next = sos[$-1][$-1]; 
            auto err = findLoop(n, sos, next);
            if (err) { // found a new loop
                ans ~= err;
                visited[next] = true;
                sospop(sos);
                continue;
            }
            if (next in visited) { // cycle and/or subtree already known
                sospop(sos);
                continue;
            }
            visited[next] = true;
            if (next in graph && graph[next].length > 0)  {
                sos ~= graph[next];
            } else {
                sospop(sos);
            }
        }
    }
    return ans;
}



/// typecheck pass 3: loop for cyclic dependencies
private bool typecheck_loops(ParseTree p, ref string[] errors) {
    string[][string] digraph = [
        `pc`:[`i10bytes`],
        `reg_srcA`:[`reg_outputA`],
        `reg_srcB`:[`reg_outputB`],
        `mem_addr`:[`mem_output`],
        `mem_readbit`:[`mem_output`],
    ];
    loop_finder_helper(p, digraph);
    string[] errs = find_cycles(digraph);
    if (errs.length > 0) {
        errors ~= errs;
        return false;
    }
    return true;
}


/// The main error-checking routine, attempts to verify that all of the
/// elements of the HCL code make sense (defined once, matching sizes, etc)
bool typecheck(ParseTree p, ref string[] errors) {
    if (initialized is null) initialized = ["reg_outputA":true, "reg_outputB":true, "mem_output":true, "i10bytes":true];
    return typecheck_decls(p,errors) && typecheck_gates(p, errors) && typecheck_loops(p, errors);
}

/// some log_2, min, and max helper functions
int lg(int wid) {
    int ans = 1;
    while (wid > 1) { ans += 1; wid >>= 1; }
    return ans;
}
/// ditto
int lgMax(int[] w...) {
    int ans = 1;
    foreach(o; w) { auto b = lg(o); if (b > ans) ans = b; }
    return ans;
}
/// ditto
int lgMin(int[] w...) {
    int ans = int.max;
    foreach(o; w) { auto b = lg(o); if (b < ans) ans = b; }
    return ans;
}
/// ditto
int min(int[] a...) {
    int ans = a[0];
    foreach(x; a) if (x < ans) ans = x;
    return ans;
}
/// ditto
int max(int[] a...) {
    int ans = a[0];
    foreach(x; a) if (x < 0) return x; else if (x > ans) ans = x;
    return ans;
}

/// Clock delay estimation.  This method is known to be very crude and
/// should most likely be re-written from scratch, but it at least gives
/// vaguley defensible answers.
int calculateDelay(ParseTree p, in int[string] delay) {
    switch(p.name) {
        case "HCL.Math1":
            int[] ans = new int[(p.children.length+1)/2];
            int[] wid = new int[(p.children.length+1)/2];
            string[] ops = new string[(p.children.length-1)/2];
            for(int i = 0; i < p.children.length; i += 2) {
                ans[i/2] = calculateDelay(p.children[i], delay);
                if (ans[i/2] < 0) return ans[i/2];
                wid[i/2] = wireWidth(p.children[i]);
                if (wid[i/2] <= 0) wid[i/2] = 64;
            }
            for(int i = 1; i < p.children.length; i += 2)
                ops[(i-1)/2] = p.children[i].matches[0];
            foreach(preclist; BIN_PREC) {
                for(int i=0; i<ops.length; i+=1) {
                    if (preclist.contains(ops[i])) {
                        int tmp, nw;
                        switch(ops[i]) {
                            case "*":  
                                nw = wid[i]+wid[i+1]-1;
                                tmp = (5+2*lgMax(wid[i],wid[i+1]))*min(wid[i],wid[i+1]); 
                                break;
                            case "/":  goto case;
                            case "%":  
                                nw = max(wid[i],wid[i+1]);
                                tmp = (5+2*lgMax(wid[i],wid[i+1]))*min(wid[i],wid[i+1])*4; 
                                break;
                            case "+":  goto case;
                            case "-":
                                nw = max(wid[i],wid[i+1])+1;
                                tmp = 3+2*lgMax(wid[i], wid[i+1]); 
                                break;
                            case "<":  goto case;
                            case ">":  goto case;
                            case "<=": goto case;
                            case ">=": goto case;
                            case "==": goto case;
                            case "!=": 
                                nw = 1;
                                tmp = lgMin(wid[i], wid[i+1]); 
                                break;
                            case "|":  nw = max(wid[i], wid[i+1]); tmp = 1; break;
                            case "^":  nw = max(wid[i], wid[i+1]); tmp = 2; break;
                            case "&":  nw = min(wid[i], wid[i+1]); tmp = 1; break;
                            case "||": goto case;
                            case "&&": 
                                nw = max(wid[i], wid[i+1]);
                                tmp = 1; 
                                break;
                            default: return -1;
                        }
                        tmp += max(ans[i],ans[i+1]);
                        ans = ans[0..i] ~ tmp ~ ans[i+2..$];
                        ops = ops[0..i] ~ ops[i+1..$];
                        wid = wid[0..i] ~ nw ~ wid[i+1..$];
                        i -= 1;
                    }
                }
            }
            return ans[0];
        case "HCL.Math2":
            int ans = calculateDelay(p.children[$-1], delay);
            if (ans < 0) return ans;
            int w = wireWidth(p.children[$-1]);
            foreach_reverse(op; p.children[0..$-1]) {
                switch (op.matches[0]) {
                    case "!" : ans += lg(w); w = 1; break;
                    case "-" : ans += 1+lg(w); break;
                    case "~" : ans += 1; break;
                    default: break;
                }
            }
            return ans;

        case "HCL.WireCat":
            int ans = 0;
            foreach(c; p.children) {
                int d = calculateDelay(c,delay);
                if (d < 0) return d;
                if (d > ans) ans = d;
            }
            return ans;

        case "HCL.Math": goto case;
        case "HCL.Math3": goto case;
        case "HCL.Slice": goto case;
        case "HCL.Value":
            return calculateDelay(p.children[0],delay);

        case "HCL.BinLit": goto case;
        case "HCL.HexLit": goto case;
        case "HCL.DecLit": goto case;
        case "HCL.BoolLit":
            return 0;

        case "HCL.Variable":
            if (p.matches[0] in constValues) return 0;
            if (`_HCL_`~p.matches[0] in delay) return delay[`_HCL_`~p.matches[0]];
            return -1;

        default: 
            return -1;


        case "HCL.MuxExp":
            int ans = 0;
            foreach(c; p.children) ans = max(ans,calculateDelay(c, delay));
            if (ans < 0) return ans;
            return ans + cast(int)p.children.length + 1;
        case "HCL.MuxRow":
            
            return max(calculateDelay(p.children[0],delay), calculateDelay(p.children[1],delay));

        case "HCL.SetMembership":
            throw new Exception("Set membership should have been refactored away");
    }
}

/// turns an expression into D code
string asDCode(ParseTree p) {
    switch(p.name) {

        case "HCL.Value":
            if (p.children[0].matches.length < p.matches.length)
                return `(`~asDCode(p.children[0])~`)`;
            else goto case;
        case "HCL.Math": goto case;
        case "HCL.Math3": 
            return asDCode(p.children[0]);

        case "HCL.Math1": 
            // a string of binary operators; evaluate by merging
            // inefficient, but simple
            string[] ans = new string[(p.children.length+1)/2];
            string[] ops = new string[(p.children.length-1)/2];
            for(int i = 0; i < p.children.length; i += 2)
                ans[i/2] = asDCode(p.children[i]);
            for(int i = 1; i < p.children.length; i += 2)
                ops[(i-1)/2] = p.children[i].matches[0];
            foreach(preclist; BIN_PREC) {
                for(int i=0; i<ops.length; i+=1) {
                    if (preclist.contains(ops[i])) {
                        string tmp = `(`~ans[i]~`)`~ops[i]~`(`~ans[i+1]~`)`;
                        ans = ans[0..i] ~ tmp ~ ans[i+2..$];
                        ops = ops[0..i] ~ ops[i+1..$];
                        i -= 1;
                    }
                }
            }
            return ans[0];
        case "HCL.Math2": 
            auto ans = ``;
            foreach(c; p.children) ans ~= asDCode(c);
            return ans;

        case "HCL.Slice":
            if (p.children.length == 1) return asDCode(p.children[0]);
            return `cast(ulong)(((`~asDCode(p.children[0])~`)>>`~asDCode(p.children[1])~`)&`~MASK[wireWidth(p)]~`)`;
        
        case "HCL.WireCat":
            string ans = asDCode(p.children[0]);
            foreach(c; p.children[1..$]) {
                auto w = wireWidth(c);
                ans = "(("~ans~")<<"~to!string(w)~") | (("~asDCode(c)~")&"~MASK[w]~")";
            }
            return ans;
        
        case "HCL.BoolLit":
            if (p.matches[0].length == 4) return "1"; // true
            else return "0"; // false
        
        case "HCL.Variable":
            if (p.matches[0] in constValues) return to!string(constValues[p.matches[0]]);
            else return `_HCL_`~p.matches[0];

        case "HCL.BinLit": goto case;
        case "HCL.HexLit": goto case;
        case "HCL.DecLit":
            return p.input[p.begin..p.end]~"UL";

        case "HCL.BinOp": goto case;
        case "HCL.UnOp":
            return p.matches[0];

        case "HCL.MuxExp":
            string ans = "(";
            foreach(c; p.children) {
                string[] errs;
                auto ec = evalConst(c.children[0], errs);
                if (errs.length)
                    ans ~= "("~asDCode(c.children[0])~") ? ("~asDCode(c.children[1])~") :\n\t\t";
                else if (ec)
                    return ans ~= "("~asDCode(c.children[1])~"))";
                else
                    continue;
            }
            return ans ~= "0)";

        default: return p.input[p.begin..p.end];
    }
}

/// creates D code for an initializer, including wire size masking,
/// and also handles delay propogation
string codeWithDelay(ParseTree p, ref int[string] delay, ref int skipped) {
    switch(p.name) {
        case "HCL.Initialize":
            string ans;
            for(int i=0; i<p.children.length; i += 2) {
                auto name = p.children[i].matches[0];
                string prefix = 
                    (name.length > 1 && name[1] == '_' && name[0] >= 'A' && name[0] <= 'Z') ? "" :
                    (name.length > 6 && name[0..6] == "stall_") ? "" :
                    (name.length > 7 && name[0..7] == "bubble_") ? "" :
                    "ulong ";
                name = `_HCL_`~name;
                if (name in delay) continue;
                
                int d = calculateDelay(p.children[i+1], delay);
                if (d < 0) skipped += 1;
                else {
                    delay[name] = d;
                    if (name[0..$-1] == "_HCL_stall_" || name[0..$-1] == "_HCL_bubble_") {
                        ans ~= `    `~prefix~name~` = cast(bool)(`~asDCode(p.children[i+1])~");\n";
                        ans ~= `    if (showall) writefln("set `~name[5..$]~` to %s",`~name~");\n";
                    } else {
                        ans ~= `    `~prefix~name~` = `~asDCode(p.children[i+1])~";\n";
                        ans ~= `    `~name~` &= `~MASK[wireWidth(p.children[i])]~";\n";
                        ans ~= `    if (showall) writefln("set `~name[5..$]~` to 0x%x",`~name~");\n";
                    }
                }
            }
            return ans;
        default: 
            string ans = "";
            foreach(c; p.children) ans ~= codeWithDelay(c, delay, skipped);
            return ans;
    }
}



/// the main code generation process.  Quite involved, but it works well.
/// It should be relatively straightforward to rewrite this to generate
/// C or another language instead of D, but I haven't spent the effort
/// to do so yet.
string codegen(ParseTree p, ref string[] errors) {
    /* Generated code should look like
     * 1. a comment with the course HCL, including builtins
     * 2. the builtin functionality's state (register file, memory)
     * 3. the user-provided register's state
     * 4. a bit "tick" method that sets all the wires in a dependency 
     *    order and then locks the register values in.
     * 5. a main method that parses command line options and drives the
     *    simulator
     */
    
    static import std.string, std.array, std.algorithm;
    
    
    // no need to declare constants; they are automatic
    // step 1-2: fixed functionality;
    string ans = `// auto-generated HCL2 simulator; DO NOT EDIT THIS FILE
/+++++++++++++++++ generated from the following HCL: ++++++++++++++++++
`;
    ans ~= std.string.strip(std.array.replace(p.input,"+/","+ /"));
    ans ~= `
++++++++++++++++++ generated from the preceeding HCL ++++++++++++++++++/

`;
    if (errors.length > 0) {
        ans ~= "pragma(msg,`";
        foreach(e; errors) {
            ans ~= std.array.replace(e,"`"," ") ~ "\n\n";
        }
        ans ~= "`);";
        return ans;
    }

//    static import std.file, std.path;
    ans ~= "\n\n\n/////////////////////// int type bigger than long ///////////////////\n";
    ans ~= bvec_src;//std.file.readText("bvec.d");
    ans ~= `alias bvec!80 ulonger;


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

//////////////// pipeline registers' initial values ////////////////`;
    int[string] delay;
    
    // step 3: declare all register outputs
    // also bubble and stall, not because they have state but to simplify
    // the tick code
    foreach(letter, rdefs; plRegisters) {
        ans ~= `
// register bank `~letter~`:
bool _HCL_bubble_`~letter~` = false;
bool _HCL_stall_`~letter~`  = false;`;
        foreach(name, rdef; rdefs) {
            ans ~= `
ulong _HCL_`~letter~`_`~name~` = `~to!string(rdef.init)~";";
            delay[`_HCL_`~letter~`_`~name] = 10;
        }
    }

    // step 4: create "tick" method
    ans ~= `

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
`;
    // fixed point computation based on how many wires still need setting
    int goAgain = int.max-1;
    int oldGoAgain = int.max;
    while (goAgain > 0 && goAgain < oldGoAgain) {
        oldGoAgain = goAgain;
        goAgain = 0;

        // HCL logic
        ans ~= codeWithDelay(p, delay, goAgain);
        
        enum rread_delay = 16, rwrite_delay = 16, dmread_delay = 32, dmwrite_delay = 24, imread_delay = 16;

        // memory reads
        if (`_HCL_pc` in delay && `_HCL_i10bytes` !in delay) {
            ans ~= "    ulonger _HCL_i10bytes = __read_imem(_HCL_pc);\n";
            ans ~= "    if (showpc) writef(`pc = 0x%x; `, _HCL_pc);\n";
            ans ~= "    if (showall || showpc) writefln(`loaded [%s]`, disas(_HCL_i10bytes));\n";
            delay[`_HCL_i10bytes`] = delay[`_HCL_pc`] + imread_delay;
        } else { goAgain += `_HCL_i10bytes` !in delay; }

        // register reads
        if (`_HCL_reg_srcA` in delay && `_HCL_reg_outputA` !in delay) {
            ans ~= "    ulong _HCL_reg_outputA = _HCL_reg_srcA < __regfile.length ? __regfile[cast(size_t)_HCL_reg_srcA] : 0;\n";
            ans ~= `    if (showall && _HCL_reg_srcA < __regfile.length) writefln("because reg_srcA was set to %x (%s), set reg_outputA to 0x%x", _HCL_reg_srcA, RNAMES[cast(size_t)_HCL_reg_srcA], _HCL_reg_outputA);`~"\n";
            delay[`_HCL_reg_outputA`] = delay[`_HCL_reg_srcA`] + rread_delay;
        } else { goAgain += `_HCL_reg_outputA` !in delay; }
        if (`_HCL_reg_srcB` in delay && `_HCL_reg_outputB` !in delay) {
            ans ~= "    ulong _HCL_reg_outputB = _HCL_reg_srcB < cast(ulong)__regfile.length ? __regfile[cast(size_t)_HCL_reg_srcB] : 0;\n";
            ans ~= `    if (showall && _HCL_reg_srcB < __regfile.length) writefln("because reg_srcB was set to %x (%s), set reg_outputB to 0x%x", _HCL_reg_srcB, RNAMES[cast(size_t)_HCL_reg_srcB], _HCL_reg_outputB);`~"\n";
            delay[`_HCL_reg_outputB`] = delay[`_HCL_reg_srcB`] + rread_delay;
        } else { goAgain += `_HCL_reg_outputB` !in delay; }

        // register writes
        if (`_HCL_reg_dstE` in delay && `_HCL_reg_inputE` in delay && `regE` !in delay) {
            ans ~= "    if (_HCL_reg_dstE < __regfile.length) { __regfile[cast(size_t)_HCL_reg_dstE] = cast(ulong)_HCL_reg_inputE; }\n";
            ans ~= `    if (showall && _HCL_reg_dstE < __regfile.length) writefln("wrote reg_inputE (0x%x) to register reg_dstE (%x, which is %s)", _HCL_reg_inputE, _HCL_reg_dstE, RNAMES[cast(size_t)_HCL_reg_dstE]);`~"\n";
            delay[`regE`] = delay[`_HCL_reg_inputE`] + rwrite_delay;
        } else { goAgain += `regE` !in delay; }
        if (`_HCL_reg_dstM` in delay && `_HCL_reg_inputM` in delay && `regM` !in delay) {
            ans ~= "    if (_HCL_reg_dstM < __regfile.length) { __regfile[cast(size_t)_HCL_reg_dstM] = cast(ulong)_HCL_reg_inputM; }\n";
            ans ~= `    if (showall && _HCL_reg_dstM < __regfile.length) writefln("wrote reg_inputM (0x%x) to register reg_dstM (%x, which is %s)", _HCL_reg_inputM, _HCL_reg_dstM, RNAMES[cast(size_t)_HCL_reg_dstM]);`~"\n";
            delay[`regM`] = delay[`_HCL_reg_inputM`] + rwrite_delay;
        } else { goAgain += `regM` !in delay; }
        
        
        // memory reads
        if (`_HCL_mem_addr` in delay && `_HCL_mem_readbit` in delay && `_HCL_mem_output` !in delay) {
            ans ~= "    ulong _HCL_mem_output = _HCL_mem_readbit ? __read_dmem(_HCL_mem_addr) : 0;\n";
            ans ~= `    if (showall && _HCL_mem_readbit) writefln("because mem_readbit was 1, set mem_output to 0x%x by reading memory from mem_addr (0x%x)", _HCL_mem_output, _HCL_mem_addr);`~"\n";
            delay[`_HCL_mem_output`] = max(delay[`_HCL_mem_addr`], delay[`_HCL_mem_readbit`]) + dmread_delay;
        } else { goAgain += `_HCL_mem_output` !in delay; }

        // memory write
        if (`_HCL_mem_addr` in delay && `_HCL_mem_writebit` in delay && `_HCL_mem_input` in delay && `dmem` !in delay) {
            ans ~= "    if (_HCL_mem_writebit) __write_dmem(_HCL_mem_addr, _HCL_mem_input);\n";
            ans ~= `    if (showall && _HCL_mem_writebit) writefln("because mem_writebit was 1, set memory at mem_addr (0x%x) to mem_input (0x%x)", _HCL_mem_addr, _HCL_mem_input);`~"\n";
            delay[`dmem`] = max(delay[`_HCL_mem_addr`], delay[`_HCL_mem_writebit`], delay[`_HCL_mem_input`]) + dmwrite_delay;
        } else { goAgain += `dmem` !in delay; }
        
    }
    // lock all register values
    ans ~= "\n\t // rising clock edge: lock register writes\n";
    foreach(letter, rdefs; plRegisters) {
        char lower = plRegsInputLetterOf[letter];
        foreach(name, rdef; rdefs) {
            if (`_HCL_`~lower~`_`~name in delay) {
                ans ~= `    if (_HCL_bubble_`~letter~`) _HCL_`~letter~`_`~name~" = "~to!string(rdef.init)~";\n";
                ans ~= `    else if (!_HCL_stall_`~letter~`) _HCL_`~letter~`_`~name~" = "~`_HCL_`~lower~`_`~name~";\n";
            }
        }
    }
    
    string[] undone;
    foreach(name,wid; wireWidths) {
        if (name.length > 6 && name[0..6] == `stall_`) continue;
        if (name.length > 7 && name[0..7] == `bubble_`) continue;
        if (name == `reg_outputA` || name == `reg_outputB` || name == `mem_output`) continue;
        if (`_HCL_`~name !in delay) undone ~= name;
    }
    
    if (undone.contains(`Stat`)) {
        undone = undone.without(`Stat`);
        ans ~= "\tpragma(msg,`WARNING: did not specify Stat; using STAT_HLT as a default`);\n";
        ans ~= "\t_HLC_Stat = 2;\n";
    }
    if (undone.contains(`mem_readbit`) && undone.contains(`mem_writebit`)) {
        undone = undone.without(`mem_addr`);
        undone = undone.without(`mem_readbit`);
        undone = undone.without(`mem_writebit`);
        undone = undone.without(`mem_input`);
        ans ~= "\tpragma(msg,`INFO: did not specify mem_readbit/mem_writebit; disabling data memory`);\n";
    }
    if (undone.contains(`mem_writebit`)) {
        undone = undone.without(`mem_writebit`);
        undone = undone.without(`mem_input`);
        ans ~= "\tpragma(msg,`INFO: did not specify mem_writebit; disabling memory writes`);\n";
    }
    if (undone.contains(`reg_srcA`)) {
        undone = undone.without(`reg_srcA`);
        ans ~= "\tpragma(msg,`INFO: did not specify reg_srcA; disabling register read port A`);\n";
    }
    if (undone.contains(`reg_srcB`)) {
        undone = undone.without(`reg_srcB`);
        ans ~= "\tpragma(msg,`INFO: did not specify reg_srcB; disabling register read port B`);\n";
    }
    if (undone.contains(`reg_dstE`)) {
        undone = undone.without(`reg_dstE`);
        undone = undone.without(`reg_inputE`);
        ans ~= "\tpragma(msg,`INFO: did not specify reg_dstE; disabling register write port E`);\n";
    }
    if (undone.contains(`reg_dstM`)) {
        undone = undone.without(`reg_dstM`);
        undone = undone.without(`reg_inputM`);
        ans ~= "\tpragma(msg,`INFO: did not specify reg_dstM; disabling register write port M`);\n";
    }
    if (undone.length > 0) {
        std.algorithm.sort(undone);
        errors ~= `failed to initialize `~join(undone,", ");
        ans ~= "\n\tstatic assert(false, `failed to initialize the following values: ";
        ans ~= join(undone,", ");
        ans ~= "`);\n";
    } else {
        // check to see if we halted
        if (`_HCL_Stat` in delay) ans ~= "\n\treturn cast(int)_HCL_Stat;\n";
        else ans ~= "\n\treturn int.max;\n";
    }
    ans ~= "}\n";

    int d = 0;
    foreach(k,v; delay) if (v > d) d = v;
    ans ~= "pragma(msg,`Estimated clock delay: "~to!string(d)~"`);\n";
    ans ~= "enum tpt = "~to!string(d)~";\n";
    
    
    // step 5: create "main" method
    ans ~= `
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
        writefln("| R12: % 16x   R13: % 16x   R14: % 16x |", __regfile[12], __regfile[13], __regfile[14]);`;
    // dump register files 
    char[] keys;
    foreach(letter; ['P','F','D','E','M','W']) { // do these first, in order
        if (letter in plRegisters) keys ~= letter;
    }
    foreach(letter, rdefs; plRegisters) { // then these
        if (letter != 'P' && letter != 'F' && letter != 'D' && letter != 'E' && letter != 'M' && letter != 'W') keys ~= letter;
    }
    foreach(letter; keys) {
        auto rdefs = plRegisters[letter];
//  foreach(letter, rdefs; plRegisters) {
        ans ~= "\n\n\twrite(`| register "~plRegsInputLetterOf[letter]~``~letter~"(`,(_HCL_bubble_"~letter~"?'B':_HCL_stall_"~letter~"?'S':'N'));\n\t\twritefln(`) {";
        uint used = 18;
        string extra = "";
        string[] names = rdefs.keys;
        names.sort;
        foreach(name; names) {
            auto rdef = rdefs[name];
            uint hexsize = (rdef.width+3)/4;
            if (used + 2 + hexsize + name.length < 71) {
                ans ~= " "~name~"=%0"~to!string(hexsize)~"x";
                extra ~= ", _HCL_"~letter~"_"~name;
                used += 2+name.length+hexsize;
            } else {
                while(used < 71) { ans ~= ' '; used += 1; }
                ans ~= " |`"~extra~");\n";
                ans ~= "\t\twritefln(`| ";
                ans ~= " "~name~"=%0"~to!string(hexsize)~"x";
                extra = ", _HCL_"~letter~"_"~name;
                used = cast(uint)(4+name.length+hexsize);
            }
        }
        ans ~= " }"; used += 2;
        while(used < 72) { ans ~= ' '; used += 1; }
        if (used < 73) ans ~= "|";
        ans ~= "`"~extra~");\n";
    }
        
    ans ~= `
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
`;

    return ans;
}


/////////////////////////////////////////////////////////////////////////////
/// handles graphviz recrod naming
string graphvizName(string name) {
	enum builtins = ["reg_srcA":0, "reg_outputA":0, "reg_srcB":0, "reg_outputB":0, "reg_dstE":0, "reg_inputE":0, "reg_dstM":0, "reg_inputM":0, "mem_addr":1, "mem_readbit":1, "mem_writebit":1, "mem_input":1, "mem_output":1, "pc":2, "i10bytes":2, "Stat":3];
	if (name in constValues) return null; // ignore constants
	else if (name.length > 1 && name[1] == '_') { // pipeline register I/O
		char letter = name[0];
		if (letter in plRegsOutputLetterOf) letter = plRegsOutputLetterOf[letter];
		return `_reg_`~letter~`:`~name;
	} else if (name[0..$-1] == `bubble_` || name[0..$-1] == `stall_`) { // pipeline register metacontrol
		char letter = name[$-1];
		return `_reg_`~letter~`:`~name;
	} else if (name in builtins) { // memory or register system
		return [`_regfile`,`_datamem`,`_instmem`, "_status"][builtins[name]]~':'~name;
	} else return name; // wire
}

/// turns an expression into a set of input wires
string[] inputWires(bool klobber=true)(ParseTree p) {
    switch(p.name) {

        case "HCL.Value": goto case;
        case "HCL.Math": goto case;
        case "HCL.Slice": goto case;
        case "HCL.Math3": 
            return inputWires!klobber(p.children[0]);

        case "HCL.BinOp": goto case;
        case "HCL.UnOp": goto case;
        case "HCL.BinLit": goto case;
        case "HCL.HexLit": goto case;
        case "HCL.DecLit": goto case;
        case "HCL.BoolLit":
            return typeof(return).init;
        
        case "HCL.Variable":
            if (p.matches[0] in constValues) return typeof(return).init; // ignore constants
            else return [klobber ? graphvizName(p.matches[0]) : p.matches[0]];
        
        case "HCL.MuxRow":
            return inputWires!klobber(p.children[1]);
        
        case "HCL.MuxExp": goto case;
        case "HCL.Math1": goto case;
        case "HCL.Math2": goto case;
        case "HCL.WireCat": goto default;
        default:
            typeof(return) ans;
            foreach(c; p.children) ans ~= inputWires!klobber(c);
            uniquify(ans);
            return ans;
    }
}
/// turns an expression into a set of mux selection input wires
string[] selectorWires(bool klobber=true)(ParseTree p) {
    switch(p.name) {

        case "HCL.Value": goto case;
        case "HCL.Math": goto case;
        case "HCL.Slice": goto case;
        case "HCL.Math3": 
            return selectorWires!klobber(p.children[0]);

        case "HCL.BinOp": goto case;
        case "HCL.UnOp": goto case;
        case "HCL.BinLit": goto case;
        case "HCL.HexLit": goto case;
        case "HCL.DecLit": goto case;
        case "HCL.BoolLit": goto case;
        case "HCL.Variable":
            return typeof(return).init;
        
        case "HCL.MuxRow":
            return inputWires!klobber(p.children[0]);
        
        case "HCL.MuxExp": goto case;
        case "HCL.Math1": goto case;
        case "HCL.Math2": goto case;
        case "HCL.WireCat": goto default;
        default:
            typeof(return) ans;
            foreach(c; p.children) ans ~= selectorWires!klobber(c);
            uniquify(ans);
            return ans;
    }
}

void uniquify(T)(ref T[] list) {
	size_t i = 0, j = 0;
	for(; i<list.length; i+=1) {
		bool keep = true;
		foreach(v; list[0..j]) keep &= (v != list[i]);
		if (keep) { list[j] = list[i]; j+=1; }
	}
	list.length = j;
}


/// creates graphviz code for an initializer
string graphvizCode_helper(ParseTree p) {
    switch(p.name) {
        case "HCL.Initialize":
            string ans;
            for(int i=0; i<p.children.length; i += 2) {
                auto name = graphvizName(p.children[i].matches[0]);
                auto ins = inputWires(p.children[i+1]);
                auto sel = selectorWires(p.children[i+1]);
                if (ins.length == 1 && sel.length == 0) {
                    ans ~= `    `~ins[0]~` -> `~name~";\n";
                } else {
                    ans ~= `    _op_`~p.children[i].matches[0]~" [shape=\"none\" label=\""~justLocation(p.children[i+1])~"\"];\n";
                    ans ~= `    _op_`~p.children[i].matches[0]~` -> `~name~";\n";
                    foreach(dep; ins) {
                        ans ~= `    `~dep~` -> _op_`~p.children[i].matches[0]~";\n";
                    }
                    foreach(dep; sel) {
                        ans ~= `    `~dep~` -> _op_`~p.children[i].matches[0]~" [style=dotted];\n";
                    }
                }
            }
            return ans;
        case "HCL.RegDef":
            char letter = p.matches[1][$-1];
            char inLetter = cast(char)(p.matches[1].length > 1 ? p.matches[1][0] : p.matches[1][$-1]+'a'-'A');
            string ans = `_reg_`~letter~` [shape="record" label="{|{<bubble_`~letter~`>bubble_`~letter~`|<stall_`~letter~`>stall_`~letter~`}}`;
            auto inp = inLetter~`_`, outp = letter~`_`;
            foreach(rp; p.children) {
                string name = rp.children[0].matches[0];
                ans ~= `|{<`~outp~name~`>`~outp~name~`|<`~inp~name~`>`~inp~name~'}';
            }
            return ans ~ "\"];\n";
            break;
        default: 
            string ans = "";
            foreach(c; p.children) ans ~= graphvizCode_helper(c);
            return ans;
    }
}



/// the main graphviz code generation process.
string graphvizCode(ParseTree p, ref string[] errors, string name="hclviz") {
    
    import std.algorithm.iteration : filter;
    import std.range : array;
    string name2 = to!string(name.filter!(a => a >= 'A' && a <= 'Z' || a >= 'a' && a <= 'z' || a == '_' || a >= '0' && a <= '9').array);
    
    // no need to declare constants; they are automatic
    // step 1-2: fixed functionality;
    string ans = `digraph `~name2~` { // auto-generated HCL2 visualization via graphviz
    node [ fontname="sans-serif" ];
    rankdir=BT;`;
    if (errors.length > 0) {
        ans ~= `
    label="Latest compilation had errors!";
}`;
        return ans;
    }
    ans ~= `
    ///////////////////////// builtin components ////////////////////////

    _regfile [shape="record" label="{<reg_outputA>reg_outputA|<reg_srcA>reg_srcA}|{<reg_outputB>reg_outputB|<reg_srcB>reg_srcB}|{|{<reg_dstE>reg_dstE|<reg_inputE>reg_inputE}}|{|{<reg_dstM>reg_dstM|<reg_inputM>reg_inputM}}" style="filled" fillcolor="#aaffff"];
    _datamem [shape="record" label="{<mem_output>mem_output|{<mem_readbit>mem_readbit|<mem_addr>mem_addr}}|{|{<mem_writebit>mem_writebit|<mem_input>mem_input}}" style="filled" fillcolor="#aaffff"];
    _instmem [shape="record" label="{<i10bytes>i10bytes|<pc>pc}" style="filled" fillcolor="#aaffff"];
    _status [shape="record" label="{|<Stat>Stat}" style="filled" fillcolor="#aaffff"];

    //////////////////////////// user code //////////////////////////////

` ~ graphvizCode_helper(p) ~ `
}`;
    
    return ans;
}
/////////////////////////////////////////////////////////////////////////////


static import std.file;
int main(string[] args) {
    if (args.length != 2 || args[1].length < 5 || args[1][$-4..$] != ".hcl") {
        writeln("USAGE: ",args[0]," hclcode.hcl");
        return 1;
    }
    if (!std.file.exists(args[1])) {
        writeln(`ERROR: no such file "`,args[0],`"`);
        return 2;
    }
    string hclcode = File(args[1]).readln('\0');
    auto t = HCL(builtins~hclcode);
    
    string[] errs;
    if (!t.successful) {
        errs ~= `Syntax error`~location(t);
    }
    typecheck(t,errs);
    string dcode = codegen(t, errs);
    if (errs.length > 0) {
        foreach(err; errs) {
            writeln("ERROR: ",err);
        }
        return 3;
    }
    string ofname = args[1][0..$-4]~"_hcl.d";
    File(ofname,"w").write(dcode);

    ofname = args[1][0..$-4]~"_hcl.dot";
    File(ofname,"w").write(graphvizCode(t,errs, args[1][0..$-4]));
    
    return 0;
}

