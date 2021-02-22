import os,sys,re
from lab0 import my_getLine

def execute(args):
    if len(args) == 0:
        return

    elif args[0].lower() == "exit":
        sys.exit(1)

    elif args[0] == "cd":
        try:
            if len(args) == 1:#go one directory back
                os.chdir("..")
            else:#go to directory provided
                os.chdir(args[1])
        except:
            pass
            
    elif "|" in args:#pipe
        pipe(args)

    else:
        rc = os.fork()
        background = True
        #background
        if "&" in args:
            args.remove("&")
            background = False

        if rc<0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)
        elif rc == 0:
            if "/" in args[0]:
                program = args[0]
                try:
                    os.execve(program, args, os.environ)
                except FileNotFoundError:
                    pass
            elif ">" in args or "<" in args:
                redirection(args)
            else:
                for dir in re.split(":", os.environ['PATH']):#try directories in path
                    program = "%s/%s" % (dir, args[0])
                    try:
                        os.execve(program, args, os.environ)
                    except FileNotFoundError:
                        pass
        
            os.write(2, ("command not found\n").encode())
            sys.exit(1)
        else:
            if background:
                childpid = os.wait()

def commands(args):
    if "/" in args[0]:
        program = args[0]
        try:
            os.execve(program, args, os.environ)
        except FileNotFoundError:
            pass
    elif ">" in args or "<" in args:
        redirection(args)
    else:
        for dir in re.split(":",os.environ['PATH']):
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ)
            except FileNotFoundError:
                pass
    os.write(2, ("%s: command not found\n" % args[0]).encode())
    sys.exit(1)

def pipe(args):
    left = args[0:args.index("|")]
    right = args[args.index("|") + 1:]
    pRead, pWrite = os.pipe()
    rc = os.fork()
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:
        os.close(1)
        os.dup(pWrite)
        os.set_inheritable(1, True)
        for fd in (pRead, pWrite):
            os.close(fd)
        commands(left)
        os.write(2, ("Could not exec %s\n" % left[0]).encode())
        sys.exit(1)
    else:
        os.close(0)
        os.dup(pRead)
        os.set_inheritable(0, True)
        for fd in (pWrite, pRead):
            os.close(fd)
        if "|" in right:
            pipe(right)
        commands(right)
        os.write(2, ("Could not exec %s\n" % right[0]).encode())
        sys.exit(1)

def redirection(args):
    #output
    if '>' in args:
        os.close(1)
        os.open(args[args.index('>')+1], os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(1,True)
        args.remove(args[args.index('>')+1])
        args.remove('>')
    #input
    else:
        os.close(0)
        os.open(args[args.index('<')+1], os.O_RDONLY)
        os.set_inheritable(0, True)
        args.remove(args[args.index('<') + 1])
        args.remove('<')

    for dir in re.split(":", os.environ['PATH']):
        prog = "%s/%s" % (dir,args[0])
        try:
            os.execve(prog, args, os.environ)
        except FileNotFoundError:
            pass
    os.write(2, ("%s: command not found\n" %args[0]).encode())
    sys.exit(1)


#os.environ.pop("PS1")
while (1):
    if 'PS1' in os.environ:
        os.write(1,(os.environ['PS1']).encode())
    else:
        os.write(1,("$ ").encode())

    input = my_getLine()
    args = input.split()
    for arg in args:
        execute(args)
