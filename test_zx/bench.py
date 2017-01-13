import time

#-----------------------------------------------------------------------------------------

time.clock()

def bench(title, ofunc, nfunc, args, n=2000):
    print("%s - %d veces" % (title, n))
    print("-------------------------------------------------")
    print ("Old = %f" % ofunc(*args))
    print ("New = %f" % nfunc(*args))

    t1 = time.clock()
    
    for i in range(n):
        ofunc(*args)
    
    t2 = time.clock()
    
    for i in range(n):
        nfunc(*args)
    
    t3 = time.clock()

    print ("Time Old = %8.0f ns/op" % (10**9*(t2 - t1)/n))
    print ("Time New = %8.0f ns/op" % (10**9*(t3 - t2)/n))
    print ("Old/New  = %8.2f veces" % ((t2-t1)/(t3 - t2)))

