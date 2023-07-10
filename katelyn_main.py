import numpy as np
import astroquery
from astroquery import simbad
from astroquery.simbad import Simbad
import astropy.units as u
import astropy.coordinates as coord
import numpy.ma as ma
import matplotlib.pyplot as plt

def star_mapper_3D(star_name, radius):
    Simbad.add_votable_fields('plx', 'distance')
    star_result=Simbad.query_object(star_name)
    RA=star_result["RA"].value
    DEC=star_result["DEC"].value
    parallax=star_result["PLX_VALUE"].value

    distance=1/(parallax/1000)*u.pc
    side_length_cube_pc=1/radius*u.pc
    side_length_cube_arcsec=(1/distance.value)*1000
    print(parallax, side_length_cube_arcsec)
    
    region= Simbad.query_region(coord.SkyCoord(RA, DEC,
                                   unit=(u.hourangle, u.deg), frame='galactic'),
                                   radius=radius*u.deg)
    
    defined_region=[]

    for test_obj in region:
        parallax_test_obj=test_obj["PLX_VALUE"]
        
        # if parallax_test_obj==int(parallax_test_obj):
        #     print(parallax_test_obj)
        
        if ma.is_masked(parallax_test_obj):
            print("m")
        else:
            if parallax_test_obj>parallax-side_length_cube_arcsec and parallax_test_obj<parallax+side_length_cube_arcsec:
                defined_region.append(test_obj)
    
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(projection='3d')

    for final_obj in defined_region:
        RA=final_obj["RA"]
        DEC=final_obj["DEC"]
        c=coord.SkyCoord(RA, DEC, unit=(u.hourangle, u.deg))
        RA=c.ra.value
        DEC=c.dec.value

        parallax=final_obj["PLX_VALUE"]
        distance=distance=1/(parallax/1000) #parsecs
        print(distance)

        ax.scatter(RA, DEC, distance)
    
    plt.show()

star_mapper_3D("LKCA 15", 0.5)