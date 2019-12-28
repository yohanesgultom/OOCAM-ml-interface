Repository for the OOCAM ML Interface

For using the current interface, please follow these steps -  
1. Clone the repo to a suitable location:  
    git clone https://github.com/shark-trek/OOCAM-ml-interface.git  
2. Install dependencies :  
    (i) Navigate to the directory where the repo has been cloned  
    (ii) Double click the installer.bat file  
3. Open Web Interface:  
    (i) Open the 'flaskInterface.py' file  
    (ii) Open the 'run.html' file    
4. To Train Model :  
    (i) In the first text field (File:), enter the directory where the images to be trained are located  
        Change single backslashes to double backslashes  
        E.g. : C:\\\Users\\\Dhruv Aggarwal\\\Downloads\\\ResizedMantaImages  
    (ii) In the second text field (Split:), enter the split value : a float value between 0 and 1  
        0.8 would mean 80% of the images are for train, 20% for test  
    (iii) In the third text field (Epoch:), enter number of epochs: no. of complete presentations of dataset to be learned by machine  
    (iv) Click Train and give it a little time to process  
        The model (model.h5) and the labels file (labels.dat) will be generated and placed into the 'output' folder    
        The maximum validation accuracy achieved shall be shown on a new webpage  
5. To Predict an Image :
      (i) In the first text field (Model:), enter the location of the model.h5 file  
      (ii) In the second text field (Image:), enter the location of the image (jpg) file that needs to be predicted  
      (iii) In the third text field (Labels:), enter the location of the labels.dat file.  
      Note: Change single backslashes to double backslashes  
      E.g. C:\\\Users\\\Dhruv Aggarwal\\\OOCAM-ml-interface\\output\\\label.dat     
      (iv) The prediction among the label types will be displayed on a new webpage    
