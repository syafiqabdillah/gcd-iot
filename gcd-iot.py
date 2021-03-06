#!/usr/bin/python
#
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

import jetson.inference
import jetson.utils
import cv2
import sys

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.gstCamera(1280, 720, "/dev/video0")
# camera = cv2.VideoCapture()
display = jetson.utils.glDisplay()

if __name__=="__main__":
	max_people_count = 5
	while display.IsOpen():
		img, width, height = camera.CaptureRGBA()
		detections = net.Detect(img, width, height)
		people_count = 0
		message = "Aman"
		for det in detections:
			if det.ClassID == 1: # ClassID 1 is person
				people_count += 1
		if people_count > max_people_count:
			message = "Tidak Aman"
		display.RenderOnce(img, width, height)
		display.SetTitle("West Gate Jakarta Station|{:.0f} FPS|Detected:{} Max:{}| Status : {}".format(net.GetNetworkFPS(), people_count, max_people_count, message))


