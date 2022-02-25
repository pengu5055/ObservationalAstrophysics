import numpy as np


def eq2azalt(ra, dec, t, SUT0, lamb, phi, t_0=15):
    H = np.deg2rad((SUT0 + lamb + (t - t_0)*(366.2422/365.2422)) - ra)
    # LST = 225.117748  # DEBUG: Manually enter Local Star time
    # LST = 44.621590
    # H = (LST - ra) % 360
    # print("Hour angle: {}".format(np.rad2deg(H)))
    dec = np.deg2rad(dec)
    phi = np.deg2rad(phi)
    h = np.arcsin(np.sin(phi)*np.sin(dec) + np.cos(phi)*np.cos(dec)*np.cos(H))
    A = np.arccos((np.sin(dec) - np.sin(h)*np.sin(phi))/(np.cos(h)*np.cos(phi)))

    return np.rad2deg(A), np.rad2deg(h)


def deg2dms(time):
    tH = int(np.trunc(time))
    tM = int(np.trunc((time - tH) * 60))
    tS = (((time - tH) * 60) - tM) * 60

    return "{:0>2d}:{:0>2d}:{:05.2f}".format(int(tH), int(tM), (tS))

