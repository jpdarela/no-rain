import os 

files =  [file_ for file_ in os.listdir() if '.exe' in file_]
for el in files:
    print(el)
    os.system('./%s'%el)
os.system('rm *txt')