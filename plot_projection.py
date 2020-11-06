import os, sys
import numpy as np
from load_data impoirt load_snapshot_data_distributed


#Load Snapshot Data
dataDir = '/data/groups/comp-astro/bruno/'

uvb = 'pchw18'
# uvb = 'hm12'
inDir = dataDir + f'cosmo_sims/2048_hydro_50Mpc/output_files_{uvb}/'


n_snapshot = 118

data_type = 'hydro'
# data_type = 'particles'

fields = ['temperature']

precision = np.float32

Lbox = 5000    #kpc/h
proc_grid = [ 8, 8, 8]
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ 2048, 2048, 2048 ] #Size of the simulation grid
subgrid = [ [0, 2048], [0, 2048], [0, 2048] ] #Size of the volume to load
data = load_snapshot_data_distributed( n_snapshot, inDir, data_type, fields, subgrid,  precision, proc_grid,  box_size, grid_size, show_progess=True )
temperature = data[data_type]['temperature']  


