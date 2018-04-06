class one(object):
	def hello(self):
		print("\nHello PS Class! This is Sri Harsha\n")
		
	def AboutMe(self):
		print("\nI am a third year research undergrad\n") 
		
class two(object):
	def __init__(self, obj):
		self.main = obj
	
	def welcome(self):
		self.main.hello()
		
	def detail(self):
		self.main.AboutMe()
		
		
sri = one()
stu = two(sri)

stu.welcome()
stu.detail()
