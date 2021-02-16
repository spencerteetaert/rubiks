'''
Allows for importing of entire diectory. No need to touch
'''
import os 
files = os.listdir("__tests__")[:-2]
for i in range(0, len(files)):
    files[i] = files[i][:-3]
__all__ = files