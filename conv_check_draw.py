import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd

file_dir = '/home/gemusia/wyniki/conv_check/LES/'


def conv_draw(data,filepath):

    fig2=plt.figure()
    ax1 = fig2.add_subplot(111)  
    ax1.set_xlabel('file no.')
    ax1.set_ylabel('$1^{st}$ bin')

    ax1.plot(data['file no.'],data['1st bin hist'])

    plt.savefig(filepath)
    plt.close(fig2)



if __name__=='__main__':

    conv_file = file_dir + 'conv_check.csv'
    conv_pict_path = file_dir + 'conv_check.png'

    conv = pd.read_csv(conv_file,names=['file no.','1st bin hist'])
    conv.sort_values('file no.',inplace=True)

    conv_draw(conv,conv_pict_path)
