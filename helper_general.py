rock = 0
paper = 1
scissors = 2

def TicToc():
  from time import perf_counter as pc 
  timer = {}

  def tic(activity = "Process"):
    timer[activity] = pc()
    print(f"{activity:.20} has begun;", end = " ")
  def toc(activity = "Process"):
    end_time = pc()
    start_time = timer.get(activity, None)

    if start_time:
      time = end_time - start_time
      print(f"{activity:.20} took {time//60:3.0f} mins {time%60:5.2f} secs")
      timer[activity] = None
      return 
    else:
      print("You didnt start the clock")
      return
  return tic, toc

tic, toc = TicToc()

import pickle

def toPickle(pickle_name, pickle_obj):     
    # Its important to use binary mode 
    dbfile = open(pickle_name, 'rb') 
    # source, destination 
    pickle.dump(pickle_obj, dbfile)                      
    dbfile.close() 
  
def readPickle(pickle_name): 
    # for reading also binary mode is important 
    dbfile = open(pickle_name, 'rb')      
    db = pickle.load(dbfile) 
    dbfile.close() 
    return db