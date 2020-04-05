import matplotlib.pylab as plt 

import math

def linePlot(y, title):
    f = plt.figure()    
    ax = f.gca()
    ax.plot(y)
    plt.title(title)
    plt.ylabel(title)
    plt.show()
    plt.savefig(title)

def getOutputData(key, lines):

    ls = [l[:-1] for l in lines if key in l]
    # for l in ls:
    #     print(l)

    print(len(ls))
    data = [float(l.split(':')[1].strip()) for l in ls]
    return data

def plotSpin(fn):

    with open(fn, 'r') as f:
        ls = f.readlines()

    keys = [
        'angle',
        'turn_speed',
    ]

    data = {}
    for key in keys:
        print(key)
        data[key] = getOutputData(key, ls)
        print(data[key][:10])

    # index vs everything
    filename = fn.replace(".", "_")
    title = "index vs all (%s)" % filename
    f = plt.figure()    
    ax = f.gca()
    # create an index
    x = range(len(data['angle']))
    for key in keys:
        ax.plot(x, data[key], label=key)
    ax.legend()    
    plt.title(title)
    plt.xlabel("index")
    # plt.ylabel("speed (degs/sec)")
    # plt.show()
    plt.savefig(title)

    # angle vs speed plot
    filename = fn.replace(".", "_")
    title = "angle vs speed (%s)" % filename
    f = plt.figure()    
    ax = f.gca()
    ax.plot(data['angle'], data['turn_speed'])
    plt.title(title)
    plt.xlabel("angle (degrees)")
    plt.ylabel("speed (degs/sec)")
    # plt.show()
    plt.savefig(title)

def plotDriveOutput(fn):
    with open(fn, 'r') as f:
        ls = f.readlines()

    keys = [
        'wheel angle',
        'base speed',
        'left speed',
        'right speed',
        'correction',
        'gyro error'
    ]

    data = {}
    for key in keys:
        print(key)
        data[key] = getOutputData(key, ls)
        print(data[key][:10])
        
        # linePlot(data[key], key)


    # convert wheel angle to inches
    wheel_radius = 1. # inches
    inches = [angle*(math.pi/180.)*wheel_radius for angle in data['wheel angle']]
    data['inches'] = inches
    # linePlot(inches, 'inches')

    # combine plots: all must have same length!
    x = inches[1:]
    y1 = data['base speed']

    filename = fn.replace(".", "_")
    title = "dist vs base speed (%s)" % filename
    f = plt.figure()    
    ax = f.gca()
    ax.plot(x, y1)
    plt.title(title)
    plt.xlabel("dist (inches)")
    plt.ylabel("base speed (degs/sec)")
    # plt.show()
    plt.savefig(title)

    title = "dist vs speeds (%s)" % filename
    plotKeys = [
        'base speed',
        'left speed',
        'right speed',
        'gyro error',
        'correction',
    ]
    f = plt.figure()    
    ax = f.gca()
    for key in plotKeys:
        ax.plot(x, data[key], label=key)
    ax.legend()
    plt.title(title)
    plt.xlabel("dist (inches)")
    # plt.ylabel("speeds (degs/sec)")
    # plt.show()
    plt.savefig(title)

def main():
    import sys
    fn = sys.argv[1]
    # fn = "sim1.out"
    # plotDriveOutput(fn)
    plotSpin(fn)

if __name__ == '__main__':
    main()