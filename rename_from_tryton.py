import os

# input file names:
# rho_[ptype_number]_[computation_type]_[file_nuber]_[direction_number].dat

# desired output file names:
#
# rho_[particle_type]_[computation_type]_[direction]_[file_number].dat
#
# given by user:
# particle_type   = fluid, St0.2, St05. St1, St5, St25, St125
# coputation_type = SGSles, LES
#
# deduced from input:
# direction: (1 -> y)
#            (2 -> z)
#            (3 -> x)
# file_number

direction_dict = {'1':'y',
                  '2':'z',
                  '3':'x'}

ptype_dict = {'1':'fluid',
              '2':'fluid',
              '3':'fluid',
              '4':'fluid'}


def name_change(fname):

    fname_tab    = fname.split('_')
    fname_tab[4] = fname_tab[4][0]
  
    new_name = fname_tab[0] + '_' + ptype_dict[fname_tab[1]] + '_'\
               + fname_tab[2] + '_' + direction_dict[fname_tab[4]]\
               + '_' + fname_tab[3] + '.dat'

    return new_name


if __name__=='__main__':

    file_path             = os.path.expanduser("~") + '/wyniki/time_scales_ii/'
    file_path_from_tryton = file_path + 'tryton/'
    rho_files             = [filename for filename in os.listdir(file_path_from_tryton) if filename.startswith("rho_")]


    for f in rho_files:

        infile  = file_path_from_tryton + f
        outfile = file_path + name_change(f)
        os.rename(infile,outfile)

