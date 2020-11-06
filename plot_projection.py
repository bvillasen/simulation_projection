import os, sys
import numpy as np
from load_data import load_snapshot_data_distributed


#Load Snapshot Data
dataDir = '/data/groups/comp-astro/bruno/'

uvb = 'pchw18'
# uvb = 'hm12'


n_snapshot = 131
projection_width = 512

data_type = 'hydro'
fields = ['temperature']
precision = np.float32

Lbox = 5000    #kpc/h
proc_grid = [ 8, 8, 8]
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ 2048, 2048, 2048 ] #Size of the simulation grid
subgrid = [ [0, projection_width], [0, 2048], [0, 2048] ] #Size of the volume to load


projections = {}
for uvb in [ 'pchw18', 'hm12']:
  inDir = dataDir + f'cosmo_sims/2048_hydro_50Mpc/output_files_{uvb}/'
  data = load_snapshot_data_distributed( n_snapshot, inDir, data_type, fields, subgrid,  precision, proc_grid,  box_size, grid_size, show_progess=True )
  current_z = data['Current_z']
  temperature = data[data_type]['temperature']  
  projection = temperature[:projection_width,:,:].sum(axis=0)
  projections[uvb] = projection

