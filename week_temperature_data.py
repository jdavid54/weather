import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



csv_file = 'csv/week_temperature_data.csv'
def read_text():
    f = open(csv_file, "r")
    text = f.readlines()
    f.close()
    print(text)
    
read_text()

data = pd.read_csv(csv_file)
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.info()

x = data['timestamp']
y = data['temperature']
from scipy import interpolate

fig, ax = plt.subplots(subplot_kw={})
ax.plot(x,y,'o',markersize=2)
'''
x_new = np.linspace(0, len(x), len(x))
a_BSpline = interpolate.make_interp_spline(x_new, y)
y_new = a_BSpline(x_new)
plt.plot(x_new, y_new)
'''
ax.plot(x, y)
ax.set_xlabel('Time')
ax.set_ylabel('Temperature')
plt.title('Week temperature')
#plt.legend()
plt.show()


from scipy.interpolate import UnivariateSpline
fig, ax = plt.subplots()

# spline the curve
factor = len(x)
xs = np.linspace(0, len(x), len(x))

spl1 = UnivariateSpline(xs, y, s=1000)  # default s=len(x)
#spl2 = UnivariateSpline(x, z)
spl1.set_smoothing_factor(factor)  # same as UnivariateSpline(x, y, s=1000)
#spl2.set_smoothing_factor(factor)

ax.plot(xs,y,'o',markersize=2)
plt.plot(xs, spl1(xs), 'g', lw=2, label='Temp')
#plt.plot(xs, spl2(xs), 'r', lw=3, label ='Hum')
plt.legend()
plt.show()

from scipy.interpolate import interp1d
x2 = np.linspace(0, 10, num=11, endpoint=True)
ynew = np.cos(-x2**2/9.0)
f = interp1d(x2, ynew)
f2 = interp1d(x2, ynew, kind='cubic')
xnew = np.linspace(0, 10, num=100, endpoint=True)
plt.plot(x2, ynew, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
plt.legend(['data', 'linear', 'cubic'], loc='best')
plt.show()

f = interp1d(xs, y)
f2 = interp1d(xs, y, kind='cubic')
xnew = np.linspace(0, len(xs), len(xs)*5)
plt.plot(xs, y, 'o')
plt.plot(xs, f(xs), '-')
plt.plot(xnew, f2(xnew), '--')
plt.legend(['data', 'cubic2'], loc='best')
plt.show()

# spline
x = np.arange(0, 2*np.pi+np.pi/4, 2*np.pi/8)
y2 = np.sin(x)
tck = interpolate.splrep(x, y2, s=0)
xnew = np.arange(0, 2*np.pi, np.pi/50)
ynew = interpolate.splev(xnew, tck, der=0)

plt.figure()
plt.plot(x, y2, 'x', xnew, ynew, xnew, np.sin(xnew), x, y2, 'b')
plt.legend(['Linear', 'Cubic Spline', 'True'])
plt.axis([-0.05, 6.33, -1.05, 1.05])
plt.title('Cubic-spline interpolation')
plt.show()

tck = interpolate.splrep(xs, y, s=0)
xnew = np.linspace(0, len(xs), len(xs)*5)
ynew = interpolate.splev(xnew, tck, der=0)

plt.figure()
plt.plot(xs, y, 'x', xnew, ynew) #, xs, np.sin(xnew), x, y, 'b')
plt.legend(['Linear', 'Cubic Spline', 'True'])
plt.title('Cubic-spline interpolation')
plt.show()