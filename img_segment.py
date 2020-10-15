import utils
import numpy as np
import json
import time

def kmeans(img,k):
    """
    Implement kmeans clustering on the given image.
    Steps:
    (1) Random initialize the centers.
    (2) Calculate distances and update centers, stop when centers do not change.
    (3) Iterate all initializations and return the best result.
    Arg: Input image;
         Number of K. 
    Return: Clustering center values;
            Clustering labels of all pixels;
            Minimum summation of distance between each pixel and its center.  
    """

    lab=np.zeros((len(img),len(img[0])))
    r,c=img.shape
    p_val=list(set(img.flatten()))
    pts=list(cmbs(2,p_val))
    his,bedg=np.histogram(img,256,[0, 256])
    c2_fin=[] 
    c1_fin=[]
    centers=[] 
    s_d=float('inf')
    for pt in pts:
        d1=float('-inf')
        d2=float('-inf')
        avg_c1=0 
        avg_c2=0 
        centers1=[]
        s_d1=0
        i=0
        while(d2!= 0 and d1!= 0):
            if(i!=0):
                C1=avg_c1
                C2=avg_c2
            else:
                C1=pt[0] 
                C2=pt[1]
            sum2=0
            sum1=0
            C2_lst=[] 
            C1_lst=[] 
            for indi,val in enumerate(his):
                if(abs(indi-C2)>abs(indi-C1)):
                    C1_lst.append(val)
                    sum1+=(indi*val)
                else:
                    C2_lst.append(val)
                    sum2+=(indi*val)
            if(sum(C1_lst)!=0):
                avg_c1=(int(sum1)/sum(C1_lst))
            if(sum(C2_lst)!=0):
                avg_c2=(int(sum2)/sum(C2_lst))       
            d1=C1-avg_c1
            d2=C2-avg_c2
            i+=1
        centers1.append(avg_c1)
        centers1.append(avg_c2)
        for indi,val in enumerate(his):
            if(abs(indi-centers1[1])>abs(indi-centers1[0])):
                s_d1+=(val*abs(indi-centers1[0]))
            else:
                s_d1+=(val*abs(indi-centers1[1]))
        if(s_d>s_d1):
            s_d=s_d1
            centers=centers1
    for indi,val in enumerate(his):
        if(abs(indi-centers[1])>abs(indi-centers[0])):
            c1_fin.append(indi)
        else:
            c2_fin.append(indi)
    for m in range(r):
        for n in range(c):
            if (img[m][n] in c1_fin):
                lab[m][n]=0
            else:
                lab[m][n]=1
    return centers,lab,s_d

def visualize(centers,labels):
    """
    Convert the image to segmentation map replacing each pixel value with its center.
    Arg: Clustering center values;
         Clustering labels of all pixels. 
    Return: Segmentation map.
    """
    # TODO: implement this function.
    r,c=labels.shape
    res=np.zeros((r,c))
    for m in range(r):
        for n in range(c):
            if(labels[m][n]==0):
                res[m][n]=centers[0]
            else:
                res[m][n]=centers[1]
    res=res.astype(np.uint8)
    return res

#To be able to generate combinations
def cmbs(b,ite):
    pl=tuple(ite)
    n=len(pl)
    if(n<b):
        return
    index=list(range(b))
    yield tuple(pl[i] for i in index)
    while True:
        for i in reversed(range(b)):
            if(index[i]!=i+n-b):
                break
        else:
            return
        index[i]+=1
        for j in range(i+1,b):
            index[j]=index[j-1]+1
        yield tuple(pl[i] for i in index)
     
if __name__ == "__main__":
    img = utils.read_image('lenna.png')
    k = 2
    start_time = time.time()
    centers, labels, sumdistance = kmeans(img,k)
    result = visualize(centers, labels)
    end_time = time.time()

    running_time = end_time - start_time
    print(running_time)

    centers = list(centers)
    with open('results/task1.json', "w") as jsonFile:
        jsonFile.write(json.dumps({"centers":centers, "distance":sumdistance, "time":running_time}))
    utils.write_image(result, 'results/task1_result.jpg')
