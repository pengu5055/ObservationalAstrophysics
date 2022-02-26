import numpy as np


def eq2azalt(alpha, delta, t, SUT0, lamb, phi, t_0=15):
    H = np.deg2rad(((SUT0 + lamb + (t - t_0)*(366.2422/365.2422)) - alpha) % 360)
    # LST = 225.117748  # DEBUG: Manually enter Local Star time
    # LST = 44.621590
    # H = (LST - ra) % 360
    # print("Hour angle: {}".format(np.rad2deg(H)))

    delta = np.deg2rad(delta)
    phi = np.deg2rad(phi)
    h = np.arcsin(np.sin(phi) * np.sin(delta) + np.cos(phi) * np.cos(delta) * np.cos(H))
    A = np.arccos((np.sin(delta) - np.sin(h) * np.sin(phi)) / (np.cos(h) * np.cos(phi)))

    # Unknown correction
    if np.rad2deg(H) < 180:
        return 360 - np.rad2deg(A), np.rad2deg(h)

    return np.rad2deg(A), np.rad2deg(h)


def deg2dms(time):
    tH = int(np.trunc(time))
    tM = int(np.trunc((time - tH) * 60))
    tS = (((time - tH) * 60) - tM) * 60

    return "{:0>2d}:{:0>2d}:{:05.2f}".format(int(tH), int(tM), (tS))

