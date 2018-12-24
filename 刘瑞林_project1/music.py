from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


import soundfile as sf
import numpy as np
import time
import pygame

AudioFile = "AllFallsDown.wav"

def playMusic(filename):
	pygame.mixer.init() 
	pygame.mixer.music.load(filename)
	pygame.mixer.music.set_volume(0.5) 
	pygame.mixer.music.play(0,0)

class draw():
	frames = []
	signals = []
	deltax = 0.01
	iter = -1
	j = 0
	begin_time = 0
	def drawframe(self, x, y, r, g, b):
		glColor3f(r, g, b)
		glBegin(GL_POLYGON)
		x = (x-300)*self.deltax/4
		glVertex2f(x,0.0)
		glVertex2f(x+self.deltax/8,0)
		glVertex2f(x+self.deltax/8,y)
		glVertex2f(x,y)
		glEnd()
		

	def drawFunc(self):
		glClear(GL_COLOR_BUFFER_BIT)

		if (self.iter == -1):
			playMusic(AudioFile)
			self.begin_time = time.time()
			self.iter = 0
		else:
			self.iter = int((time.time() - self.begin_time) / 0.0125)

		for j in range(600):
			self.drawframe(j, self.frames[self.iter][j], 156/255, 33/255, 137/255)
		glFlush()
		glBegin(GL_LINE_STRIP)
		for j in range(640):
			x = self.iter * self.frame_step + int((j-320) * 138 / 32)
			p = (j-320) * self.deltax / 4
			if (x<0 or x>=len(self.signals)):
				glVertex2f(p,-0.5)
			else:
				glVertex2f(p,self.signals[x]-0.5)
		glEnd()
		glFlush()


	# 大三, 数字信号处理PJ的一部分, 提取频谱
	def __init__(self):
		signal, sample_rate = sf.read(AudioFile)
		signal = [i[0] for i in signal]
		self.signals = signal / np.max(signal) /2
		pre_emphasis = 0.97
		signal = np.array(signal)
		signal = np.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])
		
		frame_size =   0.025
		frame_stride = 0.0125

		frame_length, frame_step = frame_size * sample_rate, frame_stride * sample_rate  # Convert from seconds to samples
		signal_length = len(signal)
		frame_length = int(round(frame_length))
		frame_step = int(round(frame_step))

		self.frame_step = frame_step

		num_frames = int(np.ceil(float(np.abs(signal_length - frame_length)) / frame_step))  # Make sure that we have at least 1 frame

		pad_signal_length = num_frames * frame_step + frame_length
		z = np.zeros((pad_signal_length - signal_length))
		pad_signal = np.append(signal, z) # Pad Signal to make sure that all frames have equal number of samples without truncating any samples from the original signal

		indices = np.tile(np.arange(0, frame_length), (num_frames, 1)) + np.tile(np.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T
		frames = pad_signal[indices.astype(np.int32, copy=False)]

		NFFT = 1200
		
		frames *= np.hamming(frame_length)	
		mag_frames = np.absolute(np.fft.rfft(frames, NFFT))  # Magnitude of the FFT
		pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))
		
		self.frames = pow_frames / np.max(pow_frames) *5


if __name__ == "__main__":
	
	d = draw()

	glutInit()
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
	glutInitWindowPosition(100, 200)
	glutInitWindowSize(1080, 720)
	glutCreateWindow("music")
	
	glutDisplayFunc(d.drawFunc)
	glutIdleFunc(d.drawFunc)
	glutMainLoop()
