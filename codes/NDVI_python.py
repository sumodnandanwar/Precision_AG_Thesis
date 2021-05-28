
#Libraries used in geo sensing
import os
import matplotlib.pyplot as plt
import numpy as np
#Rioxarray is used in clip, merge, and reproject rasters
import rioxarray as rxr
# import geopandas as gpd
#Eathpy is used in precision AG applications
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep

def NDVI_index(NIR, bR):
    if not (NIR.shape == bR.shape):
        raise ValueError("Both arrays should have the same dimensions")

    # Ignore warning for division by zero
    with np.errstate(divide="ignore"):
        n_diff = (NIR - bR) / (NIR + bR)

    # Set inf values to nan and provide custom warning
    if np.isinf(n_diff).any():
        warnings.warn(
            "Divide by zero produced infinity values that will be replaced "
            "with nan values",
            Warning,
        )
        n_diff[np.isinf(n_diff)] = np.nan

    # Mask invalid values
    if np.isnan(n_diff).any():
        n_diff = np.ma.masked_invalid(n_diff)

    return n_diff

def VARI_index(bR,bG,bB,index):
    if not (bR.shape == bG.shape == bB.shape):
        raise ValueError("Both arrays should have the same dimensions")

    # Ignore warning for division by zero
    with np.errstate(divide="ignore"):
        if index == 'VARI':
            vari = (bG - bR) / (bG + bR - bB)
        elif index == 'RGBVI':
            vari = (bG*bG)-(bR*bB) / (bG*bG)+(bR + bB)
        elif index == 'NGRDI':
            vari = (bG - bR) / (bG + bR)

    # Set inf values to nan and provide custom warning
    if np.isinf(vari).any():
        warnings.warn(
            "Divide by zero produced infinity values that will be replaced "
            "with nan values",
            Warning,
        )
        vari[np.isinf(vari)] = np.nan

    # Mask invalid values
    if np.isnan(vari).any():
        vari = np.ma.masked_invalid(vari)

    return vari

#Earth py is a really good python library for remote sensing
def tif_2index(file,output,vindex):
    naip_data = rxr.open_rasterio(file)

    # View shape of the data
    print(naip_data.shape)
    
    if naip_data.[3] is not None:
        NIR = naip_data[3]
    else:
        pass

    R = naip_data[0]
    G = naip_data[1]
    B = naip_data[2]



    if vindex == 'NDVI':
        naip_ndvi = NDVI_index(NIR, R)
    elif vindex == 'VARI' or 'RGBVI' or 'NGRDI':
        naip_ndvi = VARI_index(R,G,B,vindex)

    #Plot bands
    ep.plot_bands(naip_ndvi,
                cmap='PiYG',
                scale=False,
                vmin=-1, vmax=1,
                title=" Vegetation Index plot")
    plt.show()
    #Plot histogram
    # ep.hist(naip_ndvi.values,
    #         figsize=(12, 6),
    #         title=["NDVI: Distribution of pixels\n NAIP 2015 Cold Springs fire site"])

    # plt.show()

    type(naip_ndvi), naip_ndvi.dtype

    # Write your the ndvi raster object
    naip_ndvi.rio.to_raster(output)

img_path = '/home/nordluft_xaviernx/Desktop/Precision_Project/Potato_trained_model/_DSC9666.JPG'
output = '/home/nordluft_xaviernx/Desktop/Precision_Project/Potato_trained_model/_DSC9666.tif'
tif_2index(img_path,output, 'VARI')

### Zonation map based on index values

# # Classifying vegetation zones based on NDVI values
# # Define color map
# nbr_colors = ["gray", "y", "yellowgreen", "g", "darkgreen"]
# nbr_cmap = ListedColormap(nbr_colors)

# # Define class names
# ndvi_cat_names = [
#     "No Vegetation",
#     "Bare Area",
#     "Low Vegetation",
#     "Moderate Vegetation",
#     "High Vegetation",
# ]

# # Get list of classes
# classes = np.unique(ndvi_landsat_class)
# classes = classes.tolist()
# # The mask returns a value of none in the classes. remove that
# classes = classes[0:5]

# # Plot your data
# fig, ax = plt.subplots(figsize=(12, 12))
# im = ax.imshow(ndvi_landsat_class, cmap=nbr_cmap)

# ep.draw_legend(im_ax=im, classes=classes, titles=ndvi_cat_names)
# ax.set_title(
#     "Landsat 8 - Normalized Difference Vegetation Index (NDVI) Classes",
#     fontsize=14,
# )
# ax.set_axis_off()

# # Auto adjust subplot to fit figure size
# plt.tight_layout()