class GameConversionUtils:
	
	def __init__(self, W, H, ppm):
		
		self.ppm = ppm # Pixels per meter
		self.mpp = 1/self.ppm # Meters per pixel
	
		# Window information
		self.W = W
		self.H = H

	# Changes local coordinates to screen coordinates
	def l2s(self, x):
		px = x[0] * self.ppm
		py = self.H - x[1] * self.ppm
		
		return [px, py]

	# Changes screen coordinates to local coordinates
	def s2l(self, position):
		px = position[0] * self.mpp
		py = (self.H - position[1]) * self.mpp
		
		return [px, py]
