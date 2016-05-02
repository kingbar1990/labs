from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from numpy import pi, linspace, cos, meshgrid, sqrt, arange, ma
import time
import matplotlib.animation as animation


def generate(x, y, phi):
    return cos(2 * pi * x + phi) * (1 - sqrt(y ** 2 + x**2))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x, y = meshgrid(linspace(-1, 1, 50), linspace(-1, 1, 50))
z = generate(x, y, 0.0)

wframe = None
start = time.time()
for phi in linspace(0, 180 / pi, 300):
    oldcol = wframe
    z = generate(x, y, phi)
    wframe = ax.plot_wireframe(x, y, z, rstride=2, cstride=2)

    if oldcol is not None:               # Remove old line collection before drawing
        ax.collections.remove(oldcol)
    plt.pause(.001)

print 'FPS: {}'.format(100 / (time.time() - start))

'''Other example'''
fig, ax = plt.subplots()
x = arange(0, 2 * pi, 0.01)
line, = ax.plot(x, cos(x))


def animate(i):
    line.set_ydata(cos(x + i/10.0))
    return line,


def init():                               # Init only required for blitting to give a clean slate.
    line.set_ydata(ma.array(x, mask=True))
    return line,

ani = animation.FuncAnimation(fig, animate, arange(1, 2000), init_func=init,
                              interval=25, blit=True)
plt.show()
