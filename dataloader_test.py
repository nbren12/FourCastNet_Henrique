import sys
import os.path
import logging
from utils import logging_utils
logging_utils.config_logger()
from utils.data_loader_multifiles import GetDataset, GetCosmoDataset
import time
import torch

class Params():
    dt = 1
    n_history = 0
    # in_channels  = [0, 1 ,2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    in_channels = ['U_10M', 'V_10M', 'PMSL', 'PS', 'T_2M', 'FI', 'T', 'U', 'u_100', 'V', 'v_100', 'RELHUM']
    out_channels = [0, 1 ,2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    crop_size_x = None
    crop_size_y = None
    roll = False
    two_step_training = False
    orography = False
    add_noise = False
    normalize = False
    global_means_path = None #'/scratch/f1000/dealmeih/ds/FCN/FCN_ERA5_data_v0/global_means.npy'
    global_stds_path  = None #'/scratch/f1000/dealmeih/ds/FCN/FCN_ERA5_data_v0/global_stds.npy'
    add_grid = False
    normalization = 'zscore'

    # invars_2d = ['U_10M', 'V_10M', 'PMSL', 'PS', 'T_2M']
    # invars_3d = ['FI', 'T', 'U', 'u_100', 'V', 'v_100', 'RELHUM']

if __name__ == "__main__":
    params = Params()
    if sys.argv[1] == 'cosmo':
        params.era5 = False
        if len(sys.argv)>3:
            params.normalize = True
            params.global_means_path = os.path.join(str(sys.argv[3]), 'global_means.npy')
            params.global_stds_path  = os.path.join(str(sys.argv[3]), 'global_stds.npy')
        dataset = GetCosmoDataset(params, str(sys.argv[2]), train=False)
    else: # era5
        params.era5 = True
        params.in_channels = params.out_channels
        dataset = GetDataset(params, str(sys.argv[2]), train=False)

    print(len(dataset), torch.std_mean(dataset[0][0][35,:,:])) 
    print(dataset[0][0].shape, dataset[-1][1].shape)

    tstart = time.time()
    cntr = 0
    #for ii in range(0, len(dataset) ,2):
    for ii in range(0, 100, 2):
        dummy = dataset[ii][0].shape
        cntr += 2
        if ii%50==0:
            print('{}MB allocated'.format(torch.cuda.memory_allocated()/1024**2))
    t_tot = time.time() - tstart

    print(f'took {t_tot} to load {cntr} files')
