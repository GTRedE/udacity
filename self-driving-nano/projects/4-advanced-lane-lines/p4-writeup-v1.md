**Udacity Nanodegree &nbsp; | &nbsp; Self-Driving Car Engineer**
# Project 4: Advanced Lane Detection

### Goals
The goals of this project are to:
* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

The original Udacity template and source code for this project can be found [here in their Github repo](https://github.com/udacity/CarND-Advanced-Lane-Lines).

&nbsp;
### Results
For this project, I was able to accurately detect the driving lane and project it back onto the input from the vehicle's camera as required. Here is a video that shows the results.  

&nbsp;

<a href="https://www.youtube.com/watch?v=Zh3mrU5ELKQ" target="_blank"><img src="results/video-thumbnail.png" width="60%" /></a>


&nbsp;
### My Approach
You can find a step-by-step breakdown of my approach and the various parts of my pipeline [here in this Jupyter notebook](https://github.com/tommytracey/udacity/blob/master/self-driving-nano/projects/4-advanced-lane-lines/p4-advanced-lane-detection-final.ipynb). In the next section, I will outline how I addressed the required aspects of this project.


&nbsp;
---
## Rubric Points
In this section, I walk-through the [rubric points](https://review.udacity.com/#!/rubrics/571/view) individually and describe how I addressed each point in my implementation.

&nbsp;
### Camera Calibration

&nbsp;
#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result:

[(source code)](https://github.com/tommytracey/udacity/blob/master/self-driving-nano/projects/4-advanced-lane-lines/p4-advanced-lane-detection-final.py#L93)

<img src='results/chess-boards.png' width="80%"/>

&nbsp;
### Pipeline

&nbsp;
#### 1. Provide an example of a distortion-corrected image.

Now that we've calibrated our camera, we can apply the resulting matrix from the [stored calibration](https://github.com/tommytracey/udacity/blob/master/self-driving-nano/projects/4-advanced-lane-lines/camera_cal/calibration1.p) to correct the distortion in our driving images.

[(source code)](https://github.com/tommytracey/udacity/blob/master/self-driving-nano/projects/4-advanced-lane-lines/p4-advanced-lane-detection-final.py#L175)

In the example below, the distortion correction is most noticeable if you look at the traffic sign on the left side of the road. You'll notice that the sign now appears closer and it faces the viewer straight on instead of at an angle.

<img src='results/undistorted.png' width="80%"/>

&nbsp;
#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I used a combination of color and gradient thresholds to identify lane lines within the driving images and then generate a binary image. But determining which gradients and which parameters yield the best results requires a lot of trial and error. To make this tuning process more efficient, I used this [Jupyter Widgets function](http://ipywidgets.readthedocs.io/en/stable/examples/Using%20Interact.html), which allows you to tune the parameters and instantly view the results within your Jupyter notebook. A very useful tool!

[(source code)](https://github.com/tommytracey/udacity/blob/master/self-driving-nano/projects/4-advanced-lane-lines/p4-advanced-lane-detection-final.py#L54)

<img src='results/threshold-controls-2.gif' width="60%"/>

&nbsp;

After experimenting with lots of different threshold parameters, I was able to produce optimal results for each gradient. Here are the individual gradients I explore.

[(source code)](https://github.com/tommytracey/udacity/blob/master/self-driving-nano/projects/4-advanced-lane-lines/p4-advanced-lane-detection-final.py#L368)

![x-gradient](results/x-gradient.png)

![y-gradient](results/y-gradient.png)

![mag-gradient](results/mag-gradient.png)

![dir-gradient](results/dir-gradient.png)

&nbsp;
#### Color Channels

I also used this approach to evaluate different color channels.






&nbsp;
#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `warper()`, which appears in lines 1 through 8 in the file `example.py` (output_images/examples/example.py) (or, for example, in the 3rd code cell of the IPython notebook).  The `warper()` function takes as inputs an image (`img`), as well as source (`src`) and destination (`dst`) points.  I chose the hardcode the source and destination points in the following manner:

[(source code)]()

<img src='results/ABCDE.png' width="60%"/>

&nbsp;
```python
src = np.float32(
    [[(img_size[0] / 2) - 55, img_size[1] / 2 + 100],
    [((img_size[0] / 6) - 10), img_size[1]],
    [(img_size[0] * 5 / 6) + 60, img_size[1]],
    [(img_size[0] / 2 + 55), img_size[1] / 2 + 100]])
dst = np.float32(
    [[(img_size[0] / 4), 0],
    [(img_size[0] / 4), img_size[1]],
    [(img_size[0] * 3 / 4), img_size[1]],
    [(img_size[0] * 3 / 4), 0]])
```
&nbsp;

This resulted in the following source and destination points:

| Source        | Destination   |
|:-------------:|:-------------:|
| 585, 460      | 320, 0        |
| 203, 720      | 320, 720      |
| 1127, 720     | 960, 720      |
| 695, 460      | 960, 0        |

&nbsp;

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

[(source code)]()

<img src='results/ABCDE.png' width="60%"/>

&nbsp;

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Then I did some other stuff and fit my lane lines with a 2nd order polynomial kinda like this:

< insert equations >

[(source code)]()

<img src='results/ABCDE.png' width="60%"/>

&nbsp;

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

[(source code)]()

<img src='results/ABCDE.png' width="60%"/>

&nbsp;

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in lines # through # in my code in `yet_another_file.py` in the function `map_lane()`.  Here is an example of my result on a test image:

[(source code)]()

<img src='results/ABCDE.png' width="60%"/>

&nbsp;

---

### Discussion

&nbsp;
#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.


#### Things that worked:



#### Things that didn't work:

* CLAHE
