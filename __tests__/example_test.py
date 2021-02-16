'''
Example test file. When you add new features, write a test file here to ensure
that other people don't accidentally break it. Each feature should have its
own test file for traceability purposes. 
'''
file_name = "example_test"

def run():
    # Test code goes here 
    return True

if __name__=="__tests__."+file_name:
    print("Testing {}.py...".format(file_name))
    if run():
        print("{}.py successful.".format(file_name))
    else:
        print("ERR: {}.py failed.".format(file_name))


        # this is a change in example 