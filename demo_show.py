import gdal
import shapefile
import time
import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MaxNLocator


PLOT_SCALE = 56.0
gdal.AllRegister()
def readShapeData(path, fileName):
    myFile = path + fileName
    sf = shapefile.Reader(myFile)
    print("Read Geographic Data:")
    print("Data File -->{}{}".format(path, myFile))
    print("Type of shape= {}".format(sf.shapeTypeName))
    print("Number of shape = {}".format(len(sf)))
    print("Number of field = {}".format(len(sf.fields)))
    print("Box:{}".format([coor for coor in sf.bbox]))
    return sf

def plotProvinceMap(figF, Title, myPath, province, w, h):
    myFile = 'City\\'+province+'-city\\'+province
    sf = readShapeData(myPath, myFile)

    width = w / PLOT_SCALE
    height = h/PLOT_SCALE
    x1 = math.floor(sf.bbox[0])
    x2 = math.floor(sf.bbox[2])+1
    y1 = math.floor(sf.bbox[1])
    y2 = math.floor(sf.bbox[3])+1
    height = width*(y2-y1)/(x2-x1)
    fig = plt.figure(figsize=(width, height), edgecolor='red')
    plt.axis([x1,x2,y1,y2])
    plt.xlabel("LONGITUDE", fontsize=16)
    plt.ylabel("LATITUDE", fontsize=16)
    plt.title(Title, fontsize=20)
    shapes = sf.shapes()
    kdisplay = max(1, len(sf)//10)
    for i in range(len(sf)):
        npoint = len(shapes[i].points)
        npart = len(shapes[i].parts)
        if( (i % kdisplay ) == 0):
            print("   shape{}:{}points  {}parts".format(i+1, npoint, npart))
        for j in range(npart):
            if(j==npart-1):
                mpoint = npoint - shapes[i].parts[j]
            else:
                mpoint = shapes[i].parts[j+1]-shapes[i].parts[j]
            xx = np.zeros((mpoint, 1), dtype=np.float32)
            yy = np.zeros((mpoint, 1), dtype=np.float32)
            for k in range(mpoint):
                xx[k] = shapes[i].points[shapes[i].parts[j]+k][0]
                yy[k] = shapes[i].points[shapes[i].parts[j]+k][1]
            if(sf.shapeTypeName=="POLYLINE"):
                plt.plot(xx,yy,'-',color='grey')
            elif(sf.shapeTypeName=="POLYGON"):
                plt.fill(xx,yy,facecolor='blue', edgecolor='black')
    myfile = "Province\\"+province+"\\"+province
    sf2 = readShapeData(myPath,myfile)
    plotMapElement(sf2, 'blue', 2, 0)
    plt.grid(True, linestyle=':')
    plt.show()
    fig.savefig(figF, bbox_inches='tight')
    return 0
def plotMapElement(sf, Color, size, flag):
    shapes = sf.shapes()
    if(sf.shapeTypeName == "Point"):
        npoint = len(sf)
        xx = np.zeros((npoint,1),dtype=np.float32)
        yy = np.zeros((npoint, 1), dtype=np.float32)
        for i in range(npoint):
            xx[i] = shapes[i].points[0][0]
            yy[i] = shapes[i].points[0][1]
        plt.scatter(xx, yy, s=size, color=Color)
    else:
        for i in range(len(sf)):
            npoint = len(shapes[i].points)
            npart = len(shapes[i].parts)
            for j in range(npart):
                if(j==npart-1):
                    mpoint = npoint - shapes[i].parts[j]
                else:
                    mpoint = shapes[i].parts[j+1] - shapes[i].parts[j]

                xx = np.zeros((mpoint, 1), dtype=np.float32)
                yy = np.zeros((mpoint, 1), dtype=np.float32)
                for k in range(mpoint):
                    xx[k] = shapes[i].points[shapes[i].parts[j] + k][0]
                    yy[k] = shapes[i].points[shapes[i].parts[j] + k][1]
                if (sf.shapeTypeName == "POLYLINE"):
                    if(flag<1):
                        plt.plot(xx, yy, linewidth=size, color=Color)
                    else:
                        plt.plot(xx, yy, '-', linewidth=size, color=Color)
                elif (sf.shapeTypeName == "POLYGON"):
                    if (flag < 1):
                        plt.plot(xx, yy, color=Color)
                    elif(flag == 1):
                        plt.fill(xx, yy, facecolor=Color, edgecolor='black')
                    elif(flag>1):
                        plt.fill(xx, yy, facecolor="blue", edgecolor='black')
    return 0





if __name__ == "__main__":
    print("Plot Digital Elevation Model Picture ")
    width = 1600
    height = 800
    start = time.time()
    shapepath = 'D:\\demodata\\china1m\\'
    dempath = 'D:\\demodata\\cn_dem30\\'
    plotProvinceMap("Province.png", "Henan", shapepath, "Henan", width, height)
    pass