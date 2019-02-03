# 振荡记录器 价格在箱体里来回。
class CBox:
	def __init__(self):
		self.IsOpen = False
		self.Before = -1  # 之前的值
		self.Last = -1  # 最新的值
		self.high = -1
		self.low = -1
		self.unit = 0.01


	# True 这个action信号要被过滤掉
	def NewValue(self, prc):
		self.Before = self.Last
		self.Last = prc
		if self.IsOpen:
			return self.InBox()

		if self.Before == -1: #初始化 一定不反对此信号
			return False 
		
		self.NewValue2()
		return False 

	def InBox(self):
		if self.low <= self.Last and self.Last <= self.high:
			return True  
		# 不在区间里的话
		self.Reset() 
		return False

	# 已经有一个值了，第二个值的处理
	def NewValue2(self):
		dif = abs(self.Last - self.Before)
		if dif > 2*self.unit:  #间隔很大，并不构成区间幅度
			return 

		# 构成区间幅度了
		self.NewOpen()

	def Reset(self):
		self.IsOpen = False
		self.NewValue2()

	def NewOpen(self):
		self.high,self.low = self.Last,self.Before
		if self.Last < self.Before:
			self.high,self.low = self.Before,self.Last
		self.IsOpen = True
