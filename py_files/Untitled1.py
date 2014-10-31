
# In[7]:

import scipy.spatial.distance as spd
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
import numpy as np
import time
# used to compare energy before and after a move
# we assumed that epsilon and alpha are 1
def local_energy(site):
    local_sum = 0
    for i in xrange(len(system)):
        if site != i:
            dist = spd.euclidean(system[site],system[i])
            local_sum += -((1/dist)**12-(1/dist)**6)
    return local_sum

# total energy of the system
def system_energy():
    total_sum = 0
    for i in xrange(len(system)):
        total_sum += local_energy(i)
    return total_sum

def radial_number_density():
    rad_dist = []
    for i in xrange(len(system)):
        for j in xrange(len(system)):
            if i != j:
                temp = spd.euclidean(system[i],system[j])
                rad_dist.append(temp)
    return rad_dist

n = 400 # number of particles
# initializing the system
# the atoms occupy a square of size 10X10
system = np.zeros([n,2])
for i in xrange(len(system)):
    system[i][0] = i%20 # np.sqrt(n) wont work as it will return a float
    system[i][1] = i/20 # we need an integer denominator for this to work!

global_energy = []
accepted_moves = 0

#plt.subplot(131)
radial_dist_before = radial_number_density()
#anarray = np.asarray(alist)
#plt.hist(anarray,10);

T = 1.
# T = np.array([5.,5./2,1./1./2,1./10])
beta = 1./T
# B = 1./T
#for beta in B:
time_per_loop = []
for looptime in xrange(1000):
    start_time = time.time()
    site = np.random.choice(np.arange(n)) # atom to be moved
    # this atom can now move in the range (-alpha,alpha) in x & y
    #xmove = np.random.choice(np.array([-2.,-5./3,-4./3,-1,-2./3,-1./3,0,1./3,2./3,1.,4./3,5./3,2.]))
    #ymove = np.random.choice(np.array([-2.,-5./3,-4./3,-1,-2./3,-1./3,0,1./3,2./3,1.,4./3,5./3,2.]))
    xmove = np.random.choice(np.array([0,1./3,2./3,1.,4./3,5./3,2.]))
    ymove = np.random.choice(np.array([0,1./3,2./3,1.,4./3,5./3,2.]))
    #xmove = np.random.choice(np.array([0.,1.,2.,3.,4.]))
    #ymove = np.random.choice(np.array([0.,1.,2.,3.,4.]))
    pre_move_e = local_energy(site)
    system[site] = system[site] + np.array([xmove,ymove])
    if system[site][0] > 30 :
        system[site][0] = system[site][0]%30
    #if system[site][0] < 0 :
    #    system[site][0] = system[site][0]%100
    if system[site][1] > 30 :
        system[site][1] = system[site][1]%30
    #if system[site][1] < 0 :
    #    system[site][1] = system[site][1]%100
    post_move_e = local_energy(site)
    if post_move_e - pre_move_e < 0:
        global_energy.append(system_energy())
        accepted_moves += 1
        print "yes"
    else :
        temp = np.random.random()
        if temp < np.exp(-beta*(post_move_e - pre_move_e)):
            global_energy.append(system_energy())
            accepted_moves += 1
            print "barely yes"
        else :
            system[site] = system[site] - np.array([xmove,ymove])
            global_energy.append(system_energy())
            print "nyooo!!!!"
    print "we're done with the mc loop %f" % (time.time()-start_time)
    time_per_loop.append(time.time()-start_time)
# we get global_energy, accepted moves as the outputs here.
#plt.subplot(132)
radial_dist_after = radial_number_density()
#anarray = np.asarray(alist)
#plt.hist(anarray,10);
#plt.subplot(133)
#plt.plot(global_energy)
#print "we're done with plotting routine %f" % (time.time()-start_time)
print "accepted_moves", accepted_moves


# Out[7]:

#     yes
#     we're done with the mc loop 7.540733
#     yes
#     we're done with the mc loop 5.782312
#     yes
#     we're done with the mc loop 7.439022
#     yes
#     we're done with the mc loop 7.346425
#     yes
#     we're done with the mc loop 7.362946
#     yes
#     we're done with the mc loop 7.817872
#     yes
#     we're done with the mc loop 9.267065
#     yes
#     we're done with the mc loop 9.263690
#     nyooo!!!!
#     we're done with the mc loop 9.274417
#     yes
#     we're done with the mc loop 8.685855
#     yes
#     we're done with the mc loop 5.781334
#     yes
#     we're done with the mc loop 8.091565
#     yes
#     we're done with the mc loop 7.281504
#     yes
#     we're done with the mc loop 7.285362
#     yes
#     we're done with the mc loop 8.034200
#     nyooo!!!!
#     we're done with the mc loop 9.252084
#     yes
#     we're done with the mc loop 8.183772
#     nyooo!!!!
#     we're done with the mc loop 8.729865
#     nyooo!!!!
#     we're done with the mc loop 10.021109
#     nyooo!!!!
#     we're done with the mc loop 8.070629
#     yes
#     we're done with the mc loop 8.546466
#     yes
#     we're done with the mc loop 9.929984
#     yes
#     we're done with the mc loop 9.019647
#     yes
#     we're done with the mc loop 6.440690
#     yes
#     we're done with the mc loop 9.250816
#     yes
#     we're done with the mc loop 8.843503
#     nyooo!!!!
#     we're done with the mc loop 7.590732
#     yes
#     we're done with the mc loop 7.375478
#     yes
#     we're done with the mc loop 7.636384
#     yes
#     we're done with the mc loop 8.146533
#     nyooo!!!!
#     we're done with the mc loop 7.345734
#     barely yes
#     we're done with the mc loop 7.303199
#     yes
#     we're done with the mc loop 7.370839
#     yes
#     we're done with the mc loop 7.379156
#     yes
#     we're done with the mc loop 8.474897
#     yes
#     we're done with the mc loop 9.271929
#     yes
#     we're done with the mc loop 9.278001
#     nyooo!!!!
#     we're done with the mc loop 9.261701
#     nyooo!!!!
#     we're done with the mc loop 9.279529
#     yes
#     we're done with the mc loop 9.296288
#     yes
#     we're done with the mc loop 9.277682
#     yes
#     we're done with the mc loop 9.296111
#     nyooo!!!!
#     we're done with the mc loop 9.290898
#     yes
#     we're done with the mc loop 9.249907
#     yes
#     we're done with the mc loop 9.270735
#     yes
#     we're done with the mc loop 9.282030
#     barely yes
#     we're done with the mc loop 9.250911
#     yes
#     we're done with the mc loop 9.266958
#     yes
#     we're done with the mc loop 9.283772
#     nyooo!!!!
#     we're done with the mc loop 9.276527
#     yes
#     we're done with the mc loop 9.286787
#     yes
#     we're done with the mc loop 9.284596
#     yes
#     we're done with the mc loop 9.275902
#     nyooo!!!!
#     we're done with the mc loop 9.279064
#     yes
#     we're done with the mc loop 6.729150
#     yes
#     we're done with the mc loop 5.538854
#     nyooo!!!!
#     we're done with the mc loop 5.548928
#     yes
#     we're done with the mc loop 9.795378
#     nyooo!!!!
#     we're done with the mc loop 7.136810
#     yes
#     we're done with the mc loop 7.325426
#     yes
#     we're done with the mc loop 8.384433
#     yes
#     we're done with the mc loop 8.286372
#     yes
#     we're done with the mc loop 7.311450
#     nyooo!!!!
#     we're done with the mc loop 7.377447
#     nyooo!!!!
#     we're done with the mc loop 7.402615
#     yes
#     we're done with the mc loop 5.574311
#     yes
#     we're done with the mc loop 7.485756
#     yes
#     we're done with the mc loop 7.295956
#     yes
#     we're done with the mc loop 6.257114
#     yes
#     we're done with the mc loop 6.377398
#     yes
#     we're done with the mc loop 7.294242
#     yes
#     we're done with the mc loop 7.301500
#     yes
#     we're done with the mc loop 9.540840
#     nyooo!!!!
#     we're done with the mc loop 8.336970
#     nyooo!!!!
#     we're done with the mc loop 11.174839
#     yes
#     we're done with the mc loop 10.415587
#     yes
#     we're done with the mc loop 8.874583
#     yes
#     we're done with the mc loop 9.777362
#     yes
#     we're done with the mc loop 9.343725
#     yes
#     we're done with the mc loop 10.639781
#     nyooo!!!!
#     we're done with the mc loop 7.846132
#     yes
#     we're done with the mc loop 9.724817
#     yes
#     we're done with the mc loop 9.248298
#     yes
#     we're done with the mc loop 9.775423
#     nyooo!!!!
#     we're done with the mc loop 10.331786
#     yes
#     we're done with the mc loop 11.369211
#     yes
#     we're done with the mc loop 9.375793
#     barely yes
#     we're done with the mc loop 8.969289
#     yes
#     we're done with the mc loop 8.955027
#     yes
#     we're done with the mc loop 10.646245
#     yes
#     we're done with the mc loop 11.502741
#     nyooo!!!!
#     we're done with the mc loop 9.895929
#     nyooo!!!!
#     we're done with the mc loop 11.556653
#     yes
#     we're done with the mc loop 11.284026
#     barely yes
#     we're done with the mc loop 11.382145
#     yes
#     we're done with the mc loop 10.302006
#     yes
#     we're done with the mc loop 9.108227
#     yes
#     we're done with the mc loop 11.232480
#     yes
#     we're done with the mc loop 9.501971
#     barely yes
#     we're done with the mc loop 9.289540
#     nyooo!!!!
#     we're done with the mc loop 11.210302
#     yes
#     we're done with the mc loop 12.276435
#     yes
#     we're done with the mc loop 12.316149
#     yes
#     we're done with the mc loop 11.216229
#     barely yes
#     we're done with the mc loop 12.607461
#     yes
#     we're done with the mc loop 12.410830
#     yes
#     we're done with the mc loop 9.647412
#     nyooo!!!!
#     we're done with the mc loop 11.339315
#     nyooo!!!!
#     we're done with the mc loop 11.257103
#     yes
#     we're done with the mc loop 13.525743
#     yes
#     we're done with the mc loop 10.575053
#     yes
#     we're done with the mc loop 10.938807
#     nyooo!!!!
#     we're done with the mc loop 12.522425
#     nyooo!!!!
#     we're done with the mc loop 13.204868
#     yes
#     we're done with the mc loop 12.630880
#     nyooo!!!!
#     we're done with the mc loop 11.924673
#     yes
#     we're done with the mc loop 11.281506
#     yes
#     we're done with the mc loop 9.259107
#     yes
#     we're done with the mc loop 11.767820
#     yes
#     we're done with the mc loop 11.622376
#     yes
#     we're done with the mc loop 13.500123
#     yes
#     we're done with the mc loop 9.996312
#     nyooo!!!!
#     we're done with the mc loop 7.818316
#     yes
#     we're done with the mc loop 10.636413
#     barely yes
#     we're done with the mc loop 8.092736
#     barely yes
#     we're done with the mc loop 11.537949
#     yes
#     we're done with the mc loop 11.290364
#     yes
#     we're done with the mc loop 7.623132
#     yes
#     we're done with the mc loop 10.328744
#     yes
#     we're done with the mc loop 8.723003
#     yes
#     we're done with the mc loop 8.409317
#     nyooo!!!!
#     we're done with the mc loop 8.497915
#     yes
#     we're done with the mc loop 8.731780
#     barely yes
#     we're done with the mc loop 7.777739
#     yes
#     we're done with the mc loop 9.454472
#     yes
#     we're done with the mc loop 7.464428
#     yes
#     we're done with the mc loop 9.568213
#     yes
#     we're done with the mc loop 8.086686
#     barely yes
#     we're done with the mc loop 9.203180
#     yes
#     we're done with the mc loop 7.912979
#     yes
#     we're done with the mc loop 9.086784
#     yes
#     we're done with the mc loop 8.291695
#     yes
#     we're done with the mc loop 10.343180
#     yes
#     we're done with the mc loop 10.326440
#     yes
#     we're done with the mc loop 8.364073
#     yes
#     we're done with the mc loop 8.750339
#     nyooo!!!!
#     we're done with the mc loop 10.018510
#     nyooo!!!!
#     we're done with the mc loop 9.191873
#     nyooo!!!!
#     we're done with the mc loop 7.661152
#     yes
#     we're done with the mc loop 9.800452
#     yes
#     we're done with the mc loop 7.433603
#     nyooo!!!!
#     we're done with the mc loop 9.436975
#     yes
#     we're done with the mc loop 7.457783
#     yes
#     we're done with the mc loop 10.102271
#     barely yes
#     we're done with the mc loop 7.437511
#     yes
#     we're done with the mc loop 9.547901
#     nyooo!!!!
#     we're done with the mc loop 8.366786
#     yes
#     we're done with the mc loop 9.014061
#     nyooo!!!!
#     we're done with the mc loop 8.800299
#     nyooo!!!!
#     we're done with the mc loop 9.979253
#     yes
#     we're done with the mc loop 11.845152
#     yes
#     we're done with the mc loop 10.207865
#     yes
#     we're done with the mc loop 11.692192
#     nyooo!!!!
#     we're done with the mc loop 12.826558
#     yes
#     we're done with the mc loop 15.312075
#     nyooo!!!!
#     we're done with the mc loop 13.091108
#     nyooo!!!!
#     we're done with the mc loop 9.723592
#     yes
#     we're done with the mc loop 10.019581
#     nyooo!!!!
#     we're done with the mc loop 9.188243
#     nyooo!!!!
#     we're done with the mc loop 9.199863
#     yes
#     we're done with the mc loop 9.188425
#     nyooo!!!!
#     we're done with the mc loop 9.205703
#     yes
#     we're done with the mc loop 9.872628
#     nyooo!!!!
#     we're done with the mc loop 10.259911
#     yes
#     we're done with the mc loop 9.162322
#     nyooo!!!!
#     we're done with the mc loop 8.544719
#     yes
#     we're done with the mc loop 10.321126
#     nyooo!!!!
#     we're done with the mc loop 9.201921
#     yes
#     we're done with the mc loop 10.539753
#     nyooo!!!!
#     we're done with the mc loop 9.486442
#     nyooo!!!!
#     we're done with the mc loop 9.053782
#     nyooo!!!!
#     we're done with the mc loop 7.808444
#     yes
#     we're done with the mc loop 11.124188
#     yes
#     we're done with the mc loop 13.223310
#     yes
#     we're done with the mc loop 9.962305
#     yes
#     we're done with the mc loop 11.024899
#     nyooo!!!!
#     we're done with the mc loop 9.467551
#     yes
#     we're done with the mc loop 7.603229
#     barely yes
#     we're done with the mc loop 9.275611
#     yes
#     we're done with the mc loop 7.969724
#     yes
#     we're done with the mc loop 9.516299
#     yes
#     we're done with the mc loop 7.731129
#     yes
#     we're done with the mc loop 9.511431
#     yes
#     we're done with the mc loop 7.607254
#     yes
#     we're done with the mc loop 9.583686
#     nyooo!!!!
#     we're done with the mc loop 7.824486
#     yes
#     we're done with the mc loop 9.642111
#     nyooo!!!!
#     we're done with the mc loop 7.668383
#     yes
#     we're done with the mc loop 9.780911
#     yes
#     we're done with the mc loop 7.529290
#     nyooo!!!!
#     we're done with the mc loop 9.200338
#     yes
#     we're done with the mc loop 7.719647
#     yes
#     we're done with the mc loop 9.374406
#     yes
#     we're done with the mc loop 7.431716
#     nyooo!!!!
#     we're done with the mc loop 8.835418
#     barely yes
#     we're done with the mc loop 8.383316
#     yes
#     we're done with the mc loop 9.729578
#     yes
#     we're done with the mc loop 7.726548
#     yes
#     we're done with the mc loop 9.599770
#     yes
#     we're done with the mc loop 7.559008
#     nyooo!!!!
#     we're done with the mc loop 9.637360
#     nyooo!!!!
#     we're done with the mc loop 12.275311
#     nyooo!!!!
#     we're done with the mc loop 12.875406
#     yes
#     we're done with the mc loop 11.666071
#     yes
#     we're done with the mc loop 9.604159
#     yes
#     we're done with the mc loop 7.758409
#     yes
#     we're done with the mc loop 8.246542
#     barely yes
#     we're done with the mc loop 8.811371
#     nyooo!!!!
#     we're done with the mc loop 7.541219
#     yes
#     we're done with the mc loop 9.403265
#     nyooo!!!!
#     we're done with the mc loop 10.693504
#     yes
#     we're done with the mc loop 11.668327
#     yes
#     we're done with the mc loop 7.432462
#     yes
#     we're done with the mc loop 8.935394
#     yes
#     we're done with the mc loop 12.600916
#     yes
#     we're done with the mc loop 12.504322
#     yes
#     we're done with the mc loop 7.788926
#     yes
#     we're done with the mc loop 9.433840
#     nyooo!!!!
#     we're done with the mc loop 7.897590
#     yes
#     we're done with the mc loop 8.390777
#     yes
#     we're done with the mc loop 7.434242
#     yes
#     we're done with the mc loop 9.350006
#     yes
#     we're done with the mc loop 11.825959
#     yes
#     we're done with the mc loop 7.621740
#     nyooo!!!!
#     we're done with the mc loop 7.514151
#     barely yes
#     we're done with the mc loop 8.747349
#     nyooo!!!!
#     we're done with the mc loop 7.894298
#     yes
#     we're done with the mc loop 7.665409
#     yes
#     we're done with the mc loop 9.013546
#     nyooo!!!!
#     we're done with the mc loop 7.513461
#     yes
#     we're done with the mc loop 9.754160
#     nyooo!!!!
#     we're done with the mc loop 7.537407
#     yes
#     we're done with the mc loop 8.811088
#     nyooo!!!!
#     we're done with the mc loop 8.874573
#     yes
#     we're done with the mc loop 13.762020
#     yes
#     we're done with the mc loop 9.490783
#     yes
#     we're done with the mc loop 9.067997
#     yes
#     we're done with the mc loop 7.438157
#     nyooo!!!!
#     we're done with the mc loop 8.267932
#     nyooo!!!!
#     we're done with the mc loop 8.592313
#     yes
#     we're done with the mc loop 7.329386
#     nyooo!!!!
#     we're done with the mc loop 10.349903
#     yes
#     we're done with the mc loop 12.518461
#     yes
#     we're done with the mc loop 8.175128
#     nyooo!!!!
#     we're done with the mc loop 8.862157
#     yes
#     we're done with the mc loop 7.588272
#     yes
#     we're done with the mc loop 8.819629
#     yes
#     we're done with the mc loop 7.982397
#     yes
#     we're done with the mc loop 7.458044
#     barely yes
#     we're done with the mc loop 9.222833
#     yes
#     we're done with the mc loop 7.449807
#     yes
#     we're done with the mc loop 9.442855
#     yes
#     we're done with the mc loop 7.419307
#     nyooo!!!!
#     we're done with the mc loop 9.640973
#     nyooo!!!!
#     we're done with the mc loop 8.218100
#     nyooo!!!!
#     we're done with the mc loop 10.575983
#     nyooo!!!!
#     we're done with the mc loop 9.183585
#     yes
#     we're done with the mc loop 9.194297
#     nyooo!!!!
#     we're done with the mc loop 9.158203
#     nyooo!!!!
#     we're done with the mc loop 9.183815
#     nyooo!!!!
#     we're done with the mc loop 8.537676
#     yes
#     we're done with the mc loop 7.873824
#     yes
#     we're done with the mc loop 8.810088
#     nyooo!!!!
#     we're done with the mc loop 10.051893
#     nyooo!!!!
#     we're done with the mc loop 7.467726
#     yes
#     we're done with the mc loop 9.579057
#     nyooo!!!!
#     we're done with the mc loop 8.736386
#     yes
#     we're done with the mc loop 9.187809
#     nyooo!!!!
#     we're done with the mc loop 9.177934
#     barely yes
#     we're done with the mc loop 8.952661
#     nyooo!!!!
#     we're done with the mc loop 8.528721
#     nyooo!!!!
#     we're done with the mc loop 9.646278
#     nyooo!!!!
#     we're done with the mc loop 7.731172
#     yes
#     we're done with the mc loop 10.042474
#     yes
#     we're done with the mc loop 9.175704
#     yes
#     we're done with the mc loop 9.204876
#     nyooo!!!!
#     we're done with the mc loop 9.179504
#     yes
#     we're done with the mc loop 9.201240
#     yes
#     we're done with the mc loop 9.197574
#     yes
#     we're done with the mc loop 8.521342
#     nyooo!!!!
#     we're done with the mc loop 8.383874
#     yes
#     we're done with the mc loop 8.570414
#     yes
#     we're done with the mc loop 7.694038
#     yes
#     we're done with the mc loop 8.982070
#     nyooo!!!!
#     we're done with the mc loop 7.387179
#     nyooo!!!!
#     we're done with the mc loop 9.812170
#     yes
#     we're done with the mc loop 11.958359
#     nyooo!!!!
#     we're done with the mc loop 9.610058
#     nyooo!!!!
#     we're done with the mc loop 7.328881
#     yes
#     we're done with the mc loop 7.876064
#     yes
#     we're done with the mc loop 13.603697
#     yes
#     we're done with the mc loop 7.702134
#     yes
#     we're done with the mc loop 7.398251
#     nyooo!!!!
#     we're done with the mc loop 9.153659
#     barely yes
#     we're done with the mc loop 7.469744
#     yes
#     we're done with the mc loop 9.579505
#     yes
#     we're done with the mc loop 7.469806
#     nyooo!!!!
#     we're done with the mc loop 12.016145
#     nyooo!!!!
#     we're done with the mc loop 10.648659
#     nyooo!!!!
#     we're done with the mc loop 12.161597
#     nyooo!!!!
#     we're done with the mc loop 7.775218
#     nyooo!!!!
#     we're done with the mc loop 11.080918
#     yes
#     we're done with the mc loop 9.184417
#     nyooo!!!!
#     we're done with the mc loop 11.071192
#     yes
#     we're done with the mc loop 7.449494
#     nyooo!!!!
#     we're done with the mc loop 7.353254
#     yes
#     we're done with the mc loop 9.220900
#     nyooo!!!!
#     we're done with the mc loop 7.459197
#     yes
#     we're done with the mc loop 9.341183
#     barely yes
#     we're done with the mc loop 7.386409
#     yes
#     we're done with the mc loop 9.656144
#     yes
#     we're done with the mc loop 9.196634
#     nyooo!!!!
#     we're done with the mc loop 7.684359
#     yes
#     we're done with the mc loop 9.421514
#     yes
#     we're done with the mc loop 7.689561
#     yes
#     we're done with the mc loop 9.624647
#     nyooo!!!!
#     we're done with the mc loop 7.472902
#     nyooo!!!!
#     we're done with the mc loop 9.394064
#     yes
#     we're done with the mc loop 7.369000
#     nyooo!!!!
#     we're done with the mc loop 8.859245
#     yes
#     we're done with the mc loop 7.947871
#     yes
#     we're done with the mc loop 9.765699
#     nyooo!!!!
#     we're done with the mc loop 9.187807
#     nyooo!!!!
#     we're done with the mc loop 9.200764
#     yes
#     we're done with the mc loop 9.167419
#     yes
#     we're done with the mc loop 9.186326
#     yes
#     we're done with the mc loop 9.177409
#     yes
#     we're done with the mc loop 9.170692
#     yes
#     we're done with the mc loop 8.848028
#     nyooo!!!!
#     we're done with the mc loop 7.530456
#     yes
#     we're done with the mc loop 10.186868
#     yes
#     we're done with the mc loop 12.528013
#     nyooo!!!!
#     we're done with the mc loop 9.168216
#     nyooo!!!!
#     we're done with the mc loop 7.738398
#     yes
#     we're done with the mc loop 9.234354
#     nyooo!!!!
#     we're done with the mc loop 7.861731
#     yes
#     we're done with the mc loop 8.369739
#     nyooo!!!!
#     we're done with the mc loop 8.801754
#     nyooo!!!!
#     we're done with the mc loop 10.626592
#     nyooo!!!!
#     we're done with the mc loop 10.761628
#     yes
#     we're done with the mc loop 8.319583
#     nyooo!!!!
#     we're done with the mc loop 10.033154
#     nyooo!!!!
#     we're done with the mc loop 7.335375
#     barely yes
#     we're done with the mc loop 8.199920
#     yes
#     we're done with the mc loop 8.604885
#     nyooo!!!!
#     we're done with the mc loop 7.531129
#     yes
#     we're done with the mc loop 9.258130
#     nyooo!!!!
#     we're done with the mc loop 7.591487
#     yes
#     we're done with the mc loop 9.050874
#     nyooo!!!!
#     we're done with the mc loop 7.366491
#     nyooo!!!!
#     we're done with the mc loop 9.264955
#     barely yes
#     we're done with the mc loop 7.459320
#     yes
#     we're done with the mc loop 9.339955
#     nyooo!!!!
#     we're done with the mc loop 7.714405
#     nyooo!!!!
#     we're done with the mc loop 8.917579
#     yes
#     we're done with the mc loop 7.879047
#     nyooo!!!!
#     we're done with the mc loop 8.387956
#     yes
#     we're done with the mc loop 8.618564
#     nyooo!!!!
#     we're done with the mc loop 11.887489
#     yes
#     we're done with the mc loop 8.983575
#     yes
#     we're done with the mc loop 7.748765
#     barely yes
#     we're done with the mc loop 7.673670
#     nyooo!!!!
#     we're done with the mc loop 9.107069
#     yes
#     we're done with the mc loop 8.266173
#     yes
#     we're done with the mc loop 7.731077
#     yes
#     we're done with the mc loop 9.521298
#     nyooo!!!!
#     we're done with the mc loop 7.455954
#     nyooo!!!!
#     we're done with the mc loop 9.405110
#     nyooo!!!!
#     we're done with the mc loop 9.364684
#     yes
#     we're done with the mc loop 9.178986
#     yes
#     we're done with the mc loop 8.051242
#     nyooo!!!!
#     we're done with the mc loop 8.912798
#     yes
#     we're done with the mc loop 8.772662
#     yes
#     we're done with the mc loop 8.506570
#     nyooo!!!!
#     we're done with the mc loop 9.040689
#     nyooo!!!!
#     we're done with the mc loop 8.151223
#     yes
#     we're done with the mc loop 9.487073
#     nyooo!!!!
#     we're done with the mc loop 8.939839
#     yes
#     we're done with the mc loop 9.177479
#     yes
#     we're done with the mc loop 9.197159
#     nyooo!!!!
#     we're done with the mc loop 8.915867
#     yes
#     we're done with the mc loop 7.774190
#     yes
#     we're done with the mc loop 9.458442
#     yes
#     we're done with the mc loop 8.057108
#     yes
#     we're done with the mc loop 9.091751
#     nyooo!!!!
#     we're done with the mc loop 8.076541
#     yes
#     we're done with the mc loop 9.093990
#     yes
#     we're done with the mc loop 9.779587
#     nyooo!!!!
#     we're done with the mc loop 9.184663
#     nyooo!!!!
#     we're done with the mc loop 7.896284
#     nyooo!!!!
#     we're done with the mc loop 9.485365
#     barely yes
#     we're done with the mc loop 8.153595
#     nyooo!!!!
#     we're done with the mc loop 10.518084
#     yes
#     we're done with the mc loop 9.188153
#     nyooo!!!!
#     we're done with the mc loop 9.180492
#     nyooo!!!!
#     we're done with the mc loop 9.200363
#     yes
#     we're done with the mc loop 9.165585
#     nyooo!!!!
#     we're done with the mc loop 8.233936
#     nyooo!!!!
#     we're done with the mc loop 7.540272
#     nyooo!!!!
#     we're done with the mc loop 10.418556
#     nyooo!!!!
#     we're done with the mc loop 11.023566
#     yes
#     we're done with the mc loop 10.153633
#     nyooo!!!!
#     we're done with the mc loop 12.420887
#     yes
#     we're done with the mc loop 12.603575
#     nyooo!!!!
#     we're done with the mc loop 12.261470
#     yes
#     we're done with the mc loop 7.559948
#     nyooo!!!!
#     we're done with the mc loop 11.385680
#     yes
#     we're done with the mc loop 10.889381
#     yes
#     we're done with the mc loop 7.998810
#     yes
#     we're done with the mc loop 8.532232
#     yes
#     we're done with the mc loop 7.670046
#     nyooo!!!!
#     we're done with the mc loop 10.043714
#     nyooo!!!!
#     we're done with the mc loop 9.173749
#     nyooo!!!!
#     we're done with the mc loop 8.067366
#     yes
#     we're done with the mc loop 9.571499
#     yes
#     we're done with the mc loop 9.186144
#     yes
#     we're done with the mc loop 9.185849
#     nyooo!!!!
#     we're done with the mc loop 7.872665
#     nyooo!!!!
#     we're done with the mc loop 9.346274
#     yes
#     we're done with the mc loop 8.569644
#     nyooo!!!!
#     we're done with the mc loop 8.848603
#     nyooo!!!!
#     we're done with the mc loop 12.236142
#     nyooo!!!!
#     we're done with the mc loop 8.490676
#     yes
#     we're done with the mc loop 9.453385
#     barely yes
#     we're done with the mc loop 8.943484
#     yes
#     we're done with the mc loop 9.189148
#     nyooo!!!!
#     we're done with the mc loop 7.629286
#     yes
#     we're done with the mc loop 10.029851
#     nyooo!!!!
#     we're done with the mc loop 11.428596
#     yes
#     we're done with the mc loop 11.179586
#     nyooo!!!!
#     we're done with the mc loop 7.554408
#     nyooo!!!!
#     we're done with the mc loop 9.490472
#     nyooo!!!!
#     we're done with the mc loop 7.306924
#     nyooo!!!!
#     we're done with the mc loop 9.431342
#     nyooo!!!!
#     we're done with the mc loop 7.793568
#     yes
#     we're done with the mc loop 9.454136
#     nyooo!!!!
#     we're done with the mc loop 6.762244
#     nyooo!!!!
#     we're done with the mc loop 9.329629
#     nyooo!!!!
#     we're done with the mc loop 7.432494
#     nyooo!!!!
#     we're done with the mc loop 9.614368
#     nyooo!!!!
#     we're done with the mc loop 7.507361
#     nyooo!!!!
#     we're done with the mc loop 9.445640
#     nyooo!!!!
#     we're done with the mc loop 7.561117
#     nyooo!!!!
#     we're done with the mc loop 9.518038
#     nyooo!!!!
#     we're done with the mc loop 7.586896
#     nyooo!!!!
#     we're done with the mc loop 9.454285
#     yes
#     we're done with the mc loop 7.461754
#     nyooo!!!!
#     we're done with the mc loop 9.439256
#     yes
#     we're done with the mc loop 7.512987
#     nyooo!!!!
#     we're done with the mc loop 9.311501
#     nyooo!!!!
#     we're done with the mc loop 7.547344
#     nyooo!!!!
#     we're done with the mc loop 9.419927
#     yes
#     we're done with the mc loop 7.877984
#     nyooo!!!!
#     we're done with the mc loop 10.518600
#     yes
#     we're done with the mc loop 9.174104
#     yes
#     we're done with the mc loop 9.189314
#     nyooo!!!!
#     we're done with the mc loop 9.161909
#     yes
#     we're done with the mc loop 9.205145
#     nyooo!!!!
#     we're done with the mc loop 7.920646
#     nyooo!!!!
#     we're done with the mc loop 8.731387
#     yes
#     we're done with the mc loop 9.179108
#     barely yes
#     we're done with the mc loop 9.198572
#     yes
#     we're done with the mc loop 9.173283
#     nyooo!!!!
#     we're done with the mc loop 9.205908
#     yes
#     we're done with the mc loop 7.599698
#     nyooo!!!!
#     we're done with the mc loop 8.481808
#     nyooo!!!!
#     we're done with the mc loop 7.278273
#     nyooo!!!!
#     we're done with the mc loop 6.924770
#     nyooo!!!!
#     we're done with the mc loop 7.177978
#     nyooo!!!!
#     we're done with the mc loop 8.633882
#     yes
#     we're done with the mc loop 6.964008
#     nyooo!!!!
#     we're done with the mc loop 6.971472
#     nyooo!!!!
#     we're done with the mc loop 8.207177
#     nyooo!!!!
#     we're done with the mc loop 7.547478
#     nyooo!!!!
#     we're done with the mc loop 6.962514
#     nyooo!!!!
#     we're done with the mc loop 7.135434
#     nyooo!!!!
#     we're done with the mc loop 8.948293
#     nyooo!!!!
#     we're done with the mc loop 7.307958
#     yes
#     we're done with the mc loop 7.341421
#     nyooo!!!!
#     we're done with the mc loop 7.033928
#     nyooo!!!!
#     we're done with the mc loop 7.464263
#     yes
#     we're done with the mc loop 8.366677
#     nyooo!!!!
#     we're done with the mc loop 6.962205
#     yes
#     we're done with the mc loop 7.055415
#     nyooo!!!!
#     we're done with the mc loop 8.098453
#     yes
#     we're done with the mc loop 7.650346
#     yes
#     we're done with the mc loop 6.986583
#     nyooo!!!!
#     we're done with the mc loop 7.480253
#     nyooo!!!!
#     we're done with the mc loop 10.419756
#     yes
#     we're done with the mc loop 8.063429
#     yes
#     we're done with the mc loop 7.082077
#     yes
#     we're done with the mc loop 7.046895
#     nyooo!!!!
#     we're done with the mc loop 7.433230
#     barely yes
#     we're done with the mc loop 8.342419
#     nyooo!!!!
#     we're done with the mc loop 9.179273
#     nyooo!!!!
#     we're done with the mc loop 9.177708
#     nyooo!!!!
#     we're done with the mc loop 9.186736
#     nyooo!!!!
#     we're done with the mc loop 9.185234
#     nyooo!!!!
#     we're done with the mc loop 8.036516
#     yes
#     we're done with the mc loop 6.865127
#     yes
#     we're done with the mc loop 8.187314
#     yes
#     we're done with the mc loop 7.524629
#     yes
#     we're done with the mc loop 6.954516
#     nyooo!!!!
#     we're done with the mc loop 7.007747
#     nyooo!!!!
#     we're done with the mc loop 8.964068
#     yes
#     we're done with the mc loop 7.984748
#     nyooo!!!!
#     we're done with the mc loop 9.181013
#     yes
#     we're done with the mc loop 9.169186
#     nyooo!!!!
#     we're done with the mc loop 9.190268
#     nyooo!!!!
#     we're done with the mc loop 7.715326
#     nyooo!!!!
#     we're done with the mc loop 9.503177
#     yes
#     we're done with the mc loop 10.903997
#     nyooo!!!!
#     we're done with the mc loop 10.830596
#     yes
#     we're done with the mc loop 9.179005
#     yes
#     we're done with the mc loop 10.767021
#     nyooo!!!!
#     we're done with the mc loop 10.151451
#     yes
#     we're done with the mc loop 9.111253
#     nyooo!!!!
#     we're done with the mc loop 7.813580
#     nyooo!!!!
#     we're done with the mc loop 6.838114
#     nyooo!!!!
#     we're done with the mc loop 6.950891
#     yes
#     we're done with the mc loop 7.003113
#     nyooo!!!!
#     we're done with the mc loop 8.624584
#     nyooo!!!!
#     we're done with the mc loop 8.057744
#     yes
#     we're done with the mc loop 9.199866
#     yes
#     we're done with the mc loop 9.199507
#     yes
#     we're done with the mc loop 9.176459
#     yes
#     we're done with the mc loop 9.190178
#     yes
#     we're done with the mc loop 9.196585
#     yes
#     we're done with the mc loop 9.159782
#     nyooo!!!!
#     we're done with the mc loop 9.184987
#     nyooo!!!!
#     we're done with the mc loop 9.183534
#     barely yes
#     we're done with the mc loop 7.633529
#     nyooo!!!!
#     we're done with the mc loop 7.042255
#     nyooo!!!!
#     we're done with the mc loop 8.995261
#     yes
#     we're done with the mc loop 6.895009
#     nyooo!!!!
#     we're done with the mc loop 7.074284
#     nyooo!!!!
#     we're done with the mc loop 7.390571
#     nyooo!!!!
#     we're done with the mc loop 8.395421
#     nyooo!!!!
#     we're done with the mc loop 6.888451
#     nyooo!!!!
#     we're done with the mc loop 6.973766
#     nyooo!!!!
#     we're done with the mc loop 6.986603
#     nyooo!!!!
#     we're done with the mc loop 8.581813
#     nyooo!!!!
#     we're done with the mc loop 7.177971
#     nyooo!!!!
#     we're done with the mc loop 6.811966
#     nyooo!!!!
#     we're done with the mc loop 7.819254
#     yes
#     we're done with the mc loop 8.044980
#     barely yes
#     we're done with the mc loop 6.942923
#     yes
#     we're done with the mc loop 7.010813
#     nyooo!!!!
#     we're done with the mc loop 8.859856
#     nyooo!!!!
#     we're done with the mc loop 7.192317
#     nyooo!!!!
#     we're done with the mc loop 10.012644
#     yes
#     we're done with the mc loop 9.178211
#     barely yes
#     we're done with the mc loop 9.177848
#     nyooo!!!!
#     we're done with the mc loop 9.175991
#     barely yes
#     we're done with the mc loop 9.181321
#     yes
#     we're done with the mc loop 9.167000
#     nyooo!!!!
#     we're done with the mc loop 9.177093
#     yes
#     we're done with the mc loop 9.199166
#     nyooo!!!!
#     we're done with the mc loop 9.158255
#     nyooo!!!!
#     we're done with the mc loop 7.564601
#     barely yes
#     we're done with the mc loop 7.011042
#     nyooo!!!!
#     we're done with the mc loop 7.109995
#     nyooo!!!!
#     we're done with the mc loop 8.353875
#     yes
#     we're done with the mc loop 7.392290
#     nyooo!!!!
#     we're done with the mc loop 7.086734
#     nyooo!!!!
#     we're done with the mc loop 7.358598
#     nyooo!!!!
#     we're done with the mc loop 8.381668
#     nyooo!!!!
#     we're done with the mc loop 6.988252
#     nyooo!!!!
#     we're done with the mc loop 9.792729
#     yes
#     we're done with the mc loop 7.900880
#     yes
#     we're done with the mc loop 7.741895
#     nyooo!!!!
#     we're done with the mc loop 7.963684
#     nyooo!!!!
#     we're done with the mc loop 6.919306
#     nyooo!!!!
#     we're done with the mc loop 6.924465
#     nyooo!!!!
#     we're done with the mc loop 8.128411
#     barely yes
#     we're done with the mc loop 11.338661
#     nyooo!!!!
#     we're done with the mc loop 11.911017
#     nyooo!!!!
#     we're done with the mc loop 6.941759
#     nyooo!!!!
#     we're done with the mc loop 6.818066
#     yes
#     we're done with the mc loop 11.353260
#     barely yes
#     we're done with the mc loop 9.169083
#     yes
#     we're done with the mc loop 8.456904
#     nyooo!!!!
#     we're done with the mc loop 6.783056
#     nyooo!!!!
#     we're done with the mc loop 7.942759
#     yes
#     we're done with the mc loop 7.649149
#     yes
#     we're done with the mc loop 6.934250
#     yes
#     we're done with the mc loop 6.957454
#     nyooo!!!!
#     we're done with the mc loop 7.332900
#     yes
#     we're done with the mc loop 8.266061
#     yes
#     we're done with the mc loop 6.996430
#     nyooo!!!!
#     we're done with the mc loop 6.913731
#     barely yes
#     we're done with the mc loop 7.984568
#     barely yes
#     we're done with the mc loop 7.706566
#     nyooo!!!!
#     we're done with the mc loop 7.010139
#     nyooo!!!!
#     we're done with the mc loop 7.143850
#     nyooo!!!!
#     we're done with the mc loop 8.635764
#     yes
#     we're done with the mc loop 6.911508
#     nyooo!!!!
#     we're done with the mc loop 6.928599
#     yes
#     we're done with the mc loop 8.384815
#     nyooo!!!!
#     we're done with the mc loop 7.485034
#     nyooo!!!!
#     we're done with the mc loop 6.951891
#     yes
#     we're done with the mc loop 7.364075
#     yes
#     we're done with the mc loop 8.180496
#     yes
#     we're done with the mc loop 7.019797
#     nyooo!!!!
#     we're done with the mc loop 6.986425
#     nyooo!!!!
#     we're done with the mc loop 8.458565
#     nyooo!!!!
#     we're done with the mc loop 7.380502
#     nyooo!!!!
#     we're done with the mc loop 6.966904
#     nyooo!!!!
#     we're done with the mc loop 7.082587
#     nyooo!!!!
#     we're done with the mc loop 8.492293
#     yes
#     we're done with the mc loop 7.265139
#     yes
#     we're done with the mc loop 7.048463
#     yes
#     we're done with the mc loop 8.639207
#     nyooo!!!!
#     we're done with the mc loop 6.998477
#     nyooo!!!!
#     we're done with the mc loop 7.017765
#     yes
#     we're done with the mc loop 7.395889
#     yes
#     we're done with the mc loop 8.142167
#     yes
#     we're done with the mc loop 6.965463
#     nyooo!!!!
#     we're done with the mc loop 7.041619
#     nyooo!!!!
#     we're done with the mc loop 8.574366
#     yes
#     we're done with the mc loop 7.124361
#     nyooo!!!!
#     we're done with the mc loop 7.062329
#     yes
#     we're done with the mc loop 8.639308
#     nyooo!!!!
#     we're done with the mc loop 7.519648
#     nyooo!!!!
#     we're done with the mc loop 6.973833
#     nyooo!!!!
#     we're done with the mc loop 11.855110
#     yes
#     we're done with the mc loop 11.592904
#     nyooo!!!!
#     we're done with the mc loop 11.642280
#     nyooo!!!!
#     we're done with the mc loop 9.160442
#     nyooo!!!!
#     we're done with the mc loop 10.761810
#     barely yes
#     we're done with the mc loop 7.449707
#     nyooo!!!!
#     we're done with the mc loop 8.035775
#     nyooo!!!!
#     we're done with the mc loop 7.422067
#     yes
#     we're done with the mc loop 8.082995
#     yes
#     we're done with the mc loop 9.185272
#     nyooo!!!!
#     we're done with the mc loop 7.260871
#     nyooo!!!!
#     we're done with the mc loop 8.415285
#     yes
#     we're done with the mc loop 6.961004
#     nyooo!!!!
#     we're done with the mc loop 8.448646
#     nyooo!!!!
#     we're done with the mc loop 11.666317
#     nyooo!!!!
#     we're done with the mc loop 9.186373
#     nyooo!!!!
#     we're done with the mc loop 9.187674
#     nyooo!!!!
#     we're done with the mc loop 10.825306
#     yes
#     we're done with the mc loop 8.355812
#     nyooo!!!!
#     we're done with the mc loop 8.086065
#     nyooo!!!!
#     we're done with the mc loop 6.956611
#     yes
#     we're done with the mc loop 6.943143
#     yes
#     we're done with the mc loop 7.350819
#     nyooo!!!!
#     we're done with the mc loop 8.185934
#     yes
#     we're done with the mc loop 7.917546
#     nyooo!!!!
#     we're done with the mc loop 9.188104
#     nyooo!!!!
#     we're done with the mc loop 7.552900
#     nyooo!!!!
#     we're done with the mc loop 9.667820
#     nyooo!!!!
#     we're done with the mc loop 8.039715
#     nyooo!!!!
#     we're done with the mc loop 7.674200
#     nyooo!!!!
#     we're done with the mc loop 9.985623
#     nyooo!!!!
#     we're done with the mc loop 9.108553
#     nyooo!!!!
#     we're done with the mc loop 12.379006
#     nyooo!!!!
#     we're done with the mc loop 9.166615
#     nyooo!!!!
#     we're done with the mc loop 9.220902
#     nyooo!!!!
#     we're done with the mc loop 9.070410
#     nyooo!!!!
#     we're done with the mc loop 7.813797
#     nyooo!!!!
#     we're done with the mc loop 8.288066
#     yes
#     we're done with the mc loop 10.349708
#     nyooo!!!!
#     we're done with the mc loop 8.933368
#     yes
#     we're done with the mc loop 8.017293
#     nyooo!!!!
#     we're done with the mc loop 10.783593
#     nyooo!!!!
#     we're done with the mc loop 7.354866
#     nyooo!!!!
#     we're done with the mc loop 10.873111
#     nyooo!!!!
#     we're done with the mc loop 8.279120
#     yes
#     we're done with the mc loop 9.309020
#     nyooo!!!!
#     we're done with the mc loop 10.677704
#     nyooo!!!!
#     we're done with the mc loop 7.522108
#     yes
#     we're done with the mc loop 12.134480
#     nyooo!!!!
#     we're done with the mc loop 9.295862
#     nyooo!!!!
#     we're done with the mc loop 8.103892
#     nyooo!!!!
#     we're done with the mc loop 8.351679
#     nyooo!!!!
#     we're done with the mc loop 9.219285
#     nyooo!!!!
#     we're done with the mc loop 9.121629
#     nyooo!!!!
#     we're done with the mc loop 9.671271
#     nyooo!!!!
#     we're done with the mc loop 7.775843
#     barely yes
#     we're done with the mc loop 8.705759
#     nyooo!!!!
#     we're done with the mc loop 8.744946
#     nyooo!!!!
#     we're done with the mc loop 8.963450
#     nyooo!!!!
#     we're done with the mc loop 7.735851
#     barely yes
#     we're done with the mc loop 9.380464
#     nyooo!!!!
#     we're done with the mc loop 10.512876
#     nyooo!!!!
#     we're done with the mc loop 7.860860
#     nyooo!!!!
#     we're done with the mc loop 7.658976
#     nyooo!!!!
#     we're done with the mc loop 8.631883
#     nyooo!!!!
#     we're done with the mc loop 10.852521
#     nyooo!!!!
#     we're done with the mc loop 7.938101
#     nyooo!!!!
#     we're done with the mc loop 8.441397
#     nyooo!!!!
#     we're done with the mc loop 7.962073
#     nyooo!!!!
#     we're done with the mc loop 8.662402
#     nyooo!!!!
#     we're done with the mc loop 7.844486
#     nyooo!!!!
#     we're done with the mc loop 7.504681
#     nyooo!!!!
#     we're done with the mc loop 9.199352
#     yes
#     we're done with the mc loop 8.683494
#     nyooo!!!!
#     we're done with the mc loop 9.178823
#     nyooo!!!!
#     we're done with the mc loop 9.313754
#     nyooo!!!!
#     we're done with the mc loop 8.273626
#     yes
#     we're done with the mc loop 8.228517
#     nyooo!!!!
#     we're done with the mc loop 11.129883
#     nyooo!!!!
#     we're done with the mc loop 10.382438
#     nyooo!!!!
#     we're done with the mc loop 8.732349
#     nyooo!!!!
#     we're done with the mc loop 11.019876
#     nyooo!!!!
#     we're done with the mc loop 7.549750
#     nyooo!!!!
#     we're done with the mc loop 9.100909
#     nyooo!!!!
#     we're done with the mc loop 7.591903
#     yes
#     we're done with the mc loop 9.122107
#     nyooo!!!!
#     we're done with the mc loop 10.767617
#     nyooo!!!!
#     we're done with the mc loop 8.308360
#     nyooo!!!!
#     we're done with the mc loop 8.978809
#     nyooo!!!!
#     we're done with the mc loop 8.210291
#     nyooo!!!!
#     we're done with the mc loop 8.692060
#     yes
#     we're done with the mc loop 8.413951
#     nyooo!!!!
#     we're done with the mc loop 8.221362
#     nyooo!!!!
#     we're done with the mc loop 8.655036
#     nyooo!!!!
#     we're done with the mc loop 9.454529
#     nyooo!!!!
#     we're done with the mc loop 7.831041
#     yes
#     we're done with the mc loop 9.969500
#     nyooo!!!!
#     we're done with the mc loop 12.821718
#     nyooo!!!!
#     we're done with the mc loop 9.365366
#     nyooo!!!!
#     we're done with the mc loop 9.225079
#     nyooo!!!!
#     we're done with the mc loop 8.538576
#     yes
#     we're done with the mc loop 9.200361
#     nyooo!!!!
#     we're done with the mc loop 9.236867
#     yes
#     we're done with the mc loop 9.264662
#     nyooo!!!!
#     we're done with the mc loop 9.182012
#     nyooo!!!!
#     we're done with the mc loop 9.182681
#     nyooo!!!!
#     we're done with the mc loop 9.196284
#     nyooo!!!!
#     we're done with the mc loop 8.743368
#     yes
#     we're done with the mc loop 8.181481
#     nyooo!!!!
#     we're done with the mc loop 9.267692
#     yes
#     we're done with the mc loop 9.229998
#     nyooo!!!!
#     we're done with the mc loop 8.921427
#     yes
#     we're done with the mc loop 7.663414
#     yes
#     we're done with the mc loop 9.069023
#     nyooo!!!!
#     we're done with the mc loop 8.003803
#     yes
#     we're done with the mc loop 9.531248
#     nyooo!!!!
#     we're done with the mc loop 9.725301
#     nyooo!!!!
#     we're done with the mc loop 10.826521
#     nyooo!!!!
#     we're done with the mc loop 11.890605
#     nyooo!!!!
#     we're done with the mc loop 13.454782
#     nyooo!!!!
#     we're done with the mc loop 7.670382
#     nyooo!!!!
#     we're done with the mc loop 9.504810
#     yes
#     we're done with the mc loop 8.068964
#     nyooo!!!!
#     we're done with the mc loop 8.466977
#     nyooo!!!!
#     we're done with the mc loop 7.412067
#     yes
#     we're done with the mc loop 7.340786
#     nyooo!!!!
#     we're done with the mc loop 7.435370
#     nyooo!!!!
#     we're done with the mc loop 7.431157
#     nyooo!!!!
#     we're done with the mc loop 7.339430
#     yes
#     we're done with the mc loop 8.042032
#     nyooo!!!!
#     we're done with the mc loop 7.664703
#     yes
#     we're done with the mc loop 7.570534
#     nyooo!!!!
#     we're done with the mc loop 9.216790
#     nyooo!!!!
#     we're done with the mc loop 9.190308
#     nyooo!!!!
#     we're done with the mc loop 9.169450
#     nyooo!!!!
#     we're done with the mc loop 7.768214
#     nyooo!!!!
#     we're done with the mc loop 7.323493
#     yes
#     we're done with the mc loop 7.338191
#     nyooo!!!!
#     we're done with the mc loop 7.325430
#     yes
#     we're done with the mc loop 6.571118
#     nyooo!!!!
#     we're done with the mc loop 8.211222
#     nyooo!!!!
#     we're done with the mc loop 7.832550
#     nyooo!!!!
#     we're done with the mc loop 7.392306
#     nyooo!!!!
#     we're done with the mc loop 7.214086
#     nyooo!!!!
#     we're done with the mc loop 7.390701
#     nyooo!!!!
#     we're done with the mc loop 8.491075
#     nyooo!!!!
#     we're done with the mc loop 9.162912
#     nyooo!!!!
#     we're done with the mc loop 9.184086
#     nyooo!!!!
#     we're done with the mc loop 9.092939
#     nyooo!!!!
#     we're done with the mc loop 5.592842
#     barely yes
#     we're done with the mc loop 7.468127
#     yes
#     we're done with the mc loop 7.776304
#     nyooo!!!!
#     we're done with the mc loop 7.267508
#     nyooo!!!!
#     we're done with the mc loop 7.296733
#     nyooo!!!!
#     we're done with the mc loop 7.420238
#     nyooo!!!!
#     we're done with the mc loop 8.974631
#     nyooo!!!!
#     we're done with the mc loop 9.195676
#     nyooo!!!!
#     we're done with the mc loop 9.193142
#     nyooo!!!!
#     we're done with the mc loop 9.171754
#     nyooo!!!!
#     we're done with the mc loop 9.180212
#     nyooo!!!!
#     we're done with the mc loop 9.188291
#     nyooo!!!!
#     we're done with the mc loop 9.168807
#     nyooo!!!!
#     we're done with the mc loop 9.188315
#     nyooo!!!!
#     we're done with the mc loop 8.179110
#     nyooo!!!!
#     we're done with the mc loop 9.171546
#     nyooo!!!!
#     we're done with the mc loop 9.151435
#     nyooo!!!!
#     we're done with the mc loop 9.183262
#     nyooo!!!!
#     we're done with the mc loop 9.169602
#     barely yes
#     we're done with the mc loop 9.182805
#     nyooo!!!!
#     we're done with the mc loop 7.392418
#     barely yes
#     we're done with the mc loop 7.764001
#     nyooo!!!!
#     we're done with the mc loop 5.653410
#     nyooo!!!!
#     we're done with the mc loop 7.329411
#     nyooo!!!!
#     we're done with the mc loop 7.404432
#     nyooo!!!!
#     we're done with the mc loop 7.350623
#     nyooo!!!!
#     we're done with the mc loop 7.780778
#     yes
#     we're done with the mc loop 7.555396
#     nyooo!!!!
#     we're done with the mc loop 8.021925
#     nyooo!!!!
#     we're done with the mc loop 8.373789
#     yes
#     we're done with the mc loop 5.563270
#     nyooo!!!!
#     we're done with the mc loop 7.388204
#     nyooo!!!!
#     we're done with the mc loop 8.372680
#     nyooo!!!!
#     we're done with the mc loop 6.965201
#     yes
#     we're done with the mc loop 9.112251
#     yes
#     we're done with the mc loop 7.490762
#     yes
#     we're done with the mc loop 7.443098
#     yes
#     we're done with the mc loop 9.208763
#     yes
#     we're done with the mc loop 7.353411
#     nyooo!!!!
#     we're done with the mc loop 8.706099
#     nyooo!!!!
#     we're done with the mc loop 8.589885
#     yes
#     we're done with the mc loop 5.558251
#     nyooo!!!!
#     we're done with the mc loop 7.420051
#     nyooo!!!!
#     we're done with the mc loop 9.976227
#     nyooo!!!!
#     we're done with the mc loop 7.272518
#     nyooo!!!!
#     we're done with the mc loop 8.746350
#     nyooo!!!!
#     we're done with the mc loop 5.544851
#     nyooo!!!!
#     we're done with the mc loop 7.280745
#     nyooo!!!!
#     we're done with the mc loop 7.695853
#     nyooo!!!!
#     we're done with the mc loop 10.175614
#     yes
#     we're done with the mc loop 9.295622
#     nyooo!!!!
#     we're done with the mc loop 9.269220
#     yes
#     we're done with the mc loop 7.293728
#     yes
#     we're done with the mc loop 8.787512
#     nyooo!!!!
#     we're done with the mc loop 9.279039
#     yes
#     we're done with the mc loop 9.289563
#     nyooo!!!!
#     we're done with the mc loop 6.318762
#     nyooo!!!!
#     we're done with the mc loop 7.960848
#     nyooo!!!!
#     we're done with the mc loop 8.622233
#     barely yes
#     we're done with the mc loop 7.476822
#     nyooo!!!!
#     we're done with the mc loop 7.374675
#     yes
#     we're done with the mc loop 6.781675
#     nyooo!!!!
#     we're done with the mc loop 8.122381
#     nyooo!!!!
#     we're done with the mc loop 7.501942
#     nyooo!!!!
#     we're done with the mc loop 6.678376
#     nyooo!!!!
#     we're done with the mc loop 9.770402
#     nyooo!!!!
#     we're done with the mc loop 7.474232
#     nyooo!!!!
#     we're done with the mc loop 7.247790
#     yes
#     we're done with the mc loop 7.418026
#     nyooo!!!!
#     we're done with the mc loop 5.657168
#     nyooo!!!!
#     we're done with the mc loop 8.456597
#     nyooo!!!!
#     we're done with the mc loop 9.956179
#     nyooo!!!!
#     we're done with the mc loop 8.320357
#     yes
#     we're done with the mc loop 7.391859
#     yes
#     we're done with the mc loop 7.474804
#     nyooo!!!!
#     we're done with the mc loop 7.696692
#     nyooo!!!!
#     we're done with the mc loop 8.725008
#     nyooo!!!!
#     we're done with the mc loop 7.862408
#     yes
#     we're done with the mc loop 7.737063
#     nyooo!!!!
#     we're done with the mc loop 12.160880
#     nyooo!!!!
#     we're done with the mc loop 12.372678
#     nyooo!!!!
#     we're done with the mc loop 12.520266
#     yes
#     we're done with the mc loop 10.582484
#     yes
#     we're done with the mc loop 9.742596
#     yes
#     we're done with the mc loop 8.060188
#     nyooo!!!!
#     we're done with the mc loop 7.931944
#     nyooo!!!!
#     we're done with the mc loop 10.419170
#     nyooo!!!!
#     we're done with the mc loop 8.928824
#     yes
#     we're done with the mc loop 8.577095
#     nyooo!!!!
#     we're done with the mc loop 7.890080
#     yes
#     we're done with the mc loop 11.493017
#     nyooo!!!!
#     we're done with the mc loop 12.056752
#     nyooo!!!!
#     we're done with the mc loop 11.977361
#     yes
#     we're done with the mc loop 11.765460
#     nyooo!!!!
#     we're done with the mc loop 9.753439
#     yes
#     we're done with the mc loop 11.663709
#     nyooo!!!!
#     we're done with the mc loop 12.751735
#     nyooo!!!!
#     we're done with the mc loop 13.342378
#     nyooo!!!!
#     we're done with the mc loop 13.472055
#     barely yes
#     we're done with the mc loop 10.589537
#     yes
#     we're done with the mc loop 12.755041
#     nyooo!!!!
#     we're done with the mc loop 8.463925
#     yes
#     we're done with the mc loop 11.745578
#     nyooo!!!!
#     we're done with the mc loop 14.458701
#     nyooo!!!!
#     we're done with the mc loop 9.083290
#     nyooo!!!!
#     we're done with the mc loop 12.509697
#     nyooo!!!!
#     we're done with the mc loop 14.619633
#     barely yes
#     we're done with the mc loop 8.469171
#     nyooo!!!!
#     we're done with the mc loop 11.116754
#     nyooo!!!!
#     we're done with the mc loop 12.739903
#     nyooo!!!!
#     we're done with the mc loop 13.324590
#     nyooo!!!!
#     we're done with the mc loop 12.487322
#     nyooo!!!!
#     we're done with the mc loop 11.947465
#     yes
#     we're done with the mc loop 13.444001
#     nyooo!!!!
#     we're done with the mc loop 11.498786
#     yes
#     we're done with the mc loop 13.098700
#     nyooo!!!!
#     we're done with the mc loop 11.701680
#     nyooo!!!!
#     we're done with the mc loop 11.061875
#     nyooo!!!!
#     we're done with the mc loop 12.547860
#     nyooo!!!!
#     we're done with the mc loop 11.684051
#     barely yes
#     we're done with the mc loop 12.381222
#     yes
#     we're done with the mc loop 11.467295
#     nyooo!!!!
#     we're done with the mc loop 8.757381
#     nyooo!!!!
#     we're done with the mc loop 12.244458
#     yes
#     we're done with the mc loop 8.864559
#     nyooo!!!!
#     we're done with the mc loop 8.720297
#     nyooo!!!!
#     we're done with the mc loop 9.781083
#     nyooo!!!!
#     we're done with the mc loop 8.599594
#     nyooo!!!!
#     we're done with the mc loop 9.870635
#     nyooo!!!!
#     we're done with the mc loop 11.314972
#     nyooo!!!!
#     we're done with the mc loop 13.422171
#     nyooo!!!!
#     we're done with the mc loop 12.604826
#     nyooo!!!!
#     we're done with the mc loop 13.103826
#     barely yes
#     we're done with the mc loop 12.498687
#     nyooo!!!!
#     we're done with the mc loop 11.056562
#     nyooo!!!!
#     we're done with the mc loop 9.495200
#     yes
#     we're done with the mc loop 8.105980
#     nyooo!!!!
#     we're done with the mc loop 10.757948
#     nyooo!!!!
#     we're done with the mc loop 11.258893
#     nyooo!!!!
#     we're done with the mc loop 13.142254
#     nyooo!!!!
#     we're done with the mc loop 13.440705
#     nyooo!!!!
#     we're done with the mc loop 8.688815
#     nyooo!!!!
#     we're done with the mc loop 11.579163
#     nyooo!!!!
#     we're done with the mc loop 12.698273
#     yes
#     we're done with the mc loop 11.618016
#     nyooo!!!!
#     we're done with the mc loop 10.514111
#     nyooo!!!!
#     we're done with the mc loop 11.920476
#     nyooo!!!!
#     we're done with the mc loop 12.719058
#     nyooo!!!!
#     we're done with the mc loop 11.474301
#     nyooo!!!!
#     we're done with the mc loop 13.249700
#     yes
#     we're done with the mc loop 14.253921
#     nyooo!!!!
#     we're done with the mc loop 12.925233
#     nyooo!!!!
#     we're done with the mc loop 11.812592
#     nyooo!!!!
#     we're done with the mc loop 13.172600
#     nyooo!!!!
#     we're done with the mc loop 11.812338
#     yes
#     we're done with the mc loop 11.378377
#     nyooo!!!!
#     we're done with the mc loop 11.799384
#     nyooo!!!!
#     we're done with the mc loop 14.520689
#     nyooo!!!!
#     we're done with the mc loop 12.265776
#     nyooo!!!!
#     we're done with the mc loop 11.224557
#     yes
#     we're done with the mc loop 10.087129
#     nyooo!!!!
#     we're done with the mc loop 9.012033
#     nyooo!!!!
#     we're done with the mc loop 12.642020
#     nyooo!!!!
#     we're done with the mc loop 14.182369
#     nyooo!!!!
#     we're done with the mc loop 14.651808
#     nyooo!!!!
#     we're done with the mc loop 13.487106
#     nyooo!!!!
#     we're done with the mc loop 13.476402
#     nyooo!!!!
#     we're done with the mc loop 15.143570
#     nyooo!!!!
#     we're done with the mc loop 12.006127
#     nyooo!!!!
#     we're done with the mc loop 12.884262
#     nyooo!!!!
#     we're done with the mc loop 15.002186
#     nyooo!!!!
#     we're done with the mc loop 13.108652
#     nyooo!!!!
#     we're done with the mc loop 13.708578
#     nyooo!!!!
#     we're done with the mc loop 10.417829
#     nyooo!!!!
#     we're done with the mc loop 12.804472
#     nyooo!!!!
#     we're done with the mc loop 15.753579
#     nyooo!!!!
#     we're done with the mc loop 13.454843
#     yes
#     we're done with the mc loop 12.248547
#     nyooo!!!!
#     we're done with the mc loop 14.340463
#     nyooo!!!!
#     we're done with the mc loop 14.163203
#     nyooo!!!!
#     we're done with the mc loop 13.363051
#     yes
#     we're done with the mc loop 11.563443
#     yes
#     we're done with the mc loop 7.928092
#     nyooo!!!!
#     we're done with the mc loop 8.044385
#     nyooo!!!!
#     we're done with the mc loop 13.859995
#     nyooo!!!!
#     we're done with the mc loop 9.948566
#     nyooo!!!!
#     we're done with the mc loop 9.782345
#     nyooo!!!!
#     we're done with the mc loop 9.692192
#     nyooo!!!!
#     we're done with the mc loop 10.680306
#     nyooo!!!!
#     we're done with the mc loop 8.435735
#     nyooo!!!!
#     we're done with the mc loop 8.466254
#     nyooo!!!!
#     we're done with the mc loop 7.894421
#     yes
#     we're done with the mc loop 9.600820
#     nyooo!!!!
#     we're done with the mc loop 7.794091
#     nyooo!!!!
#     we're done with the mc loop 9.570298
#     nyooo!!!!
#     we're done with the mc loop 7.532166
#     nyooo!!!!
#     we're done with the mc loop 8.847870
#     yes
#     we're done with the mc loop 9.903852
#     barely yes
#     we're done with the mc loop 9.190973
#     nyooo!!!!
#     we're done with the mc loop 9.198038
#     yes
#     we're done with the mc loop 8.602124
#     nyooo!!!!
#     we're done with the mc loop 7.594035
#     yes
#     we're done with the mc loop 9.248315
#     nyooo!!!!
#     we're done with the mc loop 7.032310
#     nyooo!!!!
#     we're done with the mc loop 6.971461
#     nyooo!!!!
#     we're done with the mc loop 7.887483
#     nyooo!!!!
#     we're done with the mc loop 7.867982
#     barely yes
#     we're done with the mc loop 7.013883
#     yes
#     we're done with the mc loop 6.974282
#     nyooo!!!!
#     we're done with the mc loop 6.936762
#     nyooo!!!!
#     we're done with the mc loop 6.923523
#     nyooo!!!!
#     we're done with the mc loop 8.544086
#     nyooo!!!!
#     we're done with the mc loop 7.474652
#     nyooo!!!!
#     we're done with the mc loop 7.134204
#     nyooo!!!!
#     we're done with the mc loop 9.808389
#     nyooo!!!!
#     we're done with the mc loop 10.796990
#     accepted_moves 449
# 

# In[8]:

plt.subplot(121)
anarray = np.asarray(radial_dist_before)
plt.hist(anarray,10);
plt.subplot(122)
anotherarray = np.asarray(radial_dist_after)
plt.hist(anotherarray,10);


# Out[8]:

# image file:

# In[9]:

plt.plot(global_energy)


# Out[9]:

#     [<matplotlib.lines.Line2D at 0xaffa160c>]

# image file:

# In[ ]:



