# Tiny Face Detector in TensorFlow

 A Regions of Interest (ROI) extractor for implementation of [Finding Tiny Faces in the Wild with Generative Adversarial Network](https://ivul.kaust.edu.sa/Pages/pub-tiny-faces.aspx) created at External Internship Program EIP MLBLR, using [cydonia999's](https://github.com/cydonia999/Tiny_Faces_in_Tensorflow) implementation of Tiny Face Detector from [authors' MatConvNet codes](https://github.com/peiyunh/tiny)[1].
 
 Extracts equal number of non-faces as faces (ROI) detected within an image.

# Requirements

Codes are written in Python. At first install [Anaconda](https://docs.anaconda.com/anaconda/install.html).
Then install [OpenCV](https://github.com/opencv/opencv), [TensorFlow](https://www.tensorflow.org/).

# Usage

## Converting a pretrained model

`matconvnet_hr101_to_pickle` reads weights of the MatConvNet pretrained model and 
write back to a pickle file which is used in a TensorFlow model as initial weights.

1. Download a [ResNet101-based pretrained model(hr_res101.mat)](https://www.cs.cmu.edu/%7Epeiyunh/tiny/hr_res101.mat) 
from the authors' repo.

2. Convert the model to a pickle file by:
```
python matconvnet_hr101_to_pickle.py 
        --matlab_model_path /path/to/pretrained_model 
        --weight_file_path  /path/to/pickle_file
```

## Tesing Tiny Face Detector in TensorFlow

1. Prepare images in a directory. 

2. `tiny_face_eval.py` reads images one by one from the image directory and 
write images to an output directory with bounding boxes of detected faces.
```
python tiny_face_eval.py
  --weight_file_path /path/to/pickle_file
  --data_dir /path/to/input_image_directory
  --output_dir /path/to/output_directory
```

# Acknowledgments

- Many python codes are borrowed from [chinakook's MXNet tiny face detector](https://github.com/chinakook/hr101_mxnet)
- parula colormap table is borrowed from [`fake_parula.py`](https://github.com/BIDS/colormap/blob/master/fake_parula.py).

# References

1. Hu, Peiyun and Ramanan, Deva,
     Finding Tiny Faces,
     The IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2017).
     [project page](https://www.cs.cmu.edu/~peiyunh/tiny/), [arXiv](https://arxiv.org/abs/1612.04402)

2. Michael J. Wilber, Vitaly Shmatikov, Serge Belongie,
     Can we still avoid automatic face detection, 2016.
     [arXiv](https://arxiv.org/abs/1602.04504)

