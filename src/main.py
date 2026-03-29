from server import Server
from menu import Menu
from order import Order
from user import User, Customer, DeliveryAgent, Vendor
from getpass import getpass		# for typing password without showing letters
import sys						# to exit program


# FOR TESTING ONLY.
# These should be replaced with environment variables later.
mango_username = input("Enter your MangoDB username: ")
mango_password = getpass("Enter your MangoDB password: ")

# Object declarations
server = Server(user_id=mango_username, passwd=mango_password)
user = User(server)

# HELPER FUNCTIONS

def check_logout_or_quit(answer: str) -> str:
	if answer.lower() == "quit":
		server.disconnect()
		sys.exit(0)
	elif answer.lower() == "logout":
		# Not sure what to do here yet
		return answer
	else:
		return answer

def input_str(msg: str, valid_answers: list[str] = None) -> str:
	"""
	Gets string input and checks if the user typed "quit" or "logout".
	:param msg: The message you want to display to the user
	:param valid_answers: (optional) A list of acceptable answers. You do not need to include "quit" or "logout" in this list.
	:return: the user's input
	"""

	# If any string input is acceptable, simply return the user's answer after checking for quit or logout
	if valid_answers is None:
		return check_logout_or_quit(input(msg))

	# Else, we need to check if the answer is valid.
	# Make sure that all the strings in valid_answers are in lower case.
	valid_answers = [s.lower() for s in valid_answers]
	while True:
		answer = check_logout_or_quit(input(msg))
		if answer.lower() in valid_answers:
			return answer
		else:
			print("Sorry, that was not a valid answer. Please try again")

# Stackoverflow to explain sys.maxsize:
# https://stackoverflow.com/questions/7604966/maximum-and-minimum-values-for-ints
def input_int(msg: str, minimum: int = -sys.maxsize - 1, maximum: int = sys.maxsize):
	"""
	Gets integer input and checks if the user typed "quit" or "logout".
	:param msg: The message you want to display to the user.
	:param minimum: The minimum value the user is allowed to input.
	:param maximum: The maximum value the user is allowed to input.
	:return: The user's input, as an int.
	"""
	while True:
		user_input = check_logout_or_quit(input(msg))
		try:
			answer = int(user_input)
		except ValueError:
			print("Sorry, please enter a valid integer.")
		else:
			if answer < minimum or answer > maximum:
				print("Sorry, please enter a valid integer.")
			else:
				return answer

# USER TASK FUNCTIONS

def login_or_signup():
	not_signed_in = True
	while not_signed_in:
		print("Welcome to Zucc It Up!")
		option = input_int("Please select an option:\n1. Login\n2. Signup\n> ", 1, 2)

		if option == 1:		# Login
			your_viu_id = input_str("Please enter your VIU ID number\n> ")
			your_password = getpass("Please enter your password\n> ")
			not_signed_in = not user.login(your_viu_id, your_password)
			if not_signed_in:
				print("Sorry, those login details were incorrect. Please try again.")
		else:				# Signup
			print("Let's get you started!")
			option = input_int("Choose a role:\n1. Customer\n2. Delivery Agent", 1, 2)
			your_role = "Customer" if option == 1 else "Agent"
			your_viu_id = input_str("Please enter your VIU ID number\n> ")
			your_password = getpass("Please enter a password\n> ")
			your_name = input_str("Please enter your name\n> ")
			your_email = input_str("Please enter your email address\n> ")
			not_signed_in = not user.signup(viu_id=your_viu_id, passwd=your_password, name=your_name, email=your_email, role=your_role)
			if not_signed_in:
				print("Sorry, something went wrong. Please try again.")
# end login_or_signup

# MAIN LOOP
if __name__ == "__main__":
	login_or_signup()
	print("Goodbye!")
	print("""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣠⡶⠒⠒⠶⣄⣠⡴⠚⠉⠁⠀⠀⠀⠀⠀⠉⠙⠳⢦⡀⠀⠀⠀⠀⠀⠀
⢠⡏⠀⠀⠀⠀⠘⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢧⡀⠀⠀⠀⠀
⢸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠋⢱⠀⠀⢠⠉⢡⠀⠀⠀⠀⠀⠻⡄⠀⠀⠀
⠀⣧⠀⠀⠀⠀⠀⠀⠀⠀⢸⣧⣾⠄⠀⢸⣦⣾⠀⠀⠀⠀⠀⠀⢻⡄⠀⠀
⠀⠘⢧⡀⠀⠀⠀⠀⠀⠀⠈⣿⣿⠀⠀⠸⣿⡿⠀⠀⠀⠀⠀⠀⠈⠳⣄⠀
⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠈⠁⡴⠶⡆⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠹⡄
⠀⠀⠀⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠒⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷
⠀⠀⠀⠸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠇
⠀⠀⠀⣀⡿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡽⣿⡛⠁⠀
⠀⣠⢾⣭⠀⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠊⠀⢠⣝⣷⡀
⢠⡏⠘⠋⠀⠀⠀⠈⠑⠦⣄⣀⠀⠀⠀⠀⠀⣀⡠⠔⠋⠀⠀⠀⠈⠛⠃⢻
⠈⠷⣤⣀⣀⣀⣀⣀⣀⣀⣀⣤⡽⠟⠛⠿⣭⣄⣀⣀⣀⣀⣀⣀⣀⣀⣤⠞
⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠀⠀⠀
	""")