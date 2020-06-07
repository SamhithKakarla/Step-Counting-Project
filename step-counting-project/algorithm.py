lines = []
path = "/Users/samhith/step-data/"
name = "11-400-step-regular.csv"
with open(path + name) as reader:
    lines = reader.readlines()

acc_x = [ float(line.split(",")[0]) for line in lines[1:] ]
acc_y = [ float(line.split(",")[1]) for line in lines[1:] ]
acc_z = [ float(line.split(",")[2]) for line in lines[1:] ]

gyro_x = [ float(line.split(",")[3]) for line in lines[1:] ]
gyro_y = [ float(line.split(",")[4]) for line in lines[1:] ]
gyro_z = [ float(line.split(",")[5]) for line in lines[1:] ]

def net_accel(x, y, z):
    return (x**2 + y**2 + z**2)**0.5

mag_acc = [ (net_accel(acc_x[i], acc_y[i], acc_z[i])) for i in range(2, len(acc_x) - 2) ]

mag_acc[2] = (mag_acc[0] + mag_acc[1] + mag_acc[2] + mag_acc[3] + mag_acc[4])/5
for i in range(3,len(mag_acc)-2):
   mag_acc[i] = (mag_acc[i-2] + mag_acc[i-1] + mag_acc[i] + mag_acc[i+1] + mag_acc[i+2])/5

import matplotlib.pyplot as plt
%matplotlib notebook

plt.plot(mag_acc, 'k-')
plt.show()

def get_peaks(data, THRESHOLD = 2):
    mean = sum(data)/len(data)
    std_dev = (sum( [ (val-mean)**2 for val in data ] )/(len(data)-1))**0.5
        
    peaks_x = []
    for i in range(1, len(data)-1):
        if (data[i] > data[i-1] and data[i] > data[i+1]):
            if (data[i] > mean + THRESHOLD*std_dev):
                peaks_x.append(i)
    
    realpeaks_x = []
    for i in range( len(peaks_x)-1):
        if(abs(peaks_x[i] - peaks_x[i + 1]) > 7):
            realpeaks_x.append(peaks_x[i])
            
            
    peaks_y = [ data[index] for index in realpeaks_x ]
    return realpeaks_x, peaks_y

peaks_x, peaks_y = get_peaks(mag_acc, 1.6)

plt.plot(peaks_x, peaks_y, 'ro')
plt.show()

print("Total steps:", len(peaks_x)*2 )
