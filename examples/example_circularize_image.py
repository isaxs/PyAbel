import numpy as np
import matplotlib.pyplot as plt
import abel
import scipy.interpolate

#######################################################################
#
# example_circularize_image.py
#
# O- sample image -> forward Abel + distortion = measured VMI
#  measured VMI   -> inverse Abel transform -> speed distribution
# Compare disorted and circularized speed profiles
#
#######################################################################


# sample image -----------
IM = abel.tools.analytical.sample_image(n=511, name='Ominus', sigma=2)

# forward transform == what is measured
IMf = abel.Transform(IM, method='hansenlaw', direction="forward").transform

# flower image distortion
IMdist = abel.tools.analytical.flower_distort(IMf, amp=0.1, phase=2)

# circularize ------------
IMcirc, sla, sc, scspl = abel.tools.circularize.circularize_image(IMdist,
               method='lsq', nslices=32, zoom=2, smooth=0,
               return_correction=True)

# inverse Abel transform for distored and circularized images ---------
AIMdist = abel.Transform(IMdist, method="three_point",
                         transform_options=dict(basis_dir='bases')).transform
AIMcirc = abel.Transform(IMcirc, method="three_point",
                         transform_options=dict(basis_dir='bases')).transform

# respective speed distributions
rdist, speeddist = abel.tools.vmi.angular_integration(AIMdist, dr=0.5)
rcirc, speedcirc = abel.tools.vmi.angular_integration(AIMcirc, dr=0.5)

# note the small image size is responsible for the slight over correction 
# of the background near peaks

row, col = IMcirc.shape

# plot --------------------

fig, axs = plt.subplots(2, 2, figsize=(8, 8))
fig.subplots_adjust(wspace=0.5, hspace=0.5)

extent = (np.min(-col//2), np.max(col//2), np.min(-row//2), np.max(row//2))
axs[0, 0].imshow(IMdist, aspect='auto', origin='lower', extent=extent)
axs[0, 0].set_title("Ominus distorted sample image")

axs[0, 1].imshow(AIMcirc, vmin=0, aspect='auto', origin='lower',
                 extent=extent)
axs[0, 1].set_title("circ. + inv. Abel")

axs[1, 0].plot(sla, sc, 'o')
ang = np.arange(-np.pi, np.pi, 0.1)
axs[1, 0].plot(ang, scspl(ang))
axs[1, 0].set_xticks([-np.pi, 0, np.pi])
axs[1, 0].set_xticklabels([r"$-\pi$", "0", r"$\pi$"])
axs[1, 0].set_xlabel("angle (radians)")
axs[1, 0].set_ylabel("radial correction factor")
axs[1, 0].set_title("radial correction")

axs[1, 1].plot(rdist, speeddist, label='dist.')
axs[1, 1].plot(rcirc, speedcirc, label='circ.')
axs[1, 1].axis(xmin=100, xmax=240)
axs[1, 1].set_title("speed distribution")
axs[1, 1].legend(frameon=False)
axs[1, 1].set_xlabel('radius (pixels)')
axs[1, 1].set_ylabel('intensity')

plt.savefig("output/example_circularize_image.png", dpi=75)
plt.show()
