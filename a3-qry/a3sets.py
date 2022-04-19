#!/usr/bin/python3

import sys
import time



logdata = []

def timeit(method):
  """
  timer class to record execution times of inner methods.

  Ref: https://www.geeksforgeeks.org/timing-functions-with-decorators-python/
  """
  def timed(*args, **kw):
      ts = time.time()
      result = method(*args, **kw)
      te = time.time()        
      # storing runtime info in logdata in milliseconds
      logdata.append(format(((te - ts) * 1000), '.2f'))
      return result    
  
  return timed



# A: Sets and relations

def succ_map(e):
  """
  create adjacency list representation of e
  assuming graph is bidirectional
  (a,b): both should have each other in their list
  """
  S = {}
  for (a, b) in e:
      if (a in S):
          S[a].add(b)
      else:
          S[a] = {b}
      if (b in S):
          S[b].add(a)
      else:
          S[b] = {a}
  return S


def image_union(e, r):
  """
  algo from slide #46
  """
  res = set()
  for x in r:
    for y in e[x]:
      res.add(y)
  return res


@timeit
def reach_iter(e,s):
  """
  add all nodes reachable from s to r, including s itself
  algo from slide #46
  """
  r = s.copy()       # create a shallow copy of s for local changes
  s_map = succ_map(e)
  val = (image_union(s_map, r) - r)
  while val:
    y = next(iter(val))
    r.add(y)
    val = (image_union(s_map, r) - r)
  return r


@timeit
def reach_inc_chain(e,s):
  """
  s : succ_map, provides adj_list e[x] = {y}
  """
  (w,r,t) = (set(), set(), set())
  for x in s:
    for y in e[x]:
      if y not in t:
        if y not in r:
          w.add(y)
        t.add(y)
    if x in t:
      w.remove(x)
    r.add(x)
  
  while w:
    x = next(iter(w))       # keep iterating over w
    for y in e[x]:
      if y not in t:
        if y not in r:
          w.add(y)
        t.add(y)
    if x in t:
      w.remove(x)
    r.add(x)
  return r

@timeit
def reach_inc_direct(e,s):
  """
  takes e (in successor map representation) and s as arguments, and returns r 
  """
  w = s.copy()      # shallow copy for handling local changes
  r = set()
  while w:
    x = next(iter(w))
    for y in e[x]:
      if ((y not in r) and (y not in w)):
        w.add(y)
    w.remove(x)
    r.add(x)
  return r


def reach_read():
  filename = sys.argv[1] if len(sys.argv) > 1 else "reach.in.1000"
  with open(filename) as infile: 
    data= infile.read().replace('}\n{','},{').replace('[','(').replace(']',')')
  e,s = eval(data)
  logdata.append(filename)
  return e,s

def reach_test():
  e,s = reach_read()
  vertices = {x for (x,_) in e} | {y for (_,y) in e}
  print(len(e), len(s), len(vertices))

  rs = reach_iter(e,s)
  print(len(rs))

  e2 = succ_map(e)
  print(len(e2))

  rs2 = reach_inc_chain(e2,s)
  # print(rs2)
  print(rs2 == rs)

  rs3 = reach_inc_direct(e2,s)
  # print(rs3)
  print(rs3 == rs)

  # print(e2, rs, rs2, rs3)
  
  with open("A3_runtime_log.csv", "a") as logfile:
    logfile.write(f'\n{",".join(map(str, logdata))}')


reach_test()
