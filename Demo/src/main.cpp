/**
 * Authors: Caleb Bronn
 * Last update: 22 Feb 2026

 * Main file for user interaction, command-line interface, and Server instance
 */

/* 
TODO: Enter location
TODO: List vendors
TODO: Select Vendor
TODO: Menu
TODO: Loop
	TODO: Add to Cart
	TODO: Evaluate subtotal
TODO: Place order
TODO: Confirm order or decline and try again
*/

#include "../include/server.hpp"
#include <unistd.h>		// for getpass()
#include <ctype.h>		// for toupper() and tolower()
#include <cstdlib>		// for exit()
#include <limits.h>		// for INT_MIN and INT_MAX
#include <iostream>
#include <string>
using namespace std;

// Global Server
Server svr;

// Declaration for main loop options
int options();

/*******************************
 * USER INPUT HELPER FUNCTIONS *
 *******************************/

// Convert string to lowercase
string to_lower(string s) {
	for (int i = 0; i < s.length(); i++) {
		s[i] = tolower(s[i]);
	}
	return s;
}

// Convert string to uppercase
string to_upper(string s) {
	for (int i = 0; i < s.length(); i++) {
		s[i] = toupper(s[i]);
	}
	return s;
}

// Get input from user and check if user types "q" to quit the program.
string input_str(const string msg) {
	string input = "";
	cout << msg;
	getline(cin, input);
	if (to_lower(input) == "q") {
		cout << "Goodbye!" << endl;
		exit(0);
	}
	return input;
}

// Get password from user
string input_password(const char* msg) {
	return string(getpass(msg));
}

// Get double from user
double input_double(const string msg, const double min, const double max) {
	double answer = 0.0;
	string throwaway;
	cout << msg;

	// cin has a flag that reads as false if the user input is not of the correct data type.
	// We exploit that flag in this while loop. Credit to Prof. Bette Bultena for showing me 
	// this trick in CSCI 159!
	while (!(cin >> answer) || answer < min || answer > max) {
		// Clear out the buffer
		cin.clear();
		getline(cin, throwaway);

		// Quit if user types 'Q'
		if (to_lower(throwaway) == "q") {
			cout << "Goodbye!" << endl;
			exit(0);
		}
		cout << "\nSorry, that was not a valid input. Please try again\n> ";
	}
	// Clean out buffer again. Just in case.
	cin.clear();
	getline(cin, throwaway);
	return answer;
}


// Get int from user
int input_int(const string msg, const int min = INT_MIN, const int max = INT_MAX) {
	int answer;
	string throwaway;
	cout << msg;

	// If the user does not input an integer, prompt them to try again.
	// Or if the user enters an interger that's not between the min and max,
	// prompt to try again.
	while (!(cin >> answer) || answer < min || answer > max) {
		// Clean out cin and the buffer.
		cin.clear();
		getline(cin, throwaway);

		// Quit if user types 'Q'
		if (to_lower(throwaway) == "q") {
			cout << "Goodbye!" << endl;
			exit(0);
		}
		cout << "Sorry, that was not a valid integer. Please try again\n> ";
	}
	// Clean out buffer again. Just in case.
	cin.clear();
	getline(cin, throwaway);
	return answer;
}


int main() {
	cout << "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠶⠚⠋⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
	<< "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠶⠋⠀⣀⣀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
	<< "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠤⠞⠁⠀⠀⣴⠃⣼⠀⠀⣰⡇⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠐⠒⠒⠒⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀\n"
	<< "⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠚⠉⠀⡄⠀⠀⠀⢸⣿⣿⡿⠀⠀⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠲⡄⠀⠀⠀⠀⠀\n"
	<< "⠀⠀⠀⠀⠀⠀⠀⢠⠏⠁⠀⠀⡰⠁⠀⣀⡀⢸⣿⣿⠇⠀⠀⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣄⠀⠀⠱⡀⠀⠀⠀⠀\n"
	<< "⠀⠀⠀⠀⠀⠀⢀⡟⠀⠀⣀⡀⡀⠀⢾⣯⣭⠟⠉⢋⣀⣀⣀⡨⠍⠁⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠲⠯⢭⣅⣈⡀⠀⠀⠱⡄⠀⠀⠀\n"
	<< "⠀⠀⠀⠀⠀⢀⡾⠀⠀⠒⢺⢀⡇⠀⠀⠀⠀⠀⠀⠈⠻⠿⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⡄⠀⠀⠀⠀⠀⠀⠀⠱⡄⠀⠀\n"
	<< "⠀⠀⠀⠀⣠⠞⠁⠀⠀⠀⠈⡎⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣶⡄⠀⠀⠀⠀⠀⠀⠙⣆⠀\n"
	<< "⠀⠀⢠⡞⠁⠀⢷⣄⠀⣴⣾⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠃⠙⢶⣤⡀⠀⠀⠀⠀⠘⠀\n"
	<< "⠀⠀⣾⠃⠀⠀⣈⣻⣿⣿⠟⠁⠹⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠏⠀⠀⠀⢹⡏⢦⠀⠀⠀⠀⠀\n"
	<< "⠀⢠⡏⠀⠀⣰⣿⢠⣾⠟⠀⠀⠀⠘⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⡴⠋⠀⠀⠀⠀⠈⠻⣿⡄⠀⠀⠀⠀\n"
	<< "⠀⡼⠀⠀⢰⣿⠿⠛⠁⠀⠀⠀⠀⠀⠈⣿⠷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠖⠋⠉⠁⢸⡁⠀⠀⠀⠀⠀⠀⠀⣠⠃⠀⠀⠀⠀\n"
	<< "⢠⡇⠀⠀⠈⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠉⠛⠶⣦⣤⣀⣀⣶⣤⠞⠋⠁⠀⠀⠀⠀⠘⡇⠀⠀⠀⠀⠀⠀⣸⣿⢦⣤⡀⠀⠀\n"
	<< "⢸⣴⠀⣤⢶⣿⠀⠀⠀⠀⠀⠀⠀⠀⢰⠿⡆⠀⠀⠀⠀⠀⠈⣽⡟⠛⣧⡀⠀⠸⡄⠀⠀⠀⢀⡇⠀⠀⠀⠀⠀⠀⠹⣧⣴⠟⢇⢀⣀\n"
	<< "⠘⣯⣜⠁⠘⠿⠀⠀⠀⠀⠀⠀⠀⠀⠸⡄⣿⣄⠀⠀⠀⠀⣠⡿⠀⠀⠘⣷⡄⠀⠹⡆⠀⢀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣾⠟\n"
	<< "⠀⠹⣿⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣟⣿⣧⡄⠀⢰⡿⠁⠀⠀⠀⠘⣷⣀⣠⢷⣽⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀\n"
	<< "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡛⠻⣿⣶⣿⠃⠀⠀⠀⠀⠀⠘⣿⣏⢀⣤⣼⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
	<< "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣟⡶⣮⣽⡏⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⡶⠟⢱⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
	<< "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠿⠛⠛⠙⡄⠀⠀⠀⠀⠀⠀⣰⠿⣟⠉⠀⠈⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
	<< "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣧⠀⠀⠀⢀⣵⠀⠀⠀⠀⠀⠀⢿⠀⢸⡀⠀⢸⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
	<< "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣏⠀⠀⢠⣼⠏⠀⠀⠀⠀⠀⠀⠈⢿⣄⠃⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
	<< "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⣾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
	<< "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣷⣶⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⡛⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
	<< "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣼⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣷⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n";
	cout << "\nWelcome to Zucc It Up!\n\n";

	//* Get credentials for Oracle database
	cout << "First, you will need to enter your Oracle Database credentials.\n";
	cout << "Type 'Q' at any time to quit the program.\n";
	string oracle_username;
	string oracle_password;
	do {
		oracle_username = input_str("Enter Oracle username: ");
		oracle_password = input_password("Enter Oracle password: ");
	   } while (!svr.connect(oracle_username, oracle_password));
	cout << "Credentials verified!\n";;

	svr.dropTable("orders"); //drops tables
	svr.dropTable("menu");

	svr.createTable("orders"); //Creates initial tables
	svr.createTable("menu");

	svr.populateMenu();	//populates menu to have 3 options

	while(options() != 4){ //displays menu till user wants to quit
	}

	svr.dropTable("orders"); //drops tables
	svr.dropTable("menu");
	return 0;
}

//prompts user for input and displays options
int options (){
	string name, item, location, arg_str;

	cout << "Enter number to select option \n";
	cout << "1 View menu\n";
	cout << "2 View orders\n";
	cout << "3 Make orders\n";
	cout << "4 Quit\n";

	int arg = input_int("> ", 1, 4);

	if (arg == 1) {
		svr.displayTable("menu");
	} else if (arg == 2) {
		svr.displayTable("orders");
	} else if (arg == 3) {
		//insert order
		name = input_str("Enter your name: ");

		item = input_str("Enter item you wish to order (for multiple separate by comma): ");

		location = input_str("Enter building number: ");

		try {
			svr.insertOrder(name, item, location);
		} catch (const ServerException& e) {
			cout << e << endl;
		}
	} else if (arg == 4) {
		cout << " Closing...Goodbye\n";
		return 4;
	}

	return 0;
}
