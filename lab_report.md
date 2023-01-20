# Lab 1: Git Cam

## Intro

Today we are getting accustomed to commonly used tools like Git and conda. We will use our learnings today to perform some computer vision.

## Git Setup

### Task 1: Test Github Repo

- Create a new repository on github named '180DA-WarmUp' and make sure it is public.

    ![Repo Create Screen](lab_report_files\repo_creation_ss.jpg)

    The newly created repo can be found at: [github.com/afantino951/180DA-WarmUp](https://github.com/afantino951/180DA-WarmUp)

## Package Managers

We are advised to install Anaconda or Miniconda as a package manager. These package managers allow us to install different packages (and different versions of packages) in different projects. This makes it easier to collaborate since all external packages are managed by conda and each team does not need to keep note of the versions of the packages that they are using.

### Install Anaconda/Miniconda

Since I have already installed miniconda on my Linux VM, I was able to skip the install steps and go straight to updating to the newest version of conda.

I ran the following commands:

``` !bash
conda --version 
conda update -n base -c defaults conda
```

As a final test of my conda installation, I tried to install `Numpy` with:

```!bash
conda install numpy
```

## Virtual Environments

We are not going to clone our newly created Github repo to our local machine using `git clone https://github.com/afantino951/180DA-WarmUp.git`, and make a virtual environment with conda to isolate the packages that we want to include in our project to the folder containing the repository.

Execute the following commands:

```!bash
conda -V
conda create -n warmupenv python 
conda activate warmupenv
conda install pip
conda install numpy matplotlib pandas
conda deactivate
```

**Note:** It is important to activate your conda environments when you plan on working on your project or else your project will not find the packages that it is expecting.

### Task 2: Create test.txt and push to remote

- We are now going to run `nvim test.txt` and add some sample text to the file. Then, we add, commit, and push the changes to our remote Github repo. We then check the web-based GUI to see that the changes have indeed been recorded.

    ![Github File Repo](lab_report_files\Task_2.jpg)

## OpenCV Install and Python Scripts

We are now going to install OpenCV in our conda virtual environment with the command:

```!bash
conda install -c conda-forge opencv
```

We are now going to verify that our install worked correctly by opening a Python CLI.

```!python
python
>> import cv2
>> import numpy
>> [PRESS CTRL-D]
```

### Task 3: Create and Run test.py

- Create the file test.py and add the following to the file:

    ```!python
    if __name__ == '__main__':
        x = "ECE_180_DA_DB"
        if x == "ECE_180_DA_DB":
            print("You are living in 2023")
        else: 
            x += " - Best class ever"
            print(x)
    ```

- Now run `python test.py`. You should expect to see the output `You are living in 2023`. We will now commit and push the new file to the remote repository.

## Image Processing

I chose to skip this section since I had prior experience with OpenCV. I also looked ahead to learn about the video related image processing because that is what my team is going to be using for our final product.

## Camera Exercises

We are going to use the camera for localization

### Task 4: Camera Exercises

1. I am choosing my water bottle since it is a single color of blue, and will be easy to threshold.I expect that the threshold for RGB will be easier to implement and have a tighter range since the bottle is just the one color.

    - When comparing the performance of the HSV and RGB threshold I could not distinguish them from each other. The threshold range for HSV is slightly smaller than threshold range for RGB.

    |![HSV Result](lab_report_files\HSV_frame.jpg) |
    |:--:|
    | *HSV Threshold Result* |

    | ![RGB Result](lab_report_files\RGB_frame.jpg) |
    |:--:|
    | *RGB Threshold Result* |

    ```!python
    low_hsv = [97, 159, 112]
    high_hsv = [120, 255, 255]

    low_rgb = [0, 50, 140]
    high_rgb = [100, 150, 255]
    ```

2. Since the tracking subject has a reflective coating, I expect there will be a lot of variation between bright and dark lighting senarios. I shined my phone flashlight on the water bottle and evaluated the performance between the RGB thresholding and the HSV thresholding. RGB thresholding has better performance for tracking the object as compared to the performance of the HSV thresholding in non-ideal lighting conditions. This may be because my HSV range is too tight to handle these adverse conditions.

    |![HSV Light Result](lab_report_files\HSV_Light.jpg) |
    |:--:|
    | *HSV Lighting Result* |

    | ![RGB Light Result](lab_report_files\RGB_Light.jpg) |
    |:--:|
    | *RGB Lighting Result* |

3. I recorded the color of the water bottle with a color picker on my personal phone and fouynd that the RGB value was `(0,92,169)` and the HSV value was `(207,100%,33%)`. Since the RGB thresholding performed better to the adverse lighting test, I will continue to use it over the HSV thresholding. I made an RGB range with a separation of +-60.

    This initial experiment was unsucessful, so I changed found a threshold range that worked best with my phone at half brightness. It was:

    ```!python
    low_rgb = [0, 0, 231]
    high_rgb = [175, 255, 255]
    ```

    The color was able to be detected with this threshold range at medium brightness. Low and high brightness were also measured. The high brightness phone screen was able to be detected, but the low brightness phone screen was not able to be detected. However, with the high brightness phone, it took time for the camera to adjust to the brightness before the screen was detected.

    |![Blue Phone Medium Result](lab_report_files\Medium_Brightness.jpg) |
    |:--:|
    | *Blue Phone Medium Result* |

    |![Blue Phone High Result](lab_report_files\High_Brightness.jpg) |
    |:--:|
    | *Blue Phone High Result* |

    | ![Blue Phone Low Result](lab_report_files\Low_Brightness.jpg) |
    |:--:|
    | *Blue Phone Low Result* |

4. The new piece of code that finds the dominant color in a rectangle in the center of the frame uses K-means clustering. The dominant color in the 100px by 100px rectangle is then the color of the rectangle. When presented with a plain background, the color square is difficult to distinguish from the background. When I show an inconsistent background, like my face, it is easier to tell the rectangle from the frame. Therefore, the more indistinguishable the rectangle is from the frame, the more 'quality' we associate with the experiement.

    | ![No Water Bottle Result](lab_report_files\Dom_Non_Blue.jpg) |
    |:--:|
    | *No Water Bottle Result* |

    |![Blue Water Bottle Result](lab_report_files\Dom_Blue.jpg) |
    |:--:|
    | *Blue Water Bottle Result* |

    |![Blue Water Bottle with Flash Result](lab_report_files\Dom_Blue_Bright.jpg) |
    |:--:|
    | *Blue Water Bottle with Flash Result* |

    When there is a light shined on the water bottle, the dominant color detector performs less well as when it is in normal lighting conditions. This would make sense because the flash is a harsh light that makes a large variation in the color as the cylindrical shape of the bottle gets further from the light source from the inverse square law.

    |![Blue Phone Medium Result](lab_report_files\dom_blue_phone_med.jpg) |
    |:--:|
    | *Blue Phone Medium Result* |

    |![Blue Phone High Result](lab_report_files\dom_blue_phone_bright.jpg) |
    |:--:|
    | *Blue Phone High Result* |

    | ![Blue Phone Low Result](lab_report_files\dom_blue_phone_dim.jpg) |
    |:--:|
    | *Blue Phone Low Result* |

    There is little difference between the phone in the rectangle at medium brightness and max brightness. On the other hand, the phone the dimmest setting performed worse. This matches the experiement with the changing brightness object detector.

    Between the phone and the water bottle, the phone performed better. This is likely because the phone is a flat, uniform surface while the water bottle was cylindrical. The water bottle has the drawback of the inverse square law working against it.
