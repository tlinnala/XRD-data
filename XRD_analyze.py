import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks_cwt
from scipy.signal import savgol_filter

window=15
data_points=1524 # Number of measurement points
# List of files to be processed
filenames=["000s","008s","013s","025s","120s","180s","300s"]

# Function to normalize data in 1D array
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

x_all=[]
y_all=[]

# Process files one by one
for i in range(len(filenames)):
    filename="./Br-Cl_phases/XRD/"+filenames[i]+".dat"
    df=pd.read_csv(filename,sep="\s+",header=None)
    # Convert data from strings to numbers
    df=df.apply(pd.to_numeric,errors="coerce")
    # Read x data from pandas dataframe
    x=df.loc[:,0]
    x=x.values
    x_all.append(x)
    # Read y data and proces/normalize
    y=df.loc[:,1]
    y=y.values
    y_proc=data_processing(y,0,data_points,window)
    y_proc=normdata(y_proc)
    y=normdata(y)
    y_all.append(y_proc)
    # Plot the figure and save
    plt.figure()
    plt.plot(x,y,label="Unprocessed data")
    plt.plot(x,y_proc,label="Processed data")
    plt.xlabel("2theta angle (degrees)")
    plt.ylabel("Intensity")
    plt.title("XRD spectrum")
    plt.legend()
    savename="./XRD_plots/XRD_spectrum_"+str(filenames[i])+".png"
    plt.savefig(savename)

# Plot all processed spectra in the same image
plt.figure()
for i in range(len(filenames)):
    plt.plot(x_all[i],y_all[i])
plt.xlabel("2theta angle (degrees)")
plt.ylabel("Intensity")
plt.title("All processed XRD spectra")
plt.savefig("./XRD_plots/all_spectra.png")