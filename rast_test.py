import os
import sys
import StringIO
import time
import PIL

import numpy as np

lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import ecosynth.acquire as acq
import ecosynth.postprocess as pp
from ecosynth.postprocess import CloudRasterizer

def rast_test(testfiles):
    start = time.time()


    msl_float = 50.6

    
    out_filepath = os.path.join(testfiles, 'other/vellozia_rgb_t2.out')
    out_file = open(out_filepath, mode='r')
    out_tuple = pp.io.load_out(out_file)        
 
  
    print "cam_array_fixed shape", out_tuple.cam_array_fixed.shape
    print "cam_array shape", out_tuple.cam_array.shape

    log_filepath = os.path.join(testfiles, 'test_set_serc/serc511.log.txt')
    log_file = open(log_filepath, mode='r')

    gps_array = acq.utilities.telemetry_to_gps_positions(
        log_file, msl_float)

    logger_file = open('debug.txt', 'w')
    logger_file.write("Debugging File\n")

    xyzrgb_array_georef, parameters = pp.transforms.georef_telemetry(
        out_tuple, gps_array, logger=logger_file)
            
            
            
    c = pp.CloudRasterizer.CloudRasterizer(
        xyzrgb_array_georef, resolution=1.0)

    c.filter_noise_z()
    
    png_file0 = open('img_vellozia0.png', 'w') 
    
    
    max_height_raster = c.get_max_height_raster()
    c.plot_raster_heatmap(max_height_raster, title= "Max Height Raster",png_file=png_file0)  
  
  
    png_file1 = open('img_vellozia1.png', 'w')  
    
    
    color_raster = c.get_color_raster()
        
    c.plot_raster_colors(color_raster, title="Color Raster", png_file=png_file1)
    image_filepath = os.path.join(os.getcwd(), 'img_vellozia10.png')
    aoi = c.get_aoi()
    pp.io.save_image(image_filepath, color_raster,aoi)
    
    raster = c.get_cloud_array()
    c.plot_meshgrid(raster)
    
    png_file2 = open('img_vellozia2.png', 'w')

    hr_raster = c.get_height_range_raster()
    c.plot_raster_heatmap(hr_raster, title="Height range raster",png_file=png_file2)
             
    png_file3 = open('img_vellozia3.png', 'w')

    q95_raster = c.get_Q95_elevation_raster()
    c.plot_raster_heatmap(q95_raster, title="Q95 Raster",png_file=png_file3)
    
    png_file4 = open('img_vellozia4.png', 'w')

    std_raster = c.get_std_raster()
    c.plot_raster_heatmap(std_raster, title="Standard Deviation Raster",png_file=png_file4)

    png_file5 = open('img_vellozia5.png', 'w')

    point_density_raster = c.get_point_density_raster()
    c.plot_raster_heatmap(point_density_raster, title="Point Density Raster",png_file=png_file5)
   
    png_file6 = open('img_vellozia6.png', 'w')

    median_height_raster = c.get_median_height_raster()
    c.plot_raster_heatmap(median_height_raster, title="Median Height Raster",png_file=png_file6)
    print median_height_raster.shape 
 
    png_file7 = open('img_vellozia7.png', 'w') 
 
    mean_height_raster = c.get_mean_height_raster()
    c.plot_raster_heatmap(mean_height_raster, title="Mean Height Raster",png_file=png_file7)

    png_file8 = open('img_vellozia8.png', 'w')
   
    max_elevation_raster = c.get_max_elevation_raster()
    c.plot_raster_heatmap(max_elevation_raster, title="Max Height Raster",png_file=png_file8)

    png_file9 = open('img_vellozia9.png', 'w')

    cv_height_raster = c.get_cv_height_raster()
    c.plot_raster_heatmap(cv_height_raster, title="CV Height Raster",png_file=png_file9)


    print c.get_shape() 
    

    out_file.close()
    log_file.close()
    logger_file.close()

   


def main():
    testfiles = os.path.join(os.getcwd(), 'files/')
    rast_test(testfiles)


if __name__ == "__main__":
    main()
