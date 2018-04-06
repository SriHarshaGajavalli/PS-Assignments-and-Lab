from simpledelegator import SimpleDelegator, get_delegated
from collections import namedtuple

User = namedtuple('User', 'first_name last_name')
class UserPresenter(SimpleDelegator):
	@property
	def name(self):
		return self.first_name + ' ' + self.last_name
		
user = UserPresenter(User('Vaishnav K', 'Murali'))
print("First Name: " + user.first_name)
print("Last Name: " + user.last_name)
print("Name: " + user.name)

