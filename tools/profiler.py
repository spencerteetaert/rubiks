'''
    Runs a profiler on the main file to identify slow functions and runtime. 
'''

import cProfile
pr = cProfile.Profile()

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

pr.enable()
import pro
pr.disable()

pr.print_stats(sort='time')
input("Press Enter to exit...")