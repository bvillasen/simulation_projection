import os, sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from load_data import load_snapshot_data_distributed
from turbo_cmap import *
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
  projection_mean = temperature[:projection_width,:,:].sum(axis=0)
  projection2     = (temperature[:projection_width,:,:]**2).sum(axis=0)
  prejection      = projection2 / projection_mean
  projections[uvb] = np.log10(projection)




min_val = min( projections['pchw18'].min(), projections['hm12'].min() )
max_val = max( projections['pchw18'].max(), projections['hm12'].max() ) 
print( f' min:{min_val}    max:{max_val})


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
  
colormap = 'turbo'

ax = grid[0]
im = ax.imshow( projections['hm12'],   vmin=min_val, vmax=max_val, cmap=colormap, extent=(0, 50., 0, 50) )
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

ax = grid[1]
im = ax.imshow( projections['pchw18'],   vmin=min_val, vmax=max_val, cmap=colormap, extent=(0, 50., 0, 50) )
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

cb = ax.cax.colorbar( im  )

font = {'fontname': 'Helvetica',
    'color':  'black',
    'weight': 'normal',
    'size': 24,
    'ha':'center'
    }
cb.set_label_text( r'$\mathrm{log_{10}}  \,\,\,\, \mathrm{Temperature} \,\,\,\,\,[ \mathrm{K}  ] $', fontdict=font )
 
fig.tight_layout()
fileName = 'projections.png'
fig.savefig( fileName,  bbox_inches='tight',  dpi=600, pad_inches=-0.05 )
print('Saved image: ', fileName)