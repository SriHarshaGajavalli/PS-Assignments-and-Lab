import re


def validate_email(email):
	if not re.match(r"^[A-Za-z0-9\._-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
		return False
	return True

def validate_mob(mob_no):
	if not re.match(r'[6789]\d{9}$', mob_no):
		return False
	return True



inp_email = input("Please Enter an Email Address: ")
inp_mob_no = input("Please Enter a valid 10 digit Indian Mobile Number: ")

print("Validating...........")
status_email = validate_email(inp_email)
status_mob = validate_mob(inp_mob_no)

if not status_email and not status_mob:
	print("please enter valid email and mobile number")
elif not status_email:
	print("please enter valid email")
elif not status_mob:
	print("please enter valid mobile number")
else:
	print("Yayy! Input details accepted!")
