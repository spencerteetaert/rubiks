'''
Example test file. When you add new features, write a test file here to ensure
that other people don't accidentally break it. Each feature should have its
own test file for traceability purposes. 
'''
file_name = "example_test"

def run():
    # Test code goes here 
    # return boolean (true if passed, false if not) and error message if applicable 
    return True, ""

if __name__=="__tests__."+file_name:
    print("Testing {}.py...".format(file_name))
    ret, msg = run()
    if ret:
        print("{}.py successful.\n".format(file_name))
    else:
        print("ERR: {}.py failed.\n{}".format(file_name, msg))