import os,sys,re
from lab0 import my_getLine

def execute(args):
    if len(args) == 0:
        return

    elif args[0].lower() == "exit":
        sys.exit(0)

    elif args[0] == "cd":
        try:
            if len(args) == 1:
                os.chdir("..")
            else:
                os.chdir(args[1])
        except:
            os.write(1, ("cd %s: No such file or directory" % args[1]).encode())
            pass

        if rc<0:
            os.write(2, ("fork failed, returnind %d\n" % rc).encode())
            sys.exit(1)
        elif rc == 0:
            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execve(program, args, os.environ)
                except FileNotFoundError:
                    pass
            os.write(2, ("command not found \n").encode())
            sys.exit(0)

            childpid = os.wait()

while True:
    if 'PS1' in os.environ:
        os.write(1, (os.environ['PS1']).encode())
    else:
        os.write(1, ("$ ").encode())

    args = lab0.my_getLine().split()
    if len(args)==0:
        break
    execute(args)
        
