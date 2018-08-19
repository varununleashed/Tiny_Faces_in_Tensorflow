import cv2
import numpy as np
import random
def box_size_calculate(r):
  """ Calculates 1D size of bounding box
      Args:
        r:
          A list containing the 2 co-ordinates of image [(x1, y1), (x2, y2)]
      Returns:
      	length and width of box
  """
  length = r[2] - r[0]
  width = r[3] - r[1]
  return length, width

def Average(lst): #To calculate Average of the list
  if len(lst) is not 0:
    return int(sum(lst) / len(lst))
  else:
    #print("No Faces for Average!") #Case for length of list found to be zero
    return 1


def crop_faces_save(img_xsize, face_list, main_img_name):
  main_directory = '/content/thumbs/'
  img_xsize = cv2.cvtColor(img_xsize, cv2.COLOR_BGR2RGB)
  num_faces_taken = 0
  for i in enumerate(face_list):
    x1x2 = i[1][0][3] - i[1][0][1]
    y1y2 = i[1][0][2] - i[1][0][0]
    #print("x1x2 y1y2 is: ", x1x2, y1y2)
    if (i[1][0][1] < 0) or (i[1][0][3] < 0) or (i[1][0][0] < 0) or (i[1][0][2] < 0):
      continue
    if (x1x2 < 40) or (y1y2 < 40):
      #print("Not taking small face found at: ", i[1][0][1], i[1][0][3], i[1][0][0], i[1][0][2])
      continue
    if (x1x2 > 300) or (y1y2 > 300):
     # print("Not taking small face found at: ", i[1][0][1], i[1][0][3], i[1][0][0], i[1][0][2])
      continue
    oneFace = img_xsize[i[1][0][1]:i[1][0][3], i[1][0][0]:i[1][0][2]]
    num_faces_taken = num_faces_taken + 1
    resize_save_f(oneFace, main_img_name, main_directory, i[0])
  #print("Number faces returned: ", num_faces_taken)
  return num_faces_taken

def resize_save_f(face_numpy, main_img_name, main_directory, n):
  #print("resize_save_f gives face_shape: ", face_numpy.shape[:2])
  n_resolution = new_resolution(face_numpy.shape[:2])
  res = cv2.resize(face_numpy, dsize=n_resolution, interpolation=cv2.INTER_CUBIC)
  height = np.size(res, 0)
  width = np.size(res, 1)
  if not (width < 40 or height < 40 or width > 300 or height > 300):
    res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
    cv2.imwrite(main_directory + main_img_name + "face" + str(n + 1) + ".jpg", res)

def crop_nonfaces_save(img_xsize, face_list, Lavg, Wavg, main_img_name, num_faces_taken):
  if num_faces_taken == 0:
    return
  n = 0
  limit = 0
  total_faces = len(face_list)
  img_xsize = cv2.cvtColor(img_xsize, cv2.COLOR_BGR2RGB)
  main_directory = '/content/nthumbs/'
  size = img_xsize.shape
  #print("Original Size of image: ", size)
  legit_size = (size[0] - Wavg, size[1] - Lavg)
  #print("Legit size of image: ", legit_size[0], legit_size[1])
  #print("Lavg, Wavg: ", Lavg, Wavg)
  while n < num_faces_taken:
    # if n >= num_faces_taken:
    #   break
    x1 = random.randint(0, legit_size[1])
    y1 = random.randint(0, legit_size[0])
    x2 = x1 + Lavg
    y2 = y1 + Wavg

    box = (x1, y1, x2, y2)
    #print("Box calculated: ", box)
    #print("Face list gives: ", face_list)
    if does_it_overlap(face_list, box):
      if limit > 1000:
        break
      limit = limit + 1
      continue
    else:
      n = n + 1
      print()
      oneFace = img_xsize[y1:y2, x1:x2]
      if oneFace.shape[0] == 0:
        #print("oneFace.shape[0] was 0")
        n = n - 1
        continue
      if oneFace.shape[1] == 0:
        #print("oneFace.shape[1] was 0")
        n = n - 1
        continue
      height = np.size(oneFace, 0)
      width = np.size(oneFace, 1)
      #print("height, width of non-face box: ", height, width)
      if width < (int(0.95*height)) and height < (int(3*width)):
        resize_save_nf(oneFace, main_img_name, main_directory, n)
      else:
        continue
      
def resize_save_nf(face_numpy, main_img_name, main_directory, n):
  n_resolution = new_resolution(face_numpy.shape[:2])
  res = cv2.resize(face_numpy, dsize=n_resolution, interpolation=cv2.INTER_CUBIC)
  height = np.size(res, 0)
  width = np.size(res, 1)
  if not (width < 40 or height < 40 or width > 300 or height > 300):
    res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
    cv2.imwrite(main_directory + main_img_name + "Nface" + str(n + 1) + ".jpg", res)
  

def new_resolution(dim_tuple):
  dividing_factor = 1.0
  if dim_tuple[1] <= 300 and dim_tuple[0] >= 40:
    dividing_factor = (1/130) * dim_tuple[1] + (9/13)
  image_ratio = dim_tuple[1] / dim_tuple[0]
  new_height = dim_tuple[1] / dividing_factor
  new_width = new_height * image_ratio
  return (int(new_width), int(new_height)) 

def does_it_overlap(face_list, box):
  x1 = box[0]
  x2 = box[2]
  y1 = box[1]
  y2 = box[3] 
  for i in enumerate(face_list):
    x3 = i[1][0][0]
    y3 = i[1][0][1]
    x4 = i[1][0][2]
    y4 = i[1][0][3]
    if not (((x2 < x3)) or ((x1 > x4)) or ((y2 < y3)) or ((y1 > y4))):
      return True
  return False