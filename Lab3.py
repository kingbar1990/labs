import random as r
import numpy as np
import pylab
import matplotlib.ticker
from matplotlib import cm
from matplotlib.mlab import stineman_interp

print "Standard values are given in parentheses"
mu = float(raw_input('mu(0.002): ') or 0.002)
k = float(raw_input('k(4): ') or 4)
h = float(raw_input('layer thickness(1000): ') or 1000)
cos_teta = np.cos(np.radians(float(raw_input('teta angle(45): ') or 45)))
prob_abs = float(raw_input('absorption(0.05): ') or 0.05)
n = int(raw_input('number of particles(100000): ') or 100000)
x = float(raw_input('x0(0.25): ') or 0.25)
n_abs, n_ref, n_fly = 0, 0, 0
f = [0] * 90
abs_h = [0] * int(h)
for _ in xrange(n):
    x0 = x
    while True:
        if r.random() <= 1 - prob_abs:
            cos_omega = r.random() ** (1 / k)
            sin_omega = np.sqrt(1 - cos_omega ** 2)
            sin_teta = np.sqrt(1 - cos_teta ** 2)
            cos_teta_new = cos_teta * cos_omega - \
                           sin_teta * sin_omega * np.sin(2 * np.pi * r.random())
            x0_new = x0 + (-np.log(r.random()) / mu) * cos_teta_new
            if x0_new < 0:
                n_ref += 1
                break
            elif x0_new > h:
                n_fly += 1
                i = int(np.degrees(np.arccos(cos_teta_new)))
                f[i] += 1
                break
        else:
            n_abs += 1
            if 0 <= x0_new <= h:
                abs_h[int(x0_new)] += 1
            break

print "Absorbed: {p1}%, reflected: {p2}%, flown: {p3}%".format(p1=n_abs * 100. / n,
                                                               p2=n_ref * 100. / n,
                                                               p3=n_fly * 100. / n)


def plots():
    matplotlib.rcParams['backend'] = 'MacOSX'
    matplotlib.rcParams['figure.dpi'] = 80
    matplotlib.rcParams['figure.figsize'] = 12, 5
    figure = pylab.figure()

    """First graph"""
    axes = figure.add_subplot(1, 2, 1)
    # formatter = matplotlib.ticker.FuncFormatter(lambda x, pos: "{x}".format(x=int(x) - 90))
    # axes.xaxis.set_major_formatter(formatter) all this for x-axis values name
    dz = np.array(f)
    colors = cm.rainbow((dz - dz.min()) / np.float_(dz.max() - dz.min()))
    x1 = [t for t in xrange(90)]
    y1 = [f[i] for i in xrange(90)]
    pylab.bar(x1, y1, width=1, alpha=1, linewidth=0, color=colors)
    axes.set_xlabel('Degrees')
    axes.set_ylabel('Number of particles')
    axes.set_title('The particle`s angular spread')
    # yp1 = None
    # xi1 = np.linspace(x1[0], x1[-1], 15)
    # yi1 = stineman_interp(xi1, x1, y1, yp1)
    # axes.plot(xi1, yi1, '-k', alpha=0.5)

    """Second graph"""
    x2 = [t for t in xrange(int(h))]
    y2 = [abs_h[i] for i in xrange(int(h))]
    axes = figure.add_subplot(1, 2, 2)
    axes.plot(x2, y2, 'ro', alpha=0.1)
    axes.set_xlabel('Thickness (in arbitrary units)')
    axes.set_title("Position of absorption")
    # yp2 = None
    # xi2 = np.linspace(x2[0], x2[-1], 15)
    # yi2 = mlab.less_simple_linear_interpolation(x2, y2, xi2, extrap=True)
    # axes.plot(xi2, yi2, '-k', alpha=1)
    # axes.semilogx(h)
    axes.grid()
    pylab.show()

plots()
