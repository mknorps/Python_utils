###############################################
#
#  mknorps, 11.11.2017
#
#  script for convergence check of particles 
#         simulations
#
#
###############################################


import struct
import os
import csv

import numpy as np
# import matplotlib.pyplot as plt


# files are written in fortran with :
'''
       write(3)t
       write(3)time
       write(3)pos
       write(3)vpar
       write(3)upar
       write(3)usgs

fortran inserts integer*4 byte at beginning and end of each unformatted wrie statement

t        : integer
time     : real*8
pos,usgs : real*8 [400000,3]
vpar,upar: real*8 [400000,4]

400000 particles - 4 types of particles 100000 of each

'''
N     = 400000
N_par = 100000 #number of particles of one kind

# bins for histograms are taken according to eros of Chebyshev
#      polynomials
N_bins = 32
def y_plus(j):
    return np.cos(float(j)*np.pi/float(N_bins))
bins = list(reversed([y_plus(j)*150 for j in range(N_bins/2+1 )]))

def unpack_particles_file(f):
    
    t    =  struct.unpack("i", f[4:8])
    time =  struct.unpack("d", f[16:24])

    pos_byte_min = 24+8
    pos_byte_max = pos_byte_min + 400000*3*8
    pos  =  np.transpose(np.array(struct.unpack("d" * (400000*3), f[pos_byte_min:pos_byte_max])).reshape((3,400000)))

    vpar_byte_min = pos_byte_max+8
    vpar_byte_max = vpar_byte_min + 400000*4*8
    vpar  =  np.transpose(np.array(struct.unpack("d" * (400000*4), f[vpar_byte_min:vpar_byte_max])).reshape((4,400000)))

    upar_byte_min = vpar_byte_max+8
    upar_byte_max = upar_byte_min + 400000*4*8
    upar  =  np.transpose(np.array(struct.unpack("d" * (400000*4), f[upar_byte_min:upar_byte_max])).reshape((4,400000)))

    usgs_byte_min = upar_byte_max+8
    usgs_byte_max = usgs_byte_min + 400000*3*8
    usgs  =  np.transpose(np.array(struct.unpack("d" * (400000*3), f[usgs_byte_min:usgs_byte_max])).reshape((3,400000)))

    return {"t":t,"time":time,"pos":pos,"vpar":vpar,"upar":upar,"usgs":usgs}

def concentration_profiles(pos_wallnormal):
    
    N_types = N/N_par
    histograms = {}

    for p_type in range(N_types):

        particles      = np.array(pos_wallnormal[p_type*N_par:(p_type+1)*N_par])
        particles_symm = 150 * (1.0 - np.absolute(particles)) # non-dimension
        hist           = np.histogram(particles_symm, bins = bins, normed=True)
        histograms[p_type] = hist[0]
   
    return histograms


def first_bin_comparison(conc_dict,p_type, bin_id = 0):

    fbc = {}
    for p_field,conc in conc_dict.items():

        fbc[p_field] = conc[p_type][bin_id]

    return fbc

'''
def draw_convergence(conv_check,filepath):

    fig2=plt.figure()
    ax1 = fig2.add_subplot(111)  
    ax1.set_xlabel('file no.')
    ax1.set_ylabel('$1^{st}$ bin')

    ax1.plot(conv_check.keys(),conv_check.values())

    plt.savefig(filepath)
    plt.close(fig2)
'''

##################################################################################



if __name__=='__main__':
    
    # file names
    file_path      = os.path.expanduser("~") + '/LES_COR/DATA/'
    particle_files = [filename for filename in os.listdir(file_path) if filename.startswith("particles_")]

    concentration = {}
 
    for particle_file in particle_files:
        with open(file_path+particle_file, mode='rb') as file: # b is important -> binary
            data_bin = file.read()
            data_hrf = unpack_particles_file(data_bin) # humad readable format

            concentration[particle_file[10:]] = concentration_profiles(data_hrf["pos"][:,0])

    convergence_check = first_bin_comparison(concentration,0)


#    draw_convergence(convergence_check,file_path+"conv_check.eps")

    with open(file_path+'conv_check.csv', 'w') as f:
        writer = csv.writer(f)
        rows = convergence_check.iteritems()
        writer.writerows(rows)
