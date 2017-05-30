# Copyright (c) 2015-2016 Internet Education and Research Laboratory (intERLab), Asian Institute of Technology, Thailand
# @author Upeka De Silva <st116384@ait.asia>

# enumerate_publisher.py
# This class is used to split large files into smaller segments
# inputs : file name, maximum segment size, segment number
# outputs : requested segment of the file, last segment number


import sys
import time
import argparse
import traceback
import math



class EnumeratePublisher(object):


    def __init__(self, fileName, maxSegmentSize, segmentNumber):
		self.fileName = fileName
		self.maxSegmentSize = maxSegmentSize
		self.segmentNumber = segmentNumber
		self.lastSegment = 0

    def getFileSegment(self):
		#read the content to be transmitted
		f = open(self.fileName, 'rb')
		theData = f.read()
		f.close()

		# get the length of data, ie size of the input file in bytes
		dataBytes = len(theData)

		#calculate the number of chunks to be created, depending on the file size and maximum segment size requested.
		numOfSegments = dataBytes/self.maxSegmentSize
		if(dataBytes%self.maxSegmentSize):
			numOfSegments+=1

		#check if the requested segment exists, if requested segment number is out of the avaialbe segment range, throw an ERROR
		if self.segmentNumber >= numOfSegments:
			raise ValueError('Invalid Segment Number for the file')

		#If has requested a valide segment, provide the requested segment of the file
		else:
			#if only one segment exists and requested segment =0, then segment = the file
			if numOfSegments == 1 and self.segmentNumber ==0:
				dataSegment = theData
				self.last_segment = self.segmentNumber
			#if more than one segment exists , extract the requested segment
			else:
				dataSegment =theData[self.segmentNumber * self.maxSegmentSize :(self.segmentNumber+ 1) * self.maxSegmentSize]
				self.last_segment = numOfSegments -1

			return (dataSegment, self.last_segment )
