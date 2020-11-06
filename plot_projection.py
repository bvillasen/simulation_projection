import os, sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from load_data import load_snapshot_data_distributed
import matplotlib
matplotlib.use('Agg') 

#Load Snapshot Data
dataDir = '/data/groups/comp-astro/bruno/'

uvb = 'pchw18'
# uvb = 'hm12'


n_snapshot = 131
projection_width = 256

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


n_cols, n_rows = 2, 1
fig = plt.figure(0, figsize=(12*n_cols,10*n_rows),  )
grid = ImageGrid(fig, 111,          # as in plt.subplot(111)
                 nrows_ncols=(n_rows,n_cols),
                 axes_pad=0.2,
                 share_all=True,
                 cbar_location="right",
                 cbar_mode="single",
                 cbar_size="7%",
                 cbar_pad=0.1,
                 )
  


fig.tight_layout()
fileName = 'projections.png'
fig.savefig( fileName,  bbox_inches='tight',  dpi=900, pad_inches=-0.0 )
print('Saved image: ', fileName)