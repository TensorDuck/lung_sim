lung sim
========

For simulating a basic part of the lung.

Problems still need to be addressed:

1. The labels for the cell types is likely wrong, I spelled phonetically from memory.
2. The color bar for the stripe plot is not that good to look at still, but I have no idea what else to set them to.

Here's the basic use case:

go into the direcotyr
go into ipython

    import lung_sim 
    stripes=[1,2,4,10]
    lung_sim.plot_stripes(stripes, 100)
    time_list = lung_sim.run_multi_model(stripes)
    lung_sim.histogram_all(time_list, stripes)


This runs for a default setting of a 100x100 grid with a 10x Speed increase in the preferred direction of cilia. 

Currently, it randomly walks in x and y, it's goal is to reach y=lung_size starting at y=0. There is a periodic boundary condition in x, and any attempt to walk to y=-1 results in it being pushed back to y=0.

The possible actions are either right, left, up, down, hold still; all 5 with equal probability.

For the enhanced movement, the "right" option is multiplied by the speed_factor. 
