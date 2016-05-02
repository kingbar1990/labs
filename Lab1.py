import random
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

j_sleep, j_up, j_down, j_right, j_left = 0, 0, 0, 0, 0
u, d, r, l = [0]*21, [0]*21, [0]*21, [0]*21
p = [[0] * 21 for i in xrange(21)]
print "If you don't know a some value, skip it."
n = int(raw_input('100 or n: ') or 100)
m = int(raw_input('100 or m: ') or 100)
n0_glob = int(raw_input('50 or n0: ') or 50)
m0_glob = int(raw_input('50 or m0: ') or 50)
number = int(raw_input('10000 or number: ') or 10000)
print 'Enter probabilities: '
sleep = float(raw_input('0.0001 or sleep: ') or 0.0001)
up = float(raw_input('0.25 or up: ') or 0.25)
down = float(raw_input('0.25 or down: ') or 0.25)
right = float(raw_input('0.25 or right: ') or 0.25)
left = float(raw_input('0.25 or left: ') or 0.25)

for _ in xrange(number):
    n0 = n0_glob
    m0 = m0_glob
    while True:
        rand_sleep = random.random()
        if rand_sleep < (1 - sleep):
            rand = random.random()
            if rand <= up:
                n0 += 1
                if n0 > n:
                    j_up += 1
                    u[int(m0 * 20 / m)] += 1
                    break
            elif rand <= up + down:
                n0 -= 1
                if n0 < 0:
                    j_down += 1
                    d[int(m0 * 20 / m)] += 1
                    break
            elif rand <= up + down + right:
                m0 += 1
                if m0 > m:
                    j_right += 1
                    r[int(n0 * 20 / n)] += 1
                    break
            elif rand <= 1:
                m0 -= 1
                if m0 < 0:
                    j_left += 1
                    l[int(n0 * 20 / n)] += 1
                    break
        else:
            j = int(m0 * 20 / m)
            k = int(n0 * 20 / n)
            p[j][k] += 1
            j_sleep += 1
            break

for i in [j_sleep, j_up, j_down, j_right, j_left]:
    print float(i)/number*100,
print '\n' + "Total number of particles: " + str(j_sleep + j_up + j_down + j_right + j_left)


def graph():
    """The particles that left us"""
    plt.figure(1)
    for q in [u, d, r, l]:
        plt.plot([t for t in xrange(20)], [q[t] for t in xrange(20)], '-', linewidth=1.0)
        plt.bar([t for t in xrange(20)], [q[t] for t in xrange(20)], alpha=0.4)
    '''The particles that have fallen asleep'''
    plt.figure(2)

    data = np.array([p[j][k] for j in xrange(20) for k in xrange(20)])
    data.shape = (20, 20)

    ax = Axes3D(plt.figure(2))

    lx = len(data[0])            # Work out matrix dimensions
    ly = len(data[:, 0])
    xpos = np.arange(0, lx)    # Set up a mesh of positions
    ypos = np.arange(0, ly)
    xpos, ypos = np.meshgrid(xpos+0.25, ypos+0.25)

    xpos = xpos.flatten()   # Convert positions to 1D array
    ypos = ypos.flatten()
    zpos = np.zeros(lx*ly)

    dx = 1 * np.ones_like(zpos)
    dy = 1 * np.ones_like(zpos)
    dz = data.flatten()

    colors = cm.rainbow((dz-dz.min())/np.float_(dz.max()-dz.min()))

    ax.bar3d(xpos.ravel(), ypos.ravel(), zpos, dx, dy, dz, color=colors, alpha=0.6)
    ax.set_zlabel('Number of particles')
    plt.show()
graph()
