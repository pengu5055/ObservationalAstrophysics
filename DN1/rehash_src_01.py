import numpy as np


def eq2azalt(alpha, delta, t, SUT0, lamb, phi, t_0=15):
    """
    Convert equatorial coordinates to alt az
    :param alpha: Right ascension in deg
    :param delta: Declination in deg
    :param SUT0: Greenwich mean sidereal time at 0h UT in deg
    :param t: Time of observation in deg
    :param lamb: Observer longitude in deg
    :param phi: Observer latitude in deg

    :return A: Azimuth
    :return h: Elevation
    """
    H = np.deg2rad(((SUT0 + lamb + (t - t_0)*(366.2422/365.2422)) - alpha) % 360)
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


def startrack(alpha, delta, t_start, t_end, bins, SUT0, lamb, phi):
    """
    Track elevation and azimuth of desired star at discrete time points
    :param alpha: Right ascension of star
    :param delta: Declination of star
    :param t_start: Time of observation start in HMS
    :param t_end: Time of observation end in HMS
    :param bins: Discrete divisions of time interval (2 less than given because broken bins system in generator)
    :param SUT0: Greenwich sidereal time at 0h UT
    :param lamb: Observer longitude
    :param phi: Observer latitude

    :return: 2D array with Azimuth and elevation and 1D array of times
    """
    step = np.abs(t_start + t_end)/bins
    if t_start > t_end:
        times = np.arange(t_start, t_end + 360, step)
    elif t_start < t_end:
        times = np.arange(t_start, t_end, step)
    else:
        raise ValueError("Something's fucky..")

    output = []
    for time in times:
        output.append(eq2azalt(alpha, delta, time, SUT0, lamb, phi))

    return np.column_stack(np.array(output)), times
