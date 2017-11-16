// What's a makefile
// g++ video_capture.cpp `pkg-config --libs --cflags opencv` -o vc.out

#include <iostream>
#include "opencv2/opencv.hpp"

using namespace std;
using namespace cv;


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

  int ch = 180;
  int cw = 216;

  cap.set(CV_CAP_PROP_FRAME_WIDTH, w);
  cap.set(CV_CAP_PROP_FRAME_HEIGHT, h);
  cap.set(CV_CAP_PROP_FPS, fps);

  int count_frame = 1;

  int winSize = 32;


  while (1) {
    Mat frame;

    // Capture frame-by-frame
    cap >> frame;

    // If the frame is empty, break immediately
    if (frame.empty())
      break;

    // Crop image to size
    // frame = frame(Rect(cw, 0, cw, ch));

    // Convert image to RGB
    // cvtColor(frame, frame, cv::COLOR_BGR2RGB);

    // Display the resulting frame
    imshow("Frame", frame);

    // Press  ESC on keyboard to exit
    char c = (char)waitKey(1);
    if (c == 27)
      break;

    cout << "Frame";
  }

  // When everything done, release the video capture object
  cap.release();

  // Closes all the frames
  destroyAllWindows();

  return 0;
}
