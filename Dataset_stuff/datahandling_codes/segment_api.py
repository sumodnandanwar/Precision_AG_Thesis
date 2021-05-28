from segments import SegmentsClient, SegmentsDataset,utils
import urllib.request
from urllib.parse import urlparse
import json
import os


# Load json file
with open('/home/nordluft_xaviernx/Desktop/Precision_Project/Dataset_stuff/release2.json','r') as f:
   data = json.load(f)

# Folder to download
img_fold = '/home/nordluft_xaviernx/Desktop/Precision_Project/Dataset_stuff/trial_img/'
# Create a folder label in img folder
sample = data['dataset']['samples']
labelset = 'ground-truth'

def label_from_url(sample,labelset,counter):
    sample_name = os.path.splitext(sample['name'])[0]
    label = sample['labels'][labelset]
    if label is not None:
        segmentation_bitmap_url = label['attributes']['segmentation_bitmap']['url']
        url_extension = os.path.splitext(urlparse(segmentation_bitmap_url).path)[1]
        segmentation_bitmap_filename = os.path.join(img_fold+"label", '{}{}'.format(counter, url_extension))
        
        if not os.path.exists(segmentation_bitmap_filename):
            utils.download_and_save_image(segmentation_bitmap_url, segmentation_bitmap_filename)
    else:
        pass
    ####### Uncomment below block to download image data as well########
    # image_url = sample['attributes']['image']['url']
    # url_extension_img = os.path.splitext(urlparse(image_url).path)[1]
    # image_filename_rel = '{}{}'.format(counter, url_extension_img)
    # image_filename = os.path.join(img_fold, image_filename_rel)

    # if not os.path.exists(image_filename):
    #     utils.download_and_save_image(image_url, image_filename)
    
counter = 0
for sample in data['dataset']['samples']:
    label_from_url(sample,labelset,counter)
    counter += 1

print("Download Complete!!!")

# print(data)
# api_key = "730278c0560924f04fce15629ee27dee79f00801"
# client = SegmentsClient(api_key)

# List datasets
# user = "sumodkth"
# datasets_on_web = client.get_datasets(user)

# For checking the list of dataset on the web 
# for dataset in datasets:
#     print(dataset["name"], dataset["description"])

# Get a dataset
# dataset_identifier = "sumodkth/Lateblight_leaf"
# dataset_down = client.get_releases(dataset_identifier)
# print(dataset_down)
