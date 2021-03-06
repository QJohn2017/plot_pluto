import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import importlib
import os
import pluto_read_frm as prf
from scipy.constants import mu_0
import utilities as ut
import active_plasma_lens as apl
from scipy.interpolate import griddata
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from copy import copy

#plt.close("all")
importlib.reload(prf)
importlib.reload(ut)
importlib.reload(apl)

# <codecell>
# Settings

# ----
sim = ['/home/ema/simulazioni/sims_pluto/perTesi/rho2.53e-7-I500flattop-1.2cmL-1mmD-NEWGRID',
       '/home/ema/simulazioni/sims_pluto/perTesi/rho2.53e-7-I720flattop-1.2cmL-1.2mmD-NEWGRID'
       ]
pluto_nframe = 80
# Capillary length, half of the real one (including electrodes)
l_cap = 0.6e-2  # m
r_cap = (0.5e-3, 0.6e-3)  # m
dz_cap = 1.e-3
name = ('(a)','(b)')

#%% Load the data
if len(sim)!=2:
    raise ValueError('sim must be a list of two(2) simulation paths')
ne = [[], []]
r = [[],[]]
z = [[],[]]
t = [[],[]]
for ss in range(len(sim)):
    pluto_dir = os.path.join(os.path.expandvars(sim[ss]), 'out')
    q, r[ss], z[ss], theta, t[ss], n = prf.pluto_read_vtk_frame(pluto_dir,
                                                                # time=125.0,
                                                                nframe=pluto_nframe)
    ne[ss] = q["ne"]
    # Convert r and z to m
    r[ss] /= 1e5
    z[ss] /= 1e5

#%%
# Compute the cell centers
r_cc = [0.5*(r[ss][1:]+r[ss][:-1]) for ss in (0,1)]
z_cc = [0.5*(z[ss][1:]+z[ss][:-1]) for ss in (0,1)]

#%% Plotting
gs = gridspec.GridSpec(2, 2,
                       width_ratios=[30, 2],
                       height_ratios=[1, 1]
                       )

fig = plt.figure(figsize=(5.5,4.5))
ax = [[],[]]
ax[0] = plt.subplot(gs[0,0])
ax[1] = plt.subplot(gs[1,0])
ax_cb = plt.subplot(gs[:,1])

ne_logmin = 8
ne_logmax = 18
ne_plot = ne.copy()
for ss in (1,0):
    ne_plot[ss][ne_plot[ss]<1e8] = 1e8
for ss in (0,1):
    ax[ss].set_facecolor('k')
    mp = ax[ss].contourf(z_cc[ss]*1e2, r_cc[ss]*1e6,
                         np.log10(ne[ss].T),
                         levels=np.linspace(ne_logmin, ne_logmax, 150),
                         # locator=ticker.LogLocator(),
                         # norm = colors.LogNorm(vmin=vmin, vmax=vmax),
                         vmin = ne_logmin,
                         vmax = ne_logmax,
                         cmap = 'inferno')
ax[1].set_ylim(0., 2e3)
ax[0].set_ylim(0.,2e3)
for ss in (0,1):
    ax[ss].set_xlim(0.01,2.)
ax[1].set_xlabel('z (cm)')
ax[0].set_ylabel('r (μm)')
ax[1].set_ylabel('r (μm)')

cbar = fig.colorbar(mp, cax = ax_cb,
             label='Electron density $(\mathrm{cm}^{-3})$',
             ticks = [8,10,12,14,16,18])
cbar.set_ticklabels(['$<10^8$', '$10^{10}$', '$10^{12}$', '$10^{14}$', '$10^{16}$', '$10^{18}$'])

# ----
# Draw electrodes and capillary walls
# Locations of lower left corners of electrodes z(m),r(m) (one for each sim)
electrode_zr_ll = (((l_cap-dz_cap)*1e2, r_cap[0]*1e6),  # sim 0
                   ((l_cap-dz_cap)*1e2, r_cap[1]*1e6))  # sim 1
wall_zr_ll = ((0, r_cap[0]*1e6),  # sim 0
              (0, r_cap[1]*1e6))  # sim 1

electrodes = [Rectangle((electrode_zr_ll[ss][0], electrode_zr_ll[ss][1]), dz_cap*1e2, r[ss].max()*1e6,
                        fill=True, facecolor='#a3552c', edgecolor='k' ) for ss in (0,1)]
walls = [Rectangle((wall_zr_ll[ss][0], wall_zr_ll[ss][1]), (l_cap-dz_cap)*1e2, r[ss].max()*1e6,
                        fill=True, facecolor='gray', edgecolor='k' ) for ss in (0,1)]
for ss in (0,1):
    ax[ss].add_patch(electrodes[ss])
    ax[ss].add_patch(walls[ss])
# el_coll = PatchCollection([el], facecolor='r',
#                           alpha = 0.99,
#                           edgecolor='g')
# ax[0].add_collection(el_coll)

# ----
for ss in (0,1):
    ax[ss].set_title(name[ss]+', t={:g}ns'.format(t[0]))
fig.tight_layout()
plt.show()
# rr = [[],[]]
# zz = [[],[]]
# for ss in (0,1):
#     rr[ss], zz[ss] = np.meshgrid(r[ss], z[ss])
#
# fig, ax = plt.subplots()
# ss = 0
# ax.pcolormesh(rr[0], zz[0], ne_cc[0])
# ax.pcolormesh(rr[0], zz[0], ne[0])
