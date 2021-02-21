import os,sys,re
from lab0 import my_getLine

def execute(args):
    if len(args) == 0:
        return

    if args[0].lower() == "exit":
        sys.exit(1)

    if args[0] == "cd":
        if len(args) == 1:
            os.chdir("..")
        else:
            os.chdir(args[1])

    rc = os.fork()

    if rc<0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:
        for dir in re.split(":", os.environ['PATH']):
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ)
            except FileNotFoundError:
                pass
        
        os.write(2, ("command not found \n").encode())
        sys.exit(1)
    else:
        childpid = os.wait()
            
#os.environ.pop("PS1")
while (1):
    if 'PS1' in os.environ:
        os.write(1,(os.environ['PS1']).encode())
    else:
        os.write(1,"$ ".encode())

    input = my_getLine()
    args = input.split()
    
    execute(args)
