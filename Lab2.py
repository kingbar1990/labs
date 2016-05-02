from math import exp, cos, sin, pi
import random
import time
import sys
n = int(raw_input('Enter n(10000): ') or 10000)
mu = float(raw_input('Enter mu(5): ') or 5)
k = float(raw_input('Enter k(5): ') or 5)
m = 50
maximum = 0


def fx(x):
    return (1 - x) * x


def fy(y, mu):
    return exp(-mu * y)


def fz(z, k):
    return 1 + cos(2 * pi * k * z)


def func(x, y, z, mu, k):
    return fx(x) * fy(y, mu) * fz(z, k)


def analytical():
    """Analytical method"""
    i_x = 1 / 6.0
    i_y = (-1 / float(mu)) * (exp(-mu) - 1)
    i_z = (1 + 1/(2*pi*k) * sin(2*pi*k))
    print '\n' + "Analytical value: {}".format(i_x * i_y * i_z)


def rectangle():
    """Rectangle method"""
    start = time.time()
    h = 1/float(n)
    x, y, z, i_x, i_y, i_z = h/2, h/2, h/2, 0, 0, 0
    for _ in xrange(n):
        i_x += fx(x)
        x += h
        i_y += fy(y, mu)
        y += h
        i_z += fz(z, k)
        z += h
    delta_time = time.time() - start
    print '\n' + "Rectangle value: {}".format((i_x * h) * (i_y * h) * (i_z * h)) +\
          '\n' + "time processing: {}".format(delta_time)


def simple():
    """Simple calculation of integral"""
    start = time.time()
    arr = [0]*m
    mi, d, s = 0, 0, 0
    for i in xrange(m):
        for _ in xrange(n):
            s += func(random.random(), random.random(), random.random(), mu, k)
        arr[i] = s/n
        mi += arr[i]
        s = 0

    for j in xrange(m):
        d += (arr[j] - mi/m)**2

    delta_time = time.time() - start

    print '\n' + "Simple method: {}".format(mi / m) + \
          '\n' + "time processing: {}".format(delta_time) + \
          '\n' + "dispersion: {}".format(d / m) + \
          '\n' + "laboriousness: {}".format(d / m * delta_time)


def find_min_max():
    """Finding function maximum"""
    def f(x, y, z):
        return (1 - x) * x * exp(-mu * y) * (1 + cos(2 * pi * k * z))

    max_func = - sys.maxint - 1
    min_func = sys.maxint
    maximal_x, maximal_y, maximal_z = None, None, None
    minimal_x, minimal_y, minimal_z = None, None, None

    for i in xrange(1000000):
        randx, randy, randz = random.random(), random.random(), random.random()
        result = f(randx, randy, randz)

        max_func = max(max_func, result)
        if max_func == result:
            maximal_x, maximal_y, maximal_z = randx, randy, randz

        min_func = min(min_func, result)
        if min_func == result:
            minimal_x, minimal_y, minimal_z = randx, randy, randz
    global maximum
    maximum = max_func
    print '\n' + "Maximal (x, y):", (maximal_x, maximal_y, maximal_z)
    print "Max func value:", max_func, '\n'
    print "Minimal (x, y):", (minimal_x, minimal_y, minimal_z)
    print "Min func value:", min_func


def neyman():
    """Neyman calculation of integral"""
    start = time.time()
    arr = [0]*m
    mi, d, s = 0, 0, 0
    for i in xrange(m):
        for _ in xrange(n):
            if func(random.random(), random.random(), random.random(), mu, k) > random.random()*maximum:
                s += 1
        arr[i] = (s/float(n))*maximum*1
        mi += arr[i]
        s = 0
    for j in xrange(m):
        d += (arr[j] - mi/m)**2

    delta_time = time.time() - start
    print '\n' + "Neyman method: {}".format(mi / m) + \
          '\n' + "time processing: {}".format(delta_time) + \
          '\n' + "dispersion: {}".format(d / m) + \
          '\n' + "laboriousness: {}".format(d / m * delta_time)

analytical(), rectangle(), simple(), find_min_max(), neyman()
