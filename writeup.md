# **Finding Lane Lines on the Road**


---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"

---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

<!-- My pipeline consisted of 5 steps. First, I converted the images to grayscale, then I ....

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...

If you'd like to include images to show how the pipeline works, here is how to include an image: -->

My pipeline consisted of 6 steps.

1. convert the images to grayscale
2. apply GaussianBlur to images
3. detect edges by canny algorithm
4. extract edges by applying an image mask
5. convert edges to lines by Hough algorithm
6. overlay original image and lines

Step 5 consisted of 3 steps.

1.
2.
3.


![alt text][image1]


### 2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when ...

Another shortcoming could be ...

白線がこまかい
カメラを取り替えた場合
他の車が多い場合
画質が変わった場合


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to ...

Another potential improvement could be to ...

消失点を求める
単体の画像ではなくシーケンス画像として扱えるようにすればもう少しうまく動くようになる
前回の白線の位置も覚えるようにしておく
