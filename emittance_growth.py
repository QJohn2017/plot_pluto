# -*- coding: utf-8 -*-

import numpy as np
import scipy.constants as cst
import matplotlib.pyplot as plt
from matplotlib import gridspec
import importlib
import os
import pluto_read_frm as prf
from scipy.constants import mu_0
import utilities as ut
import active_plasma_lens as apl

#plt.close("all")
importlib.reload(prf)
importlib.reload(ut)
importlib.reload(apl)

# electron rest energy in MeV
me_MeV = 0.511

#%% Setting
paper_emulate = 'Pompili2017'
# paper_emulate = 'Pompili2018'

# #sim = '/home/ema/simulazioni/sims_pluto/dens_real/1.3e5Pa-1.2cm'
# ---

pluto_nframes = list(range(0,241,5))  # list(range(0,301,10))
time_unit_pluto = 1e-9  # unit time in pluto's simulation (in s)

# ----- Beam -----
# Normalized emittance (m*rad)
if paper_emulate == 'Pompili2018':
    emitt_Nx = 0.8e-6
    emitt_Ny = 0.5e-6
    energy_MeV = 127
    # NB: l'aumento di emitt cambia molto al variare di d_sigma_x
    #sigma_x = 100.e-6
    sigma_x = 110.e-6
    sigma_y = sigma_x
    d_sigma_x = -(113.-105.)/25.*1.e-4
    d_sigma_y = d_sigma_x
    # NB: l'aumento di emitt cambia poco al variare di d_sigma_x (varia anche se decommento qualche riga qui sotto)
    #d_sigma_x -= d_sigma_x*0.5
    #d_sigma_x+-= d_sigma_x*0.5
    #d_sigma_x = 0.0
    l_cap = 3.2e-2  # m
    r_cap = 0.5e-3  # m
    sim = '/home/ema/simulazioni/sims_pluto/perTesi/rho2.53e-7-I235-3.2cmL-1mmD-r60'
    # sim = '/home/ema/simulazioni/sims_pluto/perTesi/rho8e-7-I235-3.2cmL-1mmD'
    # sim = '/home/ema/simulazioni/sims_pluto/perTesi/rho8e-8-I235-3.2cmL-1mmD'
    # sim = '/home/ema/simulazioni/sims_pluto/perTesi/600mbar-I235-3.2cmL-1mmD'
    Dz = 20e-2  # meters

elif paper_emulate == 'Pompili2017':
    emitt_Nx = 1.e-6
    emitt_Ny = emitt_Nx
    energy_MeV = 126
    sigma_x = 130.e-6
    sigma_y = sigma_x
    # d_sigma_x = 0
    d_sigma_x = -(130.-112.)/20.*1.e-4  # Circa... (vedi Fig 6b. sigma(z=9cm)=200um, sigma(z=11cm)=150um -> sigma'=Dsigma/Dz=25*10^-4)
    # d_sigma_x = (128-130)*1e-6/(15e-3)  # Circa.. per tenere in conto passive focusing
    d_sigma_y = d_sigma_x
    l_cap = 3.2e-2  # m
    r_cap = 0.5e-3  # m
    # Emittance MEASURED (and respective timing w.r.t. discharge peak) after capillary
    emitt_Nx_new_meas = np.loadtxt('/home/ema/Dottorato/dati_sperimentali_e_calcoli/Tabulazione_esperimAPL/ArticoloPompili2017/extracted_data/emitt_x.dat')
    errorbars_Nx_new_meas = [0.01,0.2,1.75,0.2]
    errorbars_Ny_new_meas = [0.01,0.35,1.7,0.15]
    emitt_Ny_new_meas = np.loadtxt('/home/ema/Dottorato/dati_sperimentali_e_calcoli/Tabulazione_esperimAPL/ArticoloPompili2017/extracted_data/emitt_y.dat')
    # Spot MEASURED (and respective timing w.r.t. discharge peak) after capillary
    sigma_x_new_meas = np.loadtxt('/home/ema/Dottorato/dati_sperimentali_e_calcoli/Tabulazione_esperimAPL/ArticoloPompili2017/extracted_data/spot_x.dat')
    sigma_y_new_meas = np.loadtxt('/home/ema/Dottorato/dati_sperimentali_e_calcoli/Tabulazione_esperimAPL/ArticoloPompili2017/extracted_data/spot_y.dat')
    # sim = '/home/ema/simulazioni/sims_pluto/perTesi/rho8e-8-I90-3.2cmL-1mmD'
    sim = '/home/ema/simulazioni/sims_pluto/perTesi/rho4.5e-7-I90-3.2cmL-1mmD-r60-NTOT16-diffRecPeriod8'
    # sim = '/home/ema/simulazioni/sims_pluto/perTesi/rho4e-6-I90-3.2cmL-1mmD-r60-NTOT16-diffRecPeriod8/'
    # sim = '/home/ema/simulazioni/sims_pluto/perTesi/rho2.5e-6-I90-3.2cmL-1mmD-r60-NTOT16-diffRecPeriod8/'
    # sim = '/home/ema/simulazioni/sims_pluto/perTesi/rho6e-6-I90-3.2cmL-1mmD-r60-NTOT16-diffRecPeriod8/'
    # sim = '/home/ema/simulazioni/sims_pluto/perTesi/rho8e-6-I90-3.2cmL-1mmD'
    # sim = '/home/ema/simulazioni/sims_pluto/perTesi/200mbarOKselfmade-I90-3.2cmL-1mmD-r60-NTOT16-diffRecPeriod8'
    # sim = '/home/ema/simulazioni/sims_pluto/perTesi/300mbarOK-I90-3.2cmL-1mmD-r60-NTOT16-diffRecPeriod8'
    # sim = '/home/ema/simulazioni/sims_pluto/perTesi/100mbarOK-I90-3.2cmL-1mmD-r60-NTOT16-diffRecPeriod8'
    # sim = '/home/ema/simulazioni/sims_pluto/perTesi/rho2.53e-7-I90-3.2cmL-1mmD-r60-NTOT8'
    # sim = '/home/ema/simulazioni/sims_pluto/perTesi/rho8e-7-I90-3.2cmL-1mmD'
    # sim = '/home/ema/simulazioni/sims_pluto/perTesi/rho8e-6-I90-3.2cmL-1mmD'
    Dz = 18.5e-2  # meters
else :
    raise ValueError('Wrong choice for paper to emulate')

#%% Computations
# Number of particles in beam
Npart = 10000
gamma = energy_MeV/me_MeV

# Build x distribution ---
emitt_x = emitt_Nx/gamma
x, xp = apl.generate_beam_transverse(sigma_x, d_sigma_x, emitt_x, Npart)
# Build y distribution ---
emitt_y = emitt_Ny/gamma
y, yp = apl.generate_beam_transverse(sigma_y, d_sigma_y, emitt_y, Npart)

# Clean particles outside capillary
idx_part_outside_cap = np.argwhere(x**2+y**2 > r_cap**2)
print('{} of {} beam particles are ouside capillary, I remove them.'.format(np.sum(idx_part_outside_cap),
                                                                            Npart))
x, xp, y, yp = tuple(map(lambda v: np.delete(v, idx_part_outside_cap),
                         (x, xp, y, yp)))

#%% Particles pass in real APL
times, r_c, g_real, Dg_real = apl.g_Dg_time_evol(sim, pluto_nframes, r_cap, l_cap)
times = times*time_unit_pluto

sigma_x_new = [None]*len(pluto_nframes); emitt_x_new = [None]*len(pluto_nframes)
x_new = [None]*len(pluto_nframes); xp_new = [None]*len(pluto_nframes)
y_new = [None]*len(pluto_nframes); yp_new = [None]*len(pluto_nframes)
for tt in range(len(pluto_nframes)):
    (sigma_x_new[tt],
     emitt_x_new[tt],
     x_new[tt],
     xp_new[tt],
     y_new[tt],
     yp_new[tt]) = apl.focus_in_thick_apl(g_real[:,tt], r_c, x, xp, y, yp, l_cap, gamma, Dz)
emitt_Nx_new = np.array(emitt_x_new)*gamma
sigma_x_new = np.array(sigma_x_new)

# Get current set in simulation
t, I = ut.get_currtab(sim)

#%% Particles pass in ideal APL
I_at_times = np.interp(times, t, I)

g_ideal = np.tensordot((cst.mu_0*I_at_times)/(2*np.pi*r_cap), 1/r_c[1:], axes=0).T
# g_ideal = (cst.mu_0*I)/(2*np.pi*r_cap)/r_c
# times, r_c, g_ideal = (r_cap, l_cap)

sigma_x_new_ideal = [None]*len(pluto_nframes); emitt_x_new_ideal = [None]*len(pluto_nframes)
x_new_ideal = [None]*len(pluto_nframes); xp_new_ideal = [None]*len(pluto_nframes)
y_new_ideal = [None]*len(pluto_nframes); yp_new_ideal = [None]*len(pluto_nframes)
for tt in range(len(pluto_nframes)):
    (sigma_x_new_ideal[tt],
     emitt_x_new_ideal[tt],
     x_new_ideal[tt],
     xp_new_ideal[tt],
     y_new_ideal[tt],
     yp_new_ideal[tt]) = apl.focus_in_thick_apl(g_ideal[:,tt], r_c[1:], x, xp, y, yp, l_cap, gamma, Dz)
sigma_x_new_ideal = np.array(sigma_x_new_ideal)

# Fix emittance measurement to fit with the present ordering and conventions
# Get dt to shift data (my data is time shifted w.r.t. the articles (they put t=0 at max I))
dt = t[np.argmax(I)]
def convert_emitt_meas(emitt_N_new_meas, dt):
    ''' Fix eamittance measurement to fit with the present ordering and conventions'''
    idx_ord_emitt = np.argsort(emitt_N_new_meas[:,0])
    emitt_N_new_meas = emitt_N_new_meas[idx_ord_emitt,:]
    # Convert time to seconds as the rest of the data I have here
    emitt_N_new_meas[:,0] *= 1e-9
    emitt_N_new_meas[:,0] += dt
    emitt_N_new_meas = emitt_N_new_meas[:-1,:]
    emitt_N_new_meas[:,1] = emitt_N_new_meas[:,1]*1e-6
    return emitt_N_new_meas
emitt_Nx_new_meas = convert_emitt_meas(emitt_Nx_new_meas, dt)
emitt_Ny_new_meas = convert_emitt_meas(emitt_Ny_new_meas, dt)

# Fix spot measurement to fit with the present ordering and conventions
def convert_spot_meas(spot_new_meas, dt):
    ''' Fix eamittance measurement to fit with the present ordering and conventions'''
    idx_ord_spot = np.argsort(spot_new_meas[:,0])
    spot_new_meas = spot_new_meas[idx_ord_spot,:]
    # Convert time to seconds as the rest of the data I have here
    spot_new_meas[:,0] *= 1e-9
    spot_new_meas[:,0] += dt
    spot_new_meas[:,1] = spot_new_meas[:,1]*1e-6
    return spot_new_meas
sigma_x_new_meas = convert_spot_meas(sigma_x_new_meas, dt)
sigma_y_new_meas = convert_spot_meas(sigma_y_new_meas, dt)

#I_apl = np.interp(times, t, I)

#%% Plot
#plt.close('all')

# Emittance
fig, ax = plt.subplots()
ax.plot(t*1e9, I, '-', color='k', label='Current')
ax.set_ylim(bottom=0.)
ax_emitt = ax.twinx()
ax_emitt.plot(times*1e9, emitt_Nx_new*1e6, 'o-', color='b', label='Emitt.')
ax_emitt.axhline(y=emitt_Nx*1e6, linestyle='--', color='b', label='Emitt. no plasma')
ax_emitt.set_ylabel('Emittance (mm mrad)')
ax_emitt.set_ylim(bottom=0., top=15.)
fig.legend()
ax.set_xlabel('Time (ns)')
ax.set_ylabel('Current (A)')
title = os.path.basename(sim) + "\nσ={:.3g}μm, σ'={:.3g}, ε={:.3g} mm mrad".format(1e6*sigma_x,
                                                                                     d_sigma_x,
                                                                                     emitt_Nx)
title += "Lc={:.3g}cm, Rc={:.3g}mm".format(1e2*l_cap,
                                                 1e3*r_cap)
fig.suptitle(title, color='r')
# ax.set_title(title)
#ax.legend()
plt.tight_layout()

# Spot
fig, ax = plt.subplots()
ax.plot(t*1e9, I, '-', color='k', label='Current')
ax.set_ylim(bottom=0.)
ax_spot = ax.twinx()
ax_spot.plot(times*1e9, sigma_x_new*1e6, 'o-', color='b', label='Spot rms')
# ax_spot.axhline(y=emitt_Nx*1e6, linestyle='--', color='b', label='Emitt. no plasma')
ax_spot.set_ylabel('Spot (mm mrad)')
# ax_spot.set_ylim(bottom=0., top=15.)
fig.legend()
ax.set_xlabel('Time (ns)')
ax.set_ylabel('Current (A)')
title = os.path.basename(sim) + "\nσ={:.3g}μm, σ'={:.3g}, ε={:.3g} mm mrad".format(1e6*sigma_x,
                                                                                     d_sigma_x,
                                                                                     emitt_Nx)
title += "Lc={:.3g}cm, Rc={:.3g}mm".format(1e2*l_cap,
                                           1e3*r_cap)
fig.suptitle(title, color='r')
# ax.set_title(title)
#ax.legend()
plt.tight_layout()

# Trace space
fig, ax = plt.subplots(nrows=2)
ax[0].scatter(x,xp)
ax[1].scatter(x_new,xp_new)


#%% Plot for thesis
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# Emittance
fig_I_th, ax_em_th = plt.subplots(figsize=(4.5,3.))

emitt_sim, = ax_em_th.plot(times*1e9, emitt_Nx_new*1e6, color='purple',
                          lw=2,
                          # label='$\epsilon_N$ simulated',
                          zorder=10)

emitt_x_meas = ax_em_th.errorbar(emitt_Nx_new_meas[:,0]*1e9, emitt_Nx_new_meas[:,1]*1e6, yerr=errorbars_Nx_new_meas,
                                  color='b', linestyle='--', marker='o',
                                  # label='$\epsilon_{N,y}$, measured',
                                  uplims=True,
                                  lolims=True,
                                  zorder=8)
emitt_y_meas = ax_em_th.errorbar(emitt_Ny_new_meas[:,0]*1e9, emitt_Ny_new_meas[:,1]*1e6, yerr=errorbars_Ny_new_meas,
                                  color='r', linestyle='--', marker='o',
                                  # label='$\epsilon_{N,y}$, measured',
                                  uplims=True, lolims=True, zorder=9)
emitt_base = ax_em_th.axhline(y=emitt_Nx*1e6, linestyle='--', lw=2,
                               color='purple',
                               # label='$\epsilon_N$ no plasma',
                               zorder=12)

ax_I_th = ax_em_th.twinx()
curr, = ax_I_th.plot(t*1e9, I, '-', lw=3, c='darkgray', zorder=0)
ax_I_th.set_ylim(bottom=0., top=100.)
ax_I_th.set_zorder(ax_em_th.get_zorder()-1)
ax_em_th.patch.set_visible(False)

ax_em_th.set_ylabel('Emittance (mm mrad)')
ax_em_th.set_ylim(bottom=0., top=14.)
ax_em_th.set_xlim([0.,1200])

# ax_em_th.legend(loc=1)
ax_em_th.legend([curr, emitt_x_meas, emitt_y_meas, emitt_base, emitt_sim],
                ['Current',
                 '$\epsilon_{N,x}$ measured',
                 '$\epsilon_{N,y}$ measured',
                 '$\epsilon_N$ no plasma',
                 '$\epsilon_N$ simulated'])

ax_em_th.set_xlabel('Time (ns)')
ax_I_th.set_ylabel('Current (A)')

plt.tight_layout()

# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# Spot
fig_I_th, ax_sp_th = plt.subplots(figsize=(4.5,3.))

spot_sim, = ax_sp_th.plot(times*1e9, sigma_x_new*1e6,
                          color='purple',
                          lw=2,
                          # label='$\epsilon_N$ simulated',
                          zorder=10)
spot_ideal, = ax_sp_th.plot(times*1e9, sigma_x_new_ideal*1e6,
                            color='purple',
                            linestyle='--')
spot_x_meas, = ax_sp_th.plot(sigma_x_new_meas[:,0]*1e9,
                            sigma_x_new_meas[:,1]*1e6,
                            color='b', linestyle='--', marker='o',
                            # label='$\epsilon_{N,y}$, measured',
                            zorder=8)
spot_y_meas, = ax_sp_th.plot(sigma_y_new_meas[:,0]*1e9,
                            sigma_y_new_meas[:,1]*1e6,
                            color='r', linestyle='--', marker='o',
                            # label='$\epsilon_{N,y}$, measured',
                            zorder=8)

ax_I_th_sp = ax_sp_th.twinx()
curr, = ax_I_th_sp.plot(t*1e9, I, '-', lw=3, c='darkgray', zorder=0)
ax_I_th_sp.set_ylim(bottom=0., top=100.)
ax_I_th_sp.set_zorder(ax_sp_th.get_zorder()-1)
ax_sp_th.patch.set_visible(False)

ax_sp_th.set_ylabel('Spot rms (μm)')
ax_sp_th.set_xlim([0.,1200])
ax_sp_th.set_ylim([0.,350])

# ax_sp_th.legend(loc=1)
ax_sp_th.legend([curr, spot_x_meas, spot_y_meas, spot_sim, spot_ideal],
                ['Current',
                 '$\sigma_{x}$ measured',
                 '$\sigma_{y}$ measured',
                 '$\sigma$ simulated',
                 '$\sigma$ unif. current'])

ax_sp_th.set_xlabel('Time (ns)')
ax_I_th_sp.set_ylabel('Current (A)')

plt.tight_layout()
