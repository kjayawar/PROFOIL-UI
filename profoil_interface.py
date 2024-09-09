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

# This modules interfaces PROFOIL-UI with PROFOIL.
# One design feature was to have a clear separation between the input and output of PROFOIL has been maintained
# meaning profoil.in file has nothing to do with what is been extracted to do the plots and vice versa. 
# For each output file [profoil.xy, profoil.dmp, profoil.vel] there exists a corresponding extract_{} function,
# which extracts the required information from the files with the following data types.

# +-------------+---------------+----------------+
# | File        | Data          | Extracted Type |
# +-------------+---------------+----------------+
# | profoil.xy  | x coordinates | numpy_array    |
# |             | y coordinates | numpy_array    |
# +-------------+---------------+----------------+
# | profoil.dmp | nu            | numpy_array    |
# |             | alfa          | numpy_array    |
# |             | ile           | int            |
# |             | phi_S         | float          |
# +-------------+---------------+----------------+
# | profoil.vel | phi           | numpy_array    |
# |             | v/v_inf       | numpy_array    |
# +-------------+---------------+----------------+

# As for the input, the main functionality is encapsulated into gen_input_template(...), and gen_input_file(...) functions. 
# The first one creates a substitutable string by de-voiding FOIL and ILE lines mainly.
# Please note – All the FOIL lines are supposed to be placed in one place without empty lines.

import re
import numpy as np
from io import StringIO
from scipy.interpolate import interp1d
import os


from preferences import *

from pathlib import Path
import shutil

WORKDIR = Path(WORK_DIR).resolve()   # using absolute paths
BINDIR  = Path(BIN_DIR).resolve()    # using absolute paths
EXEC_ABS_PATH = str(BINDIR/"{}".format("profoil.exe" if os.name == "nt" else "./profoil"))

def extract_alphas(filename=WORKDIR/"profoil.in"):
    """
    Extracts design alpha values from the profoil.in file
    This functions is not currently being used but could
    be useful if alphas to be included as a legend
    in the velocity plot
    """
    alphas = []
    lines = open(filename).readlines()
    for i, line in enumerate(lines):
        if line.startswith("ALFASP "):
            n = int(re.findall("ALFASP\s+(\d+)", line)[0])
            for j in range(n):
                alphas.append(float(lines[i+j+1]))
    assert len(alphas) == n
    return alphas

def extract_xy(filename=WORKDIR/"profoil.xy"):
    """
    Extracts  x,y data from profoil.xy file
    """
    x,y = np.loadtxt(filename).T
    return x,y

def extract_vel(filename=WORKDIR/"profoil.vel"):
    """
    Extracts v/v_inf data from profoil.vel file
    First column is expected to carry "phi" data
    generated with VELDIST 60
    """
    phi, v_vinf= np.loadtxt(filename).T
    return phi, v_vinf

def extract_dmp(filename=WORKDIR/"profoil.dmp"):
    """
    Extracts the converged nu-alpha* pairs, LE index,
    and recovery parameters from the profoil.dump file.
    regex is used exclusively for all extractions
    with multi-line flag.
    """
    text = open(filename).read()
    foil_section = re.findall(r"^FOIL.*(?:\nFOIL.*)*$", text, flags = re.M)[0]
    nu, alfa = np.loadtxt(StringIO(foil_section), usecols=(1,2)).T
    ile = int(re.findall(r"^ILE\s+(\d+)", text, flags=re.M)[0])
    phis = [float(i) for i in re.findall(r"^PHIS\s+(.*)", text, flags=re.M)[0].split()]
    return nu, alfa, ile, phis

def split_vel(phi, v_vinf):
    """
    PROFOIL writes Non-dimensionalized velocities over the airfoil contour
    in a continuous stream of numbers without breaks for each AoA. 
    This continuous stream is split into a list of phi-v/v_inf pairs 
    using phi==0 (start of each AoA) locators. 

    PS: Splitting into fixed length chunks won't work here because depending 
    on the placement of the LE stagnation point, an additional point may or
    may not be added in to the stream.
    """
    breaks  = np.argwhere(phi==0).flatten()[1:]
    phi_list= np.split(phi, breaks)
    vel_list= np.split(v_vinf, breaks)
    return phi_list, vel_list

def gen_vel_splines(phi_list, vel_list):
    """
    Takes a list of phi-v/v_inf pairs and creates a spline for each
    phi-v/v_inf distribution. These splines will be used to locate the 
    phi markers on the upper and lower surfaces.
    """
    return [interp1d(phi,v, fill_value='extrapolate') for phi,v in zip(phi_list, vel_list)]

def gen_phi2xy_splines(x, y):
    """
    Creates 2 splines which maps;
    phi->x 
    phi->y
    x,y coordinates are taken from profoil.xy file and equidistant phi distribution is presumed.
    """
    phis = np.linspace(0,360, len(x))
    return interp1d(phis,x, fill_value='extrapolate'), interp1d(phis,y, fill_value='extrapolate')

def extract_all_data():
    """
    This lengthy function could be somewhat problematic to understand at the first glance;
    hence the below diagram for better clarity.

          +-----------+  +-----------+      +-----------+
          |profoil.xy |  |profoil.dmp|      |profoil.vel|
          +-----------+  +-----------+      +-----------+
              |   |            |               |     |
              v   v            v               v     v
            +--++--+  +--------------------+ +---++---------+
            | x||y |  |phi alpha ile phi_S | |phi||v/v_inf  |
            +--++--+  +--------+-----------+ +---++---------+
               |               |               |     |
               v               |               v     v
       +-------+-------+       |       +---------++-----------+
    +--+ phi2x |phi2y  +---+   |       | phi_list||vv_inf_list|
    |  +-------+-------+   |   |       ++--------++-----------+
    |          |           |   |        |          |
    |          v        +--v---v------+ |          v
    |    +-----------+  |lower_markers| | +------------------+
    |    | xy_markers|  |upper_markers| | | phi2v_spline_list|
    |    +-----------+  +-------------+ | +------------------+
    |                                   |          |
    |                                   |          v
    |                                   |     +--------+
    +-----------------------------------+---->|ue_lines|
                                              +--------+

    main point to understand is, whatever the data not represented as f(x) has to be
    transformed into f(x), using splines in the form of spl(phi). popular interp1d spline
    is used here which appears to work without any issue given phi increases monotonically.
    Additionally, for the airfoil contour, x(phi) and y(phi) has to be constructed because
    the markers are given in phi. 
    """

    # extract row data from output files
    phi, vel = extract_vel()
    nu, alfa, ile, (phis_upper, phis_lower) = extract_dmp()
    x,y = extract_xy()

    # create splines
    phi2x_spline, phi2y_spline = gen_phi2xy_splines(x,y)
    phi_list, vel_list = split_vel(phi, vel)
    phi2v_spline_list = gen_vel_splines(phi_list, vel_list)

    design_alphas = range(len(phi_list))
    # design_alphas is just a dummy alpha list.
    # this can be replaced with extract_alphas() if needed
    # but this will place a constraint on having alphas listed in the .in file.
    # since listing alphas in the plot is not mandatory, a simple range would work here

    # creates x-v/v_inf distribution from phi-v/v_inf distribution using phi2x_spline.
    ue_lines =  {alfa:{"x": phi2x_spline(phi), "v_vinf": spl(phi)} 
                 for alfa, phi, spl 
                 in zip(design_alphas, phi_list, phi2v_spline_list)}

    # creates a list of phi values corresponding to FOIL lines.
    # This is done by transforming the FOIL line phi by a constant factor NU2PHI
    # caution; these markers are not sorted - since they will be plotted as scatter.

    NU2PHI = 6 # degrees around the circle / nu_max in the FOIL lines which is 60.

    nu_upper = nu[:ile].tolist()
    alfa_upper = alfa[:ile].tolist()
    upper_markes_phi = np.array([phis_upper] + nu_upper) * NU2PHI

    nu_lower = nu[ile:].tolist()
    alfa_lower = alfa[ile:].tolist()
    lower_markes_phi = np.array(nu_lower + [phis_lower]) * NU2PHI

    # Triangular marker positions on upper and lower surfaces are determined using the previously
    # transformed phi values. This is done on upper and lower surface velocity distributions
    # and upper and lower x,y coordinates.

    upper_vel_markers = {alfa:{"x": phi2x_spline(upper_markes_phi), "v_vinf": spl(upper_markes_phi)} 
                    for alfa, spl 
                    in zip(design_alphas, phi2v_spline_list)}

    lower_vel_markers = {alfa:{"x": phi2x_spline(lower_markes_phi), "v_vinf": spl(lower_markes_phi)} 
                    for alfa, spl 
                    in zip(design_alphas, phi2v_spline_list)}

    xy_marker_upper = {"x" : phi2x_spline(upper_markes_phi) , "y": phi2y_spline(upper_markes_phi)}
    xy_marker_lower = {"x" : phi2x_spline(lower_markes_phi) , "y": phi2y_spline(lower_markes_phi)}

    return  x,y, xy_marker_upper, xy_marker_lower, \
            ue_lines, upper_vel_markers, lower_vel_markers, \
            nu_upper, alfa_upper, nu_lower, alfa_lower, ile

def gen_input_template(filename=WORKDIR/"profoil.in"):
    """
    Takes profoil.in file and devoid the FOIL section containing
    nu-alpha* block along with ILE line so that these 2 sections
    can then be filled up by profoil-ui data
    As a precautionary measure, VELDIST will be set to 60 as well.
    """
    file_content            = open(filename).read()
    foils_blk_devoided      = re.sub(r"^FOIL.*(?:\nFOIL.*)*$", r"{}",   file_content,       flags=re.M, count=1)
    foils_ile_devoided      = re.sub(r"(^ILE\s+)\d+",          r"\1{}", foils_blk_devoided, flags=re.M, count=1)
    foils_ile_vdist_fixed   = re.sub(r"^VELDIST\s+\d+",  r"VELDIST 60", foils_ile_devoided, flags=re.M, count=1)
    return foils_ile_vdist_fixed

def gen_foil_line(nu, alpha, i, ile, delta_alpha=0):
    """
    generates a foil line with ILE marker for easy REF
    """
    return "FOIL{:12.5f}{:12.5f}{:5d}{:4d}{}".format(nu, alpha, i, delta_alpha, 
                                                    "  <--- ILE" if i == ile else "")

def gen_input_file(nu_list, alpha_list, ile):
    """
    Generates profoil.in file using passed nu-alpha pairs and LE seg.
    Only the FOIL section and ILE will be updated 
    while keeping the rest of the original profoil.in file intact.
    """
    file_template = gen_input_template()
    foils_section = "\n".join([gen_foil_line(nu, alpha, i, ile) 
                                for i, (nu, alpha) 
                                in  enumerate(zip(nu_list,alpha_list), start=1)])

    save2profoil_in(file_template.format(foils_section, ile))

def save2profoil_in(text, filename=WORKDIR/"profoil.in"):
    """
    saves changes to the profoil.in file if the contents were actually altered.
    """

    # bug fix -- 26/Jul/2024
    # https://www.rcgroups.com/forums/showpost.php?p=52737531&postcount=95
    # could have used 'a+' flag for edge case of non-existing file with one open call 
    # but seek(0) would make it vulnerable in some unix based systems.

    f_handle = Path(filename)
    if (f_handle.is_file() and f_handle.open('r').read() == text): return
    with f_handle.open("w") as f:
        f.write(text)   

def is_design_converged(filename=WORKDIR/"profoil.log"):
    """
    Upon running PROFOIL.exe this function examines profoil.log file 
    for successful completion of airfoil design.
    Note: 
    Probably its best to check for "STATISTICS" line instead.
    Because there could be errors in calculations in VELDIST for ex:
    even after the design is converged
    """
    return "AIRFOIL DESIGN IS FINISHED" in open(filename).read()

def exec_profoil():
    """
    Executes PROFOIL.exe located in the BINDIR
    chdir found to be required to do this without using subprocess.
    """
    os.chdir(WORKDIR)
    os.system("{} > profoil.log".format(EXEC_ABS_PATH))

def extract_summary(filename=WORKDIR/"profoil.log"):
    """
    Extracts the summary portion from the log file. 
    If airfoil name is prescribed in the *.in file the name will be extracted too
    """
    text = open(filename).read()
    stats = re.findall('\*{5}STATISTICS\*{5}\n(.*)|$', text, flags=re.DOTALL)[0]
    airfoil_name = re.findall("Airfoil Name:(.*)|$", text)[0].strip()
    
    # Strip spaces from each line of stats
    stripped_stats = "\n".join(line.strip() for line in stats.splitlines())
    return f"{airfoil_name}\n\n{stripped_stats}"

"""
Below utility functions are self explanatory. 
They just move the files from BIN directory to WORK directory and vise versa.
shutil is used to keep the generality between platforms.
"""
def gen_buffer():
    shutil.copy(WORKDIR/"profoil.in", WORKDIR/"buffer.in")

def swap_buffer():
    shutil.copy(WORKDIR/"profoil.in", WORKDIR/"temp.in")
    shutil.copy(WORKDIR/"buffer.in",  WORKDIR/"profoil.in")
    shutil.copy(WORKDIR/"temp.in",    WORKDIR/"buffer.in")

def catfile(filename, tail=0):
    """
    Equivalent to linux 'cat' command. option 'tail' is to specify
    the number of tail lines to show. tail=0 means the whole file
    will be displayed.
    """
    lines = Path(filename).open().readlines()
    return "".join(lines[-tail:])
