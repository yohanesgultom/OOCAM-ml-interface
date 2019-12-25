# OOCAM-ml_interface
Repository for ML interface for OOCAM.

Clone the repo here: https://github.com/greatblitz982/OOCAM-ml_interface

Couple of dependencies you're gonna need. Install them with:

pip3 install flask tensorflow numpy opencv-python

(I recommend using a virtualenv but that's up to you).

Next, navigate to the directory that you've cloned the repository to, and run "python3 flaskInterface.py" and visit localhost:5000/. 

In the first text field, enter the directory where the images you want to train on are located with double backslashes. For example:

C:\\Users\\admin\\Downloads\\ResizedMantaImages

The folder you're selecting (in the above example) should contain the folders as the class names, and each image should be contained within those folders. Take a look at the example I've used here: https://drive.google.com/open?id=1W3hJv2T-JTAbL5WTt3SahUD1QtPnguvR

The second textbox is the train/test split: a float value between 0 and 1. 0.8 would mean 80% of the images are for train, 20% for test.

The last is epochs, self explanatory.

Click Train, give it a bit of time. Shortly after, the model will be generated and placed into the same folder (model.h5) and the maximum validation accuracy achieved will be displayed.

Couple of caveats:
1. Evaluate isn't done yet, but I'll try and finish it soon enough.
2. This model is a placeholder model, nowhere near close to good. The point is, it works and it's easy to swap it out for a properly functioning model.