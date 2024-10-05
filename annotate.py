# Copyright (c) 2022 Kanishka Jayawardane [kanishkagj@yahoo.com]
# Copyright (c) 2022 Michael Selig

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from collections import namedtuple

#======================================== IFTP.. Definitions ========================================
IFTP1_dict = {
    100 : "K_S (trailing edge thickness parameter)",
    101 : "c_m0",
    102 : "t/c_max",
    103 : "alpha_0 (rarely used)",
    104 : "x/c_max location of maximum thickness",
    105 : "maximum camber",
    106 : "leading edge radius",
    107 : "t/c_max (Eppler method)",
    121 : "t/c_max for a gensym airfoil",
    122 : "flap angle for a gensym airfoil",
    135 : "area (uses value for CHORDO for chord length)",
    146 : "volume of an axisymmetric body produced by a symmetric airfoil rotated about the x-axis",
    155 : "TEX (Trailing Edge offset in X)",
    156 : "TEY (Trailing Edge offset in Y)",
    157 : "XTEMIDPT (Trailing Edge MIDPoinT in X -- relative to x = 1)",
    158 : "YTEMIDPT (Trailing Edge MIDPoinT in Y)",
    184 : "omega_us",
    185 : "omega_ls",
    190 : "mu_us",
    191 : "mu_ls",
    192 : "K_H_us",
    193 : "K_H_ls",
    194 : "omega_us (indirectly through mu_us as linearizer)",
    195 : "omega_ls (indirectly through mu_ls as linearizer)",
    196 : "omega'_us",
    197 : "omega'_ls",
    198 : "omega_T_us (incompatible with IFTP1=200)",
    199 : "omega_T_ls (incompatible with IFTP1=200)",
    201 : "velocity differential between Phi_S_us and Phi_S_ls",
    202 : "velocity at Phi_S_us",
    203 : "velocity at Phi_S_ls",
    204 : "c_m",
    205 : "t/c for given x/c",
    206 : "camber for given x/c",
    400 : "x/c",
    401 : "s/c",
    402 : "y/c",
    403 : "angle (used to design flat bottomed airfoils)",
    500 : "H_12 when alpha is segment alpha*",
    501 : "R_delta2 when alpha is segment alpha*",
    502 : "TC when alpha is segment alpha*",
    503 : "n_ENN when alpha is segment alpha*",
    504 : "n_Drela when alpha is segment alpha*",
    505 : "H_32 when alpha is segment alpha*",
    506 : "c_f when alpha is segment alpha*",
    600 : "H_12",
    601 : "H_32",
}

IFTP2_dict = {
    100 : "v(s) when alpha is segment alpha*",
    200 : "H_12(s) when alpha is segment alpha*",
    201 : "TC(s) when alpha is segment alpha*",
    202 : "n(s)_ENN when alpha is segment alpha*",
    203 : "n(s)_Drela when alpha is segment alpha*",
    204 : "H_32(s) when alpha is segment alpha*",
    205 : "C_f(s) when alpha is segment alpha*",
    300 : "H_32(s) for given Re(R1) and alpha(R2) --[allows for iteration on alpha*]",
    500 : "Bubble ramp"
}

#======================================== ITP.. Definitions =========================================
ITP_1_val_dict ={
    1 : "Phi of segment {}",
    4 : "Vi (iteration on velocity level allowed only once) of segment {}",
    5 : "Vi_tilde of segment {}",
    6 : "Alpha* of segment {}",
}

ITP_2_val_dict = {
    0:{
    1 : "DELSX - used to get TEX (trailing edge thickness in x)",
    2 : "DELXY - used to get TEY (trailing edge thickness in y)",
    3 : "XMAPOFF - used to get XTEMIDPT",
    4 : "YMAPOFF - used to get YTEMIDPT",
    },

    1:{
    100 : "upper-surface Phi-values, except Phi_ILE",
    200 : "lower-surface Phi-values, except Phi_ILE",
    300 : "upper-surface and lower-surface Phi-values in OPPOSITE directions (excluding Phi_ILE)",
    400 : "upper-surface and lower-surface Phi-values in the SAME direction (excluding Phi_ILE)",   
    500 : "upper-surface Phi-values, including Phi_ILE",
    600 : "lower-surface Phi-values, including Phi_ILE",
    700 : "upper-surface and lower-surface Phi-values in OPPOSITE directions (including Phi_ILE)",
    800 : "upper-surface and lower-surface Phi-values in the SAME direction (including Phi_ILE)",
    1000 : "group 1 Phi-values",
    1100 : "group 2 Phi-values",
    1200 : "group 3 Phi-values",
    },
    
    2:{
    100 : "Phi_W Upper (=Phi_1)",
    200 : "Phi_W Lower (=Phi_ISEG-1)",
    300 : "Phi_W Upper and Phi_W Lower in OPPOSITE directions",
    400 : "Phi_W Upper and Phi_W Lower in the SAME direction",
    },
    3:{
    100 : "Phi_S Upper(= Phi1)",
    200 : "Phi_S Lower(= PhiI_SEG-1)",
    300 : "Phi_S Upper and Phi_S Lower in OPPOSITE directions",
    400 : "Phi_S Upper and Phi_S Lower in the SAME direction",
    },
    6:{
    100 : "upper-surface alpha* values",
    200 : "lower-surface alpha* values",
    300 : "upper-surface alpha* values and lower-surface alpha* values in OPPOSITE directions",
    400 : "upper-surface alpha* values and lower-surface alpha* values in the SAME direction",
    500 : "upper-surface alpha* values (excluding the recovery alpha*)",
    600 : "lower-surface alpha* values (excluding the recovery alpha*)",
    700 : "upper-surface alpha* values and lower-surface alpha* values in OPPOSITE directions (excluding the recovery alpha*s)",
    800 : "upper-surface alpha* values and lower-surface alpha* values in the SAME direction (excluding the recovery alpha*s)",
    1000 : "group 1 alpha*-values",
    1100 : "group 2 alpha*-values",
    1200 : "group 3 alpha*-values",
    },
    7:{
    100 : "upper-surface K",
    200 : "lower-surface K",
    300 : "upper-surface K and lower-surface K in OPPOSITE directions",
    400 : "upper-surface K and lower-surface K in the SAME direction",
    }
}

#====================================== LLBOS/LLBE Definitions ======================================
LLBOS_dict = {
    1: "beginning of the segment (BOS)",
    0: "end of the segment (EOS)"
}

LLBE_dict = {
    1: "in the BOS-->EOS direction (lower Surface)",
    0: "in the EOS-->BOS direction (upper Surface)"
}

# ======================================= NEWT1.. Descriptions =======================================
NEWT1G0_description = """\
# Specify {} = {} 
# Iterate on {}.
{}{}"""

NEWT1G1_description = """\
# Specify {} = {} @ {} 
# Iterate on {}.
{}{}"""

NEWT1S0_description = """\
# Specify {} at the {} {} = {} 
# Iterate on {}.
{}{}"""

NEWT1S1_description = """\
# Specify {} = {} at the {} {} for Re={}
# Iterate on {}.
{}{}"""

NEWT1S2_description = """\
# Specify {} = {} at the {} {} @ alpha of {} degrees and Re={} 
# Iterate on {}.
{}{}"""

# ======================================= NEWT2.. Descriptions =======================================

NEWT2SD0_description = """\
# Specify {}
# Iterate on DELV for segment {} velocity distribution
# Specification(s) given by the [SubSegment arc length | SubSegment tilde] pairs in the proceeding {}; 
# Specs are {}
{}{}"""

NEWT2SD1_description = """\
# Specify {}
# Iterating on DELV for segment {} velocity distribution
# Specification(s) given by the [SubSegment arc length | SubSegment tilde] pairs in the proceeding {}; 
# Specs are {} for given Re = {}
{}{}"""

NEWT2SD2_description = """\
# Specify {}
# Iterate on DELV for segment {} velocity distribution
# Specification(s) given by the [SubSegment arc length | SubSegment tilde] pairs in the proceeding {}; 
# Specs are {} for given Re = {} and alpha = {}
{}{}"""

# ======================================= NEWT1.. Named tuples =======================================
NEWT1G0 = namedtuple('NEWT1G0', "IFTP1 FNEWT1 ITP1 ITP2 CLAMP1",                          defaults=(None,)*5)
NEWT1G1 = namedtuple('NEWT1G1', "IFTP1 COND1 FNEWT1 ITP1 ITP2 CLAMP1",                    defaults=(None,)*6)
NEWT1S0 = namedtuple('NEWT1S0', "IFTP1 JSEGIX1 LLBOS FNEWT1 ITP1 ITP2 CLAMP1",            defaults=(None,)*7)
NEWT1S1 = namedtuple('NEWT1S1', "IFTP1 JSEGIX1 LLBOS COND1 FNEWT1 ITP1 ITP2 CLAMP1",      defaults=(None,)*8)
NEWT1S2 = namedtuple('NEWT1S2', "IFTP1 JSEGIX1 LLBOS COND1 COND2 FNEWT1 ITP1 ITP2 CLAMP1",defaults=(None,)*9)

# ======================================= NEWT2.. Named tuples =======================================
NEWT2SD0 = namedtuple('NEWT2SD0', "IFTP2 JSEGIX2 LLBE KADJSBS CLAMP1",        defaults=(None,)*5)
NEWT2SD1 = namedtuple('NEWT2SD1', "IFTP2 JSEGIX2 LLBE R1 KADJSBS CLAMP1",     defaults=(None,)*6)
NEWT2SD2 = namedtuple('NEWT2SD2', "IFTP2 JSEGIX2 LLBE R1 R2 KADJSBS CLAMP1",  defaults=(None,)*7)

# ================================== NEWT1.. Interpreter Functions ===================================
def get_ITP_interpretation(ITP1, ITP2):
    try:    return ITP_2_val_dict[ITP1][ITP2]
    except: return ITP_1_val_dict[ITP1].format(ITP2)

def interpret_NEWT1G0(newt_line):
    newt1g0 = NEWT1G0(*newt_line.split()[1:])
    return NEWT1G0_description.format(IFTP1_dict[int(newt1g0.IFTP1)],
                                      newt1g0.FNEWT1,
                                      get_ITP_interpretation(int(newt1g0.ITP1), int(newt1g0.ITP2)),
                                      f"# CLAMP is {newt1g0.CLAMP1}\n" if newt1g0.CLAMP1 else "",
                                      newt_line)

def interpret_NEWT1G1(newt_line):
    newt1g1 = NEWT1G1(*newt_line.split()[1:])
    return NEWT1G1_description.format(IFTP1_dict[int(newt1g1.IFTP1)],
                                      newt1g1.FNEWT1,
                                      f"x/c of {newt1g1.COND1}" if newt1g1.IFTP1=="205" else f"alpha of {newt1g1.COND1} degrees",
                                      get_ITP_interpretation(int(newt1g1.ITP1), int(newt1g1.ITP2)),
                                      f"# CLAMP is {newt1g1.CLAMP1}\n" if newt1g1.CLAMP1 else "",
                                      newt_line)

def interpret_NEWT1S0(newt_line):
    newt1s0 = NEWT1S0(*newt_line.split()[1:])
    return NEWT1S0_description.format(IFTP1_dict[int(newt1s0.IFTP1)],
                                      LLBOS_dict[int(newt1s0.LLBOS)],
                                      newt1s0.JSEGIX1,
                                      newt1s0.FNEWT1,
                                      get_ITP_interpretation(int(newt1s0.ITP1), int(newt1s0.ITP2)),
                                      f"# CLAMP is {newt1s0.CLAMP1}\n" if newt1s0.CLAMP1 else "",
                                      newt_line)

def interpret_NEWT1S1(newt_line):
    newt1s1 = NEWT1S1(*newt_line.split()[1:])
    return NEWT1S1_description.format(IFTP1_dict[int(newt1s1.IFTP1)],
                                      newt1s1.FNEWT1,
                                      LLBOS_dict[int(newt1s1.LLBOS)],
                                      newt1s1.JSEGIX1,
                                      newt1s1.COND1,
                                      get_ITP_interpretation(int(newt1s1.ITP1), int(newt1s1.ITP2)),
                                      f"# CLAMP is {newt1s1.CLAMP1}\n" if newt1s1.CLAMP1 else "",
                                      newt_line)

def interpret_NEWT1S2(newt_line):
    newt1s2 = NEWT1S2(*newt_line.split()[1:])
    return NEWT1S2_description.format(IFTP1_dict[int(newt1s2.IFTP1)],
                                      newt1s2.FNEWT1,
                                      LLBOS_dict[int(newt1s2.LLBOS)],
                                      newt1s2.JSEGIX1,
                                      newt1s2.COND1,
                                      newt1s2.COND2,
                                      get_ITP_interpretation(int(newt1s2.ITP1), int(newt1s2.ITP2)),
                                      f"# CLAMP is {newt1s2.CLAMP1}\n" if newt1s2.CLAMP1 else "",
                                      newt_line)

# ================================== NEWT2.. Interpreter Functions ===================================
def interpret_NEWT2SD0(newt_line):
    newt2sd0 = NEWT2SD0(*newt_line.split()[1:])
    KADJSBS = int(newt2sd0.KADJSBS)

    return NEWT2SD0_description.format(IFTP2_dict[int(newt2sd0.IFTP2)],
                                       newt2sd0.JSEGIX2,
                                       "line" if KADJSBS==1 else f"{KADJSBS} lines",
                                       LLBE_dict[int(newt2sd0.LLBE)],
                                       f"# CLAMP is {newt2sd0.CLAMP1}\n" if newt2sd0.CLAMP1 else "",
                                       newt_line)

def interpret_NEWT2SD1(newt_line):
    newt2sd1 = NEWT2SD1(*newt_line.split()[1:])
    KADJSBS = int(newt2sd1.KADJSBS)

    return NEWT2SD1_description.format(IFTP2_dict[int(newt2sd1.IFTP2)],
                                       newt2sd1.JSEGIX2,
                                       "line" if KADJSBS==1 else f"{KADJSBS} lines",
                                       LLBE_dict[int(newt2sd1.LLBE)],
                                       newt2sd1.R1,
                                       f"# CLAMP is {newt2sd1.CLAMP1}\n" if newt2sd1.CLAMP1 else "",
                                       newt_line)

def interpret_NEWT2SD2(newt_line):
    newt2sd2 = NEWT2SD2(*newt_line.split()[1:])
    KADJSBS = int(newt2sd2.KADJSBS)

    return NEWT2SD2_description.format(IFTP2_dict[int(newt2sd2.IFTP2)],
                                       newt2sd2.JSEGIX2,
                                       "line" if KADJSBS==1 else f"{KADJSBS} lines",
                                       LLBE_dict[int(newt2sd2.LLBE)],
                                       newt2sd2.R1,
                                       newt2sd2.R2,
                                       f"# CLAMP is {newt2sd2.CLAMP1}\n" if newt2sd2.CLAMP1 else "",
                                       newt_line)

def interpret_line(line):
    # NEWT1.. Lines
    if line.startswith("NEWT1G0"): return interpret_NEWT1G0(line)
    if line.startswith("NEWT1G1"): return interpret_NEWT1G1(line)
    if line.startswith("NEWT1S0"): return interpret_NEWT1S0(line)
    if line.startswith("NEWT1S1"): return interpret_NEWT1S1(line)
    if line.startswith("NEWT1S2"): return interpret_NEWT1S2(line)

    # NEWT2.. Lines
    if line.startswith(("NEWT2SD0","NEWT2RD0")): return interpret_NEWT2SD0(line)
    if line.startswith(("NEWT2SD1","NEWT2RD1")): return interpret_NEWT2SD1(line)
    if line.startswith(("NEWT2SD2","NEWT2RD2")): return interpret_NEWT2SD2(line)

    # Not applicable for interpretation
    else: 
        return line

def safe_interpret_line(line):
    """
    Definitions could be partial(undocumented) or code could be erroneous.
    just make the best effort approach here so that the main program won't error out
    """
    try:
        return interpret_line(line)
    except:
        return line

def annotate_text(text):
    lines = text.split("\n")
    output = [safe_interpret_line(line) for line in lines]
    return "\n".join(output)
