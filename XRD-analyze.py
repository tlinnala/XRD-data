import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks_cwt
from scipy.signal import savgol_filter

window=15
exp_min=0
exp_max=1524    # Number of measurement points
process_data=True
filenames=["000s.dat","008s.dat","013s.dat","025s.dat","120s.dat","180s.dat","300s.dat"]

# Function to normalize data in an array
def normdata(data):
    len1 = np.shape(data)[0]
    ndata = np.zeros(len1)
    ndata[:]=(data[:]-min(data[:]))/(max(data[:])-min(data[:]))
    return ndata

# Function to process measurement data
def data_processing (data,minn,maxn,window):
    nexp1=np.zeros(maxn-minn)
    # savgol_filter to smooth the data
    new1 = savgol_filter(data[minn:maxn], 31, 3)
    # Peak finding
    zf=find_peaks_cwt(new1, np.arange(10,15), noise_perc=0.01)
    # Background substraction
    for j in range(len(zf)-1):
        zf_start=np.maximum(0,zf[j+1]-window//2)
        zf_end=np.minimum(zf[j+1]+window//2,maxn)
        peak=new1[zf_start:zf_end]
        #abritaryly remove 1/4 data
        npeak=np.maximum(0,peak-max(np.partition(peak,window//5 )[0:window//5]))
        nexp1[zf_start:zf_end]= npeak
    return nexp1

# Process files one by one
for i in range(len(filenames)):
    filename="/home/tlinnala/work/XRD-data/Br-Cl_phases/XRD/"+filenames[i]
#    filename="./Br-Cl_phases/XRD/"+filenames[i]
    df=pd.read_csv(filename,sep="\s+",header=None)
    df=df.apply(pd.to_numeric,errors="coerce")
    # Read data from pandas dataframe
    x=df.loc[:,0]
    x=x.values
    y=df.loc[:,1]
    y=y.values
    # Process and normalize measurement data
    if process_data:
        y=data_processing(y,exp_min,exp_max,window)
        y=normdata(y)
    else:
        y=normdata(y)
    # Plot the figure and save
    plt.figure()
    plt.plot(x,y)
    plt.xlabel("2theta angle (degrees)")
    plt.ylabel("Intensity")
    plt.title("XRD-spectrum")
    savename="/home/tlinnala/work/XRD-data/XRD-spectrum_"+str(filenames[i])+".png"
    plt.savefig(savename)
