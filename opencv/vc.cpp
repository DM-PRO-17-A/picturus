// What's a makefile
// g++ video_capture.cpp `pkg-config --libs --cflags opencv` -o vc.out

#include <iostream>
#include <vector>
#include <stdio.h>
#include "opencv2/opencv.hpp"
#include <string>
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "math.h"

using namespace std;
using namespace cv;

int Distance(Vec3b color1, Vec3b color2);
Mat Region(Mat image, Vec3b red, Vec3b blue, int radii[2]);
Mat CropRegion(Mat image, Mat T, int limit);
Mat Preprocessing(Mat image, Vec3b red, Vec3b blue, int radii[2], int limit);

Vec3b red = Vec3b(123,34,30); 
Vec3b blue = Vec3b(21,42,95); 
//int radii[] = {25,25};
int radii[] = {30,30};
int limit = 10000;

Mat Region(Mat image, Vec3b red, Vec3b blue, int radii[2])
{
  int x = image.cols;
  int y = image.rows;
  Mat T(y, x, CV_8UC1);
  for(int i=0;i<y;i++){
    for(int j=0;j<x;j++){
      Vec3b rgb=image.at<Vec3b>(i,j);
      int reddist = Distance(rgb, red);
      int bluedist = Distance(rgb, blue);
      if(reddist < radii[0] || bluedist < radii[1])
      {
        T.at<unsigned char>(i,j) = 255;
      }
      else
      {
        T.at<unsigned char>(i,j) = 0;
      }
    }
  }
  return T;
}

Mat CropRegion(Mat image, Mat T, int limit)
{
  Mat mat, crop;
  dilate(T, T, getStructuringElement(MORPH_ELLIPSE, Size(3, 3)));
  dilate(T, T, getStructuringElement(MORPH_ELLIPSE, Size(3, 3)));
  dilate(T, T, getStructuringElement(MORPH_ELLIPSE, Size(3, 3)));
  mat = T.clone();
  floodFill(mat, Point(0,0), Scalar(255));
  bitwise_not(mat, mat);
  T = (T | mat);
  Moments oMoments = moments(T);
  double dM01 = oMoments.m01;
  double dM10 = oMoments.m10;
  double dArea = oMoments.m00;
  if (dArea > limit)
  {
    int posX = dM10 / dArea;
    int posY = dM01 / dArea;
    //int i = posX;
    //cout << i << endl;
    //while((int)T.at<uchar>(i,posY) < 50)
    //{
    //  i++;
    //}
    //int radius = int(i/3) - posX;
    //int radius = int(i/3) - posX;
    //int radius = sqrt(dArea/M_PI)/9;
    int radius = sqrt(dArea/3)/9;
    int x = posX-radius;
    int y = posY-radius;
    int s = 2*radius;
    Mat crop = image.clone();
    line(crop, Point(x,y), Point(x+s,y), Scalar(255, 255, 255), 1, 8);
    line(crop, Point(x,y+s), Point(x+s,y+s), Scalar(255, 255, 255), 1, 8);
    line(crop, Point(x,y), Point(x,y+s), Scalar(255, 255, 255), 1, 8);
    line(crop, Point(x+s,y), Point(x+s,y+s), Scalar(255, 255, 255), 1, 8);
    cout << x << " " << y << " " << s << endl;
    //crop = image(Rect(x, y, s, s));
    return crop;
  }
  else {
    //crop = T(Rect(50, 50, 32, 32));
    Mat T(image.cols, image.rows, CV_8UC1);
    return T;
  }
  //mat.release();
  //return crop;
}

int Distance(Vec3b color1, Vec3b color2)
{
  int r1 = color1.val[0];
  int g1 = color1.val[1];
  int b1 = color1.val[2];
  int b2 = color2.val[0];
  int g2 = color2.val[1];
  int r2 = color2.val[2];
  int res = sqrt(pow(r1-r2,2)+pow(g1-g2,2)+pow(b1-b2,2));
  return res;
}

Mat Preprocessing(Mat image, Vec3b red, Vec3b blue, int radii[2], int limit)
{
  Mat reg = Region(image, red, blue, radii);
  Mat crop = CropRegion(image, reg, limit);
  //reg.release();
  //Mat res;
  //resize(crop, res, cvSize(32, 32), 0, 0, CV_INTER_AREA );
  //crop.release();
  //reg.release();
  return crop;
}

int main() {
  // Create a VideoCapture object and open the webcam
  // Index signifies which webcam, use 0 on pynq
  VideoCapture cap(0);

  // Check if camera opened successfully
  if (!cap.isOpened()) {
    cout << "Error opening video stream or file" << endl;
    return -1;
  }

  int w = 432;
  int h = 240;
  int fps = 5;

  //int ch = 180;
  //int cw = 216;

  cap.set(CV_CAP_PROP_FRAME_WIDTH, w);
  cap.set(CV_CAP_PROP_FRAME_HEIGHT, h);
  cap.set(CV_CAP_PROP_FPS, fps);
  //cout << cap.get(CV_CAP_PROP_FRAME_WIDTH) << endl;
  //int count_frame = 1;

  //int winSize = 32;


  while (1) {
    Mat frame;

    // Capture frame-by-frame
    cap >> frame;

    // If the frame is empty, break immediately
    if (frame.empty())
     // break;
      continue;

    // Crop image to size
    //frame = frame(Rect(cw, 0, cw, ch));
    Mat cropped;
    cropped = Preprocessing(frame, red, blue, radii, limit);
    if (cropped.empty())
      continue;

    // Convert image to RGB
    // cvtColor(frame, frame, cv::COLOR_BGR2RGB);

    // Display the resulting frame
    imshow("Cropped", cropped);
    imshow("Frame", frame);

    // Press  ESC on keyboard to exit
    char c = (char)waitKey(1);
    if (c == 27)
      break;

    cout << "Frame " << endl;
  }

  // When everything done, release the video capture object
  cap.release();

  // Closes all the frames
  destroyAllWindows();

  return 0;
}
