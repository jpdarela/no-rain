
import numpy as np
import os 

nx = 720      # numero de colunas em cada imagem
ny = 360      #  /////////linhas em cada imagem 

## FUNÇÔES QUE VAO FAZER A PARADA TODA:
def list_files(cwd = os.getcwd()):
    files = []
    for dirpath, b, filenames in os.walk(cwd):
        for filename in filenames:
            files.append(os.path.join(dirpath,filename))
    return (files, filenames)


def catch_nt(input_file):
    file_size = os.path.getsize(input_file)
    num_lay = file_size/1024/1012.5
    nt = int(num_lay)
    return nt


def catch_data(input_file, data_len):
    return np.fromfile(input_file, count=nx*ny*data_len, dtype=np.float32).reshape((data_len,nx,ny))


def save_ascii_grid(arr, outfilepath):
    """ save an array as an ascii-grid file"""
    
    if type(arr) == type(np.zeros(2)) and len(arr.shape) == 2:
        
        if arr.shape[0] < arr.shape[1]:
            nrows, ncols = arr.shape
        else:
            ncols, nrows = arr.shape
        
        cellsize = 360/ncols
        NO_DATA = arr[0][0]
        
        header = ['ncols %d\r\n'%ncols, 'nrows %d\r\n'%nrows,
                  'xllcorner -180\r\n', 'yllcorner -90\r\n', 
                  'cellsize %f\r\n'%cellsize, 'NODATA_value %f\r\n'%NO_DATA]
    
    else: print('arr não é array')

    # save arr as txt.delimited file
    try:
        #save
        txt_file = 'np_array_calc_avg_py.txt'
        np.savetxt(txt_file, arr, fmt='%.10f')
        # catch np.array data in txt format
        with open(txt_file, newline='\r\n') as fh:
            reader = fh.readlines()
        # erase aux_file
        os.remove(txt_file)
        
    except:
        print('f1')
    
#    # write asc file:
    try:
        with open(outfilepath, mode='w') as fh:
            fh.writelines(header)
        
        with open(outfilepath, mode='a') as fh:
            for line in reader:
                fh.write(line)    
    except:
        print('f2')


def write_header(file_conn, input_data, xllcorner=-180, yllcorner=-90, 
                 byteOrder='LSBFIRST'):        
     """ Cria um cabeçalho.hdr nos padrões dos arquivos.flt """            
     noDataValue = input_data[0][0] 
     xdim, ydim = input_data.shape
     cellsize = 360/xdim
     write = ['NCOLS %d\r\n'%xdim,
              'NROWS %d\r\n'%ydim,
              'XLLCORNER %d\r\n'%xllcorner,
              'YLLCORNER %d\r\n'%yllcorner,
              'CELLSIZE %f\r\n'%cellsize,
              'NODATA_VALUE %f\r\n'%noDataValue,
              'BYTEORDER %s\r\n'%byteOrder
              ]
     with open(file_conn, 'w') as fh:
         for line in write:
             fh.write(line)


def write_flt(data_array, layers, filename):
    """inputs: data_array = np.array(shape=(nx,ny,nt))
               layers = numero de meses ou camadas ou blablabla
       output(side_effect): arquivo de imagem.flt com imagem.hdr + imagem.asc
    """
    # read fortran source code flip_image.f90
    with open('flip_image.f90', 'r') as fh:
        to_compile = fh.readlines()
    
    # create a folder to save data
    folder = filename.split('.')[0] 
    os.mkdir(folder)
    curdir = os.getcwd()
    # change cwd
    os.chdir(os.getcwd() + '/' + folder)
    
    # writing flip_image
    with open('flip_image.f90', 'w') as fh:
        fh.writelines(to_compile)
    
    # compiling flip_image    
    os.system('gfortran flip_image.f90 -o flip_image.exe')   
    
    # para cada uma das camadas do arquivo binario
    for image in range(layers):
        # nomes bonitos para os arquivos (.flt, .hdr)        
        outfile_name = filename.split('.')[0] + '_LAYER' +  str(image+1) + '.flt'
        outfile_hd =  outfile_name.split('.')[0] + '.hdr'
        print(outfile_name)
        # Salve a parte binaria (.flt)
        with open(outfile_name, 'wb') as fh:
            data_array[image].tofile(fh, sep='', format = "%.10f")
        
        # flip na imagem + header
        if filename == 'COW2006.BIN':
            write_header(outfile_hd,data_array[image])
        else:
            os.system('./flip_image.exe %s'%outfile_name)
            write_header(outfile_hd,data_array[image])
                   
        # salve em formato ascii grid : bom pra arquivar os seus dados!
        dt1 = np.fromfile(outfile_name, count=nx*ny, dtype=np.float32).reshape((nx,ny))
        save_ascii_grid(dt1,outfile_name.split('.')[0] + '.asc' )
    
    # finaliza
    while True:
        try:
            os.remove('flip_image.exe')
            break
        except:
            pass
           
    os.remove('flip_image.f90')
    os.chdir(curdir)


def main():
    for el in [file for file in list_files()[1] if (str('.bin')in file or str('.BIN') in file)]:
        nt = catch_nt(el)
        dt = catch_data(el, nt)
        print(el, '\n')
        write_flt(dt,nt,el)


# executa
if __name__ == '__main__':
    main()    