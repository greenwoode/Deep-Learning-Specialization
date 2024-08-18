# Specialized CNN model

This is the code to train and test verious cnn models on a subset of the ImageNet dataset and a custom dataset generated in the [dataset branch](https://github.com/greenwoode/Deep-Learning-Specialization/tree/Data). This code expects data to be inside `./Data/` and for the models to be in `./models/` .

Utilizes latest version of TensorFlow, and will require being install on a linux system or WSL2 as a result. Creating an enviroment with the `requirements.txt` should be the only prerequisite to running any of the scripts. Google colab will readily accept the .ipynb files and should have most if not all of the requirements already. 

Adjusting the `target` variable will allow you to point to a custom dataset that is not either of the two included, as long as it follows the same folder structure of `./{dataset}/{split}/{images}`. You can utilize the dataset generating code in the [dataset branch](https://github.com/greenwoode/Deep-Learning-Specialization/tree/Data) to create a new dataset using a different YouTube search prompt as well.

- `CNN_TF.ipynb`
  - The base model training code, and overall evaluation
- `CNN-TF-Bulk.ipynb`
  - Code to train multiple models in one run, with varrying amounts of training images or classes.
- `Charting.ipynb`
  - The code that generate all of the charts and graphs found in the associated paper. 
- `Demo.ipynb`
  -  A simple script that allows prediction using individual images instead of a dataset.
