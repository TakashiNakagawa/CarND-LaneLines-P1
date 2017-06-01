# **Finding Lane Lines on the Road**


---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image2]: ./doc_images/separate_lane.jpg "SeparateLane"
[image3]: ./doc_images/extend_lane.jpg "ExtendLane"

---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

<!-- My pipeline consisted of 5 steps. First, I converted the images to grayscale, then I ....

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...

If you'd like to include images to show how the pipeline works, here is how to include an image: -->

#### My pipeline consisted of 6 steps.
1. convert the images to grayscale
2. apply GaussianBlur to images
3. detect edges by canny algorithm
4. extract edges by applying an image mask
5. convert edges to lines by Hough algorithm
6. overlay original image and lines

#### Step 5 consisted of 5 steps.
1. apply cv2.HoughLinesP
2. separate left and right lanes
3. lanes are extended to image border
4. apply an image mask to lines
5. left and right lanes are extracted to a single line

#### separate left and right lanes
In order to separate left and right lanes, I calculated the inner product of y-axis and lane direction.  
(lane direction was adjusted so that x value was to be positive beforehand.)  
if absolute of inner product value was too small, it was not lane. it might be noise.
if an inner product was positive, then the lane might be the right lane.  
if an inner product was negative, then the lane might be the left lane.  

![alt text][image2]

#### lanes are extended to image border
In order to extend lanes, I calculated intersect points of lane and image borders.  
I select near side points, then I apply image mask to trim lanes.

![alt text][image3]

#### left and right lanes are extracted to a single line
In order to extract a single line, I calculated the angle of lanes and y-axis.  
I sorted lanes by angle order, then I choose middle index of angle.  


### 2. Identify potential shortcomings with your current pipeline

There are several shortcomings.
1. When a white or yellow lane is small, cv2.HoughLinesP needs parameter changing. So it is not robust.
2. When other cars running in front of this car, a lane can not be captured. So it will be difficult to detect lane.

### 3. Suggest possible improvements to your pipeline

There are several possible improvements.
1. If vanishing point could be decided, then select edges, lanes could be robust. Because lanes are on the vanishing point. In order to decide vanishing point, optical flow using sequential images might be needed.
2. With sequential images, if lanes are lost, then previous lanes of the image would compensate current lanes.
