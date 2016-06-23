import os 
filename_exe = 'harv_hadcm3_biomas.exe'

#filename_comp = 'harv_allcfts_2035_2065_amazon.f'
#filename_comp = 'harv_allcfts_91_00_brazil_biomas_v2.f'
#filename_comp = 'harv_allcfts_91_00_brazil_biomas_v3.f'

filename_comp = 'harv_allcfts_2035_2065_amazon_biomas.f'
os.system('gfortran %s -o %s'%(filename_comp,filename_exe))