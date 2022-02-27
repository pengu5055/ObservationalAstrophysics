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
        az, alt = eq2azalt(alpha, delta, time, SUT0, lamb, phi)
        output.append([az, alt])

    return np.column_stack(np.array(output)), times


def sun_analemma(GMST, TOD, Obs_lambda, Obs_phi, index_delay=0):
    """
    Get Az, Alt of sun at certain time in the day for a whole year

    :param GMST: Array of SUT0 numbers for days in degrees
    :param TOD: Time of day in degrees
    :param Obs_lambda: Observer longitude in degrees
    :param Obs_phi: Observer latitude in degrees
    :param index_delay: Delay of GMST vector for days since vernal equinox
    :return: Array with azimuth, altitude and day since vernal equinox
    """
    DSE = np.arange(0, len(GMST)) + index_delay  # Days since spring equinox
    epsilon = np.deg2rad(23.44)
    lamb = 2*np.pi*DSE/365.2422  # Already in radians
    alpha = np.arctan(np.tan(lamb)*np.cos(epsilon))
    delta = np.arcsin(np.sin(lamb)*np.sin(epsilon))
    output = []

    # Continuity corrections
    alpha[(171 - 79):] += np.pi
    alpha[(353 - 79):] += np.pi

    # Convert to deg for eq2azalt
    alpha = np.rad2deg(alpha)
    delta = np.rad2deg(delta)

    for day in range(len(GMST)):
        az, alt = eq2azalt(alpha[day], delta[day], TOD, GMST[day], Obs_lambda, Obs_phi)
        output.append([az, alt, DSE[day]])

    return np.column_stack(np.array(output))


def sun_proper_analemma(GMST, TOD, Obs_lambda, Obs_phi, JD_start, index_delay=0):
    """
    Analemma but taking into account, that Earth's orbit is not circular but elliptical
    Get Az, Alt of sun at certain time in the day for a whole year

    :param GMST: Array of SUT0 numbers for days in degrees
    :param TOD: Time of day in degrees
    :param Obs_lambda: Observer longitude in degrees
    :param Obs_phi: Observer latitude in degrees
    :param JD_start: Julian date of first day in GMST
    :param index_delay: Delay of GMST vector for days since vernal equinox
    :return: Array with azimuth, altitude and day since vernal equinox
    """
    # Podane konstante
    epsilon = np.deg2rad(23.44)
    Pi = 102.9373
    M_0 = 357.5291
    M_1 = 0.98560028
    J_2000 = 2451545
    C_1 = 1.9148
    C_2 = 0.0200
    C_3 = 0.0003
    C_4 = 0
    C_5 = 0
    C_6 = 0

    DSE = np.arange(0, len(GMST)) + index_delay  # Days since spring equinox
    J = np.arange(JD_start, JD_start + 366)
    M = (M_0 + M_1*(J - J_2000)) % 360
    C = get_C(M, C_1, C_2, C_3, C_4, C_5, C_6)

    lamb = np.deg2rad(M + Pi + C + 180)  # Lambda in degrees
    print(lamb)
    print(2*np.pi*DSE/365.2422)
    alpha = np.arctan(np.tan(lamb) * np.cos(epsilon))
    delta = np.arcsin(np.sin(lamb) * np.sin(epsilon))
    output = []

    # Continuity corrections
    alpha[(171 - 77):] += np.pi
    alpha[(353 - 76):] += np.pi

    # Convert to deg for eq2azalt
    alpha = np.rad2deg(alpha)
    delta = np.rad2deg(delta)

    for day in range(len(GMST)):
        az, alt = eq2azalt(alpha[day], delta[day], TOD, GMST[day], Obs_lambda, Obs_phi)
        output.append([az, alt, DSE[day]])

    return np.column_stack(np.array(output))


def get_C(M, C_1, C_2, C_3, C_4, C_5, C_6):
    M = np.deg2rad(M)
    return (C_1*np.sin(M) + C_2*np.sin(2*M) + C_3*np.sin(3*M) +
            C_4*np.sin(4*M) + C_5*np.sin(5*M) + C_6*np.sin(6*M))

