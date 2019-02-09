from __future__ import print_function
from myo.utils import TimeInterval
import myo
import sklearn.ensemble
from sklearn import metrics
import sys
from time import sleep
import numpy as np
import threading
import collections
import math
from threading import Lock, Thread


def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]

def rms(array):
    n = len(array)
    sum = 0
    for a in array:
        sum =+ a*a
    return np.sqrt((1/float(n))*sum)

def iav(array):
    sum = 0
    for a in array:
        sum += np.abs(a)
    return sum

def ssi(array):
    sum = 0
    for a in array:
        sum += a*a
    return sum

def var(array):
    n = len(array)
    sum = 0
    for a in array:
        sum += a*a
    return ((1/float(n-1))*sum)

def tm3(array):
    n = len(array)
    print('n : ', n)
    sum = 0
    for a in array:
        sum =+ a*a*a
    return np.power((1/float(n))*sum,1/float(3))

def wl(array):
    sum = 0
    for a in range(0,len(array)-1):
        sum =+ array[a+1] - array[a]
    return sum

def aac(array):
    n = len(array)
    sum = 0
    for a in range(0,n-1):
        sum =+ array[0+1] - array[0]
    return sum/float(n)


def featurize(array):
    n = []
    for a in array:
        n.append(rms(a))
    return n

status = 0

X = []

def toEuler(quat):
    quat = quat[0]

    # Roll
    sin = 2.0 * (quat.w * quat.w + quat.y * quat.z)
    cos = +1.0 - 2.0 * (quat.x * quat.x + quat.y * quat.y)
    roll = math.atan2(sin, cos)

    # Pitch
    pitch = math.asin(2 * (quat.w * quat.y - quat.z * quat.x))

    # Yaw
    sin = 2.0 * (quat.w * quat.z + quat.x * quat.y)
    cos = +1.0 - 2.0 * (quat.y * quat.y + quat.z * quat.z)
    yaw = math.atan2(sin, cos)
    return [pitch, roll, yaw]



   
class Listener(myo.DeviceListener):

  def __init__(self):
    self.interval = TimeInterval(None, 0.1)
    self.orientation = None
    self.emg_enabled = False
    self.emg = None
    self.lock = Lock()
    self.emg_data_queue = collections.deque(maxlen=1)
    self.ori_data_queue = collections.deque(maxlen=1)

  global X
  def output(self):
    if not self.interval.check_and_reset():
      return

    parts = []
    if self.orientation:
      for comp in self.orientation:
        parts.append(comp)
      parts.append(self.emg)

      X.append(parts)
      #print(parts) 
       #parts is the orientation data   

    sys.stdout.flush()

  def on_connected(self, event):
    event.device.stream_emg(True)

  def on_orientation(self, event):
    self.orientation = event.orientation
    self.output()

  def on_emg_data(self, event):
    print(str(event.emg))
    self.output()

  def on_emg(self, event):
    self.emg = event.emg
    self.output()



if __name__ == '__main__':
  myo.init(sdk_path='./myo-sdk-win-0.9.0/')
  hub = myo.Hub()
  listener = Listener()
  status = 9999

  sleep(1)

  myX = []

  req_iter = 20
  train_1 = []
  train_2 = []
  train_3 = []
  train_4 = []
  train_5 = []

  ges1 = ['Rock', 'Paper', 'Scissors', 'Lizard', 'Spock']
  ges2 = ['Number 1', 'Number 2', 'Number 3', 'Number 4', 'Number 5']
  ges3 = ['Spread Fingers', 'Wave Out', 'Wave In', 'Fist', 'Rest']

  ges = ges3


  while hub.run(listener.on_event, 500):
    print(X)
    pass
