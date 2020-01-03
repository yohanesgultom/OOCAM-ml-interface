import os, stat

def rmtree(dir):
    for root, dirs, files in os.walk(dir, topdown = False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(dir)
