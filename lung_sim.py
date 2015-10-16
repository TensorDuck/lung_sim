import numpy as np
import random


def run_sim(Nsim, lung, diff_prob, lung_size, start_x, start_y):
    time_list = []
    for i in range(Nsim):
        time = 0
        mucusx = start_x
        mucusy = start_y
        go = True
        while go:
            rand = random.random()
            cell_type = lung[mucusx, mucusy]
            #assign direction of step
            if rand < diff_prob[cell_type,0]: #move forward
                mucusy += 1
            elif rand < diff_prob[cell_type,1]: #move backward
                mucusy -= 1
            elif rand < diff_prob[cell_type,2]: #move up
                mucusx += 1
            elif rand < diff_prob[cell_type,3]: #move down
                mucusx -= 1
            else:
                pass #do nothing
            #check legality of step:
            if mucusy == lung_size: #finished!
                go = False
            if mucusy < 0: # uh oh, went backwards too much, just stop...
                mucusy = 0
            if mucusx == lung_size: #loop around for periodic boundary condition
                mucusx = 0
            if mucusx < 0: #loop around for periodic boundary condition
                mucusx = lung_size -1
            time += 1 #increment the time
        time_list.append(time)
    return time_list        

def run_multi_model(stripes, speed_factor=10, lung_size=100, Nsim=10000, start_x=None, start_y=None):

    ##lung_size    = number of lung cells in each direction on a 2-D lattice
    ##stripes      = list where each entry is the number of rows before the same cell appears again for that run.  i.e. 1 is every other row, 2 is every two rows

    ##Nsim         = number of mucus particles to simulate sequence
    ##speed_factor = Factor by which it is faster to go forward with scilia than randomly without

    #if no start positions specified, default start in center at the farthest from end point position
    if start_x == None:
        start_x = lung_size/2
    if start_y == None:
        start_y = 0
        
    #check if stripes is a list or not:
    try:
        len(stripes)
    except:
        stripes=[stripes]

    diffusion_forces = np.ones((2,5))
    diffusion_forces[1,0] *= speed_factor

    #normalize diffusion forces, then append in the probability matrix.
    for i in range(np.shape(diffusion_forces)[0]):
        diffusion_forces[i,:] /= np.sum(diffusion_forces[i,:])

    diff_prob = np.copy(diffusion_forces)
    for i in range(5):
        if i == 0:
            pass
        else:
            diff_prob[:,i] += diff_prob[:,i-1]
            
    time_list = []
    ##debug
    #lung = np.ones((lung_size, lung_size)).astype(int)
    ##debug
    for strip in stripes:
        #make array representing your lung structure. 
        ## 0 = secretory cells
        ## 1 = ciliated cells
        alternation = strip
        lung = np.zeros((lung_size, lung_size)).astype(int)
        count = 0
        write = 1
        for i in range(lung_size):
            if count < alternation:
                count += 1
                lung[:,i] = write
                if count == alternation:
                    count = 0
                    if write == 1:
                        write = 0
                    else:
                        write = 1

        #run actual simulation
        tl = run_sim(Nsim, lung, diff_prob, lung_size, start_x, start_y)
        time_list.append(tl)
    return time_list
            
def histogram_all(time_list, stripes, spacing=100, title="plot", plot_axis=None):
    import matplotlib
    font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 20}

    matplotlib.rc('font', **font)
    
    import matplotlib.pyplot as plt
    
    
    #check to make sure everything that's a list is a list:
    try:
        len(stripes)
    except:
        stripes = [stripes]
    
    try:
        len(time_list[0])
    except:
        time_list = [time_list]
        
    plt.figure()
    maxt = 0
    for tl in time_list:
        if max(tl) > maxt:
            maxt = max(tl)
    
    maxt = (int(maxt/100)*100) + 100              
    bins = maxt/100
    for idx, strip in enumerate(stripes):
        plt.hist(time_list[idx], label="Stripe=%d"%strip, alpha=0.5, range=(0,maxt), bins=bins, normed=True)  
    
    plt.legend()
    plt.xlabel("Number of Time Steps")
    plt.ylabel("Counts")
    plt.title(title)
    plt.tight_layout()
    if not plot_axis == None:
        plt.axis(plot_axis)
    plt.savefig(title)
    plt.show()
          
def plot_stripes(stripes, lung_size):
    import matplotlib
    font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 20}

    matplotlib.rc('font', **font)
    
    import matplotlib.pyplot as plt
    
    #check to make sure everything that's a list is a list:
    try:
        len(stripes)
    except:
        stripes = [stripes]
    
    
    for strip in stripes:
        plt.figure()
        #make array representing your lung structure. 
        ## 0 = secretory cells
        ## 1 = ciliated cells
        alternation = strip
        lung = np.zeros((lung_size, lung_size)).astype(int)
        count = 0
        write = 1
        for i in range(lung_size):
            if count < alternation:
                count += 1
                lung[:,i] = write
                if count == alternation:
                    count = 0
                    if write == 1:
                        write = 0
                    else:
                        write = 1
        edges = np.arange(lung_size+1)                    
        qmesh = plt.pcolormesh(edges, edges, lung.transpose(), cmap="seismic")  
        #cbar = plt.colorbar(qmesh, ticks=[0,1])
        
        #cbar.ax.set_yticklabels(["Mucus","Scilia"])
        qmesh.axes.get_xaxis().set_visible(False)
        qmesh.axes.get_yaxis().set_visible(False)
        plt.savefig("Lung%d-Stripe%d"%(lung_size, strip))
            
            
        
        
