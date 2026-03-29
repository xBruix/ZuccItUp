from server import Server
from menu import Menu
from order import Order
from user import User, Customer, DeliveryAgent, Vendor
from getpass import getpass		# for typing password without showing letters
import sys						# to exit program
import re						# for regex


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
		user.logout()
		print("You have successfully logged out!")
		# Not sure what should happen now?
		return answer
	else:
		return answer

def input_str(msg: str, regex_pattern: str = None) -> str:
	"""
	Gets string input and checks if the user typed "quit" or "logout".
	:param msg: The message you want to display to the user
	:param regex_pattern: (optional) A regex string to match the user input to.
	:return: the user's input
	"""

	# If any string input is acceptable, simply return the user's answer after checking for quit or logout
	if regex_pattern is None:
		return check_logout_or_quit(input(msg))

	# Else, we need to check if the answer is valid -- i.e. that it matches regex_pattern
	matching = True
	answer = ""
	while not matching:
		answer = check_logout_or_quit(input(msg))
		matching = re.match(regex_pattern, answer)
		if not matching:
			print("Sorry, that was not a valid answer. Please try again.")
	return answer

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
		signin_option = input_int("Please select an option:\n1. Login (type 1)\n2. Signup (type 2)\n> ", 1, 2)

		if signin_option == 1:		# Login
			your_viu_id = input_str("Please enter your VIU ID number\n> ")
			your_password = getpass("Please enter your password\n> ")
			not_signed_in = not user.login(your_viu_id, your_password)
			if not_signed_in:
				print("Sorry, those login details were incorrect. Please try again.")
		else:				# Signup
			print("Let's get you started!")
			signin_option = input_int("Choose a role:\n1. Customer\n2. Delivery Agent", 1, 2)
			your_role = "Customer" if signin_option == 1 else "Agent"
			your_viu_id = input_str("Please enter your VIU ID number\n> ")
			your_password = getpass("Please enter a password\n> ")
			your_name = input_str("Please enter your name\n> ")
			your_email = input_str("Please enter your email address\n> ")
			not_signed_in = not user.signup(viu_id=your_viu_id, passwd=your_password, name=your_name, email=your_email, role=your_role)
			if not_signed_in:
				print("Sorry, something went wrong. Please try again.")
# end login_or_signup


# MAIN LOOP GOES HERE
print("Welcome to Zucc It Up!")
print("At any time, you can type 'quit' to close the program, or type 'logout' to logout of your account.")
login_or_signup()

if user.get_role() == "Customer":
	# TODO: Enter Location (user location)
	your_building = input_str("Enter your building number\n> ", "^[1-4]\\d\\d$")
	your_room = input_str("Enter your room number\n> ", "^[1-5]\\d\\d\\w?$")

	# TODO: List options
	customer_option = input_str("What do you want to do?\n1. Create an Order \n2. View Your Cart")
	if customer_option == 1:	# Create an Order
		# TODO: List vendors
		# TODO: Customer selects vendor
		# TODO: List menus for that vendor
		# TODO: Customer selects a menu
		# TODO: List menu items from that menu
		pass
	else:						# View your cart
		pass

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