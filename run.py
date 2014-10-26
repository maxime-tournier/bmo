#!/usr/bin/env python

import argparse
import cv2
from numpy import empty, nan
import os
import sys
import time

import CMT
import numpy as np


CMT = CMT.CMT()

parser = argparse.ArgumentParser(description='Track an object.')

parser.add_argument('--preview', dest='preview', action='store_const', const=True, default=None, help='Force preview')
parser.add_argument('--no-preview', dest='preview', action='store_const', const=False, default=None, help='Disable preview')
parser.add_argument('--no-scale', dest='estimate_scale', action='store_false', help='Disable scale estimation')
parser.add_argument('--with-rotation', dest='estimate_rotation', action='store_true', help='Enable rotation estimation', default = True)
parser.add_argument('--bbox', dest='bbox', help='Specify initial bounding box.')
parser.add_argument('--pause', dest='pause', action='store_true', help='Specify initial bounding box.')
parser.add_argument('--output-dir', dest='output', help='Specify a directory for output data.')
parser.add_argument('--quiet', dest='quiet', action='store_true', help='Do not show graphical output (Useful in combination with --output-dir ).')
parser.add_argument('--skip', dest='skip', action='store', default=None, help='Skip the first n frames', type=int)

parser.add_argument('--width', dest = 'width', help='Width for camera capture', default = 640)
parser.add_argument('--height', dest = 'height', help='Height for camera capture', default = 480)
parser.add_argument('--flip', dest = 'flip', help='Flip image horizontally', default = True)
parser.add_argument('--detect', dest = 'detect', help='Use automatic face detection', default = True)

args = parser.parse_args()

CMT.estimate_scale = args.estimate_scale
CMT.estimate_rotation = args.estimate_rotation

# Clean up
cv2.destroyAllWindows()

preview = args.preview


# If no input path was specified, open camera device
cap = cv2.VideoCapture(0)

if args.width:  cap.set(3, float(args.width) )
if args.height: cap.set(4, float(args.height) )

# Check if videocapture is working
if not cap.isOpened():
        print 'Unable to open video input.'
        sys.exit(1)

# wrap frame read
def read():
        status, im = cap.read()
        if args.flip: im = cv2.flip(im, 1)
        return status, im



def detect():
        path = '/usr/local/opt/opencv/share/OpenCV/'

        path += '/haarcascades/haarcascade_frontalface_alt.xml'
        cascade = cv2.CascadeClassifier( path )

        faces = []

        print 'detecting face, please smile :D'
        
        while len(faces) == 0:
                # Read first frame
                status, im0 = read()
                im_gray0 = cv2.cvtColor(im0, cv2.COLOR_BGR2GRAY)
                im_draw = np.copy(im0)

                faces = cascade.detectMultiScale(
                        im_gray0,
                        scaleFactor=1.1,
                        minNeighbors=5,
                        minSize=(30, 30),
                        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                )
                if len(faces) == 0:
                        sys.stdout.write('.')
                        sys.stdout.flush()

        print 'done'
        (x, y, w, h) = faces[0]

        (tl, br) = ((x, y), (x + w, y + h))
        return im_gray0, (tl, br)

im_gray0, (tl, br) = detect()
CMT.initialise(im_gray0, tl, br)


face_pos = []

import bmo

constant = [float(5e7)]
from PySide import QtGui, QtCore
def key_press(e):
        k = e.key()
        if k == ord('+'):
                constant[0] *= 2
        elif k == ord('-'):
                constant[0] /= 2
        elif k == QtCore.Qt.Key_Space:
                im_gray0, (tl, br) = detect()
                CMT.initialise(im_gray0, tl, br)

        print constant[0]

print '+/- to increase/decrease depth factor'
print 'space to redetect face'

bmo.key_press = key_press

frame = 1
import math

def loop():
        # Read image
        status, im = read()
        if not status:
                pass
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im_draw = np.copy(im)

        tic = time.time()
        CMT.process_frame(im_gray)
        toc = time.time()

        # Display results
        coords = None

        # Draw updated estimate
        if CMT.has_result:

                # cv2.line(im_draw, CMT.tl, CMT.tr, (255, 0, 0), 4)
                # cv2.line(im_draw, CMT.tr, CMT.br, (255, 0, 0), 4)
                # cv2.line(im_draw, CMT.br, CMT.bl, (255, 0, 0), 4)
                # cv2.line(im_draw, CMT.bl, CMT.tl, (255, 0, 0), 4)

                shape = im_draw.shape
                coords = tuple(CMT.center[i] / shape[i] for i in xrange(2))

                diag = [ np.array(CMT.tl) - np.array(CMT.br),
                         np.array(CMT.tr) - np.array(CMT.bl) ]

                length = np.array( [ math.sqrt(x.dot(x)) for x in diag ] )

                size = np.amax( length )

                depth = (constant[0] / float( shape[0])) / size

                coords = (coords[0], coords[1], depth)


        # util.draw_keypoints(CMT.tracked_keypoints, im_draw, (255, 255, 255))
        # # this is from simplescale
        # util.draw_keypoints(CMT.votes[:, :2], im_draw)  # blue
        # util.draw_keypoints(CMT.outliers[:, :2], im_draw, (0, 0, 255))

      
        # if not args.quiet:
        # 	cv2.imshow('main', im_draw)

        # 	# Check key input
        # 	k = cv2.waitKey(pause_time)
        # 	key = chr(k & 255)
        # 	if key == 'q':
        # 		break
        # 	if key == 'd':
        # 		import ipdb; ipdb.set_trace()

        # Remember image
        im_prev = im_gray

        # Advance frame number
        # frame += 1
        return coords

bmo.track( loop, 100 )
bmo.exec_()

