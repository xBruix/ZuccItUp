/**
 * Authors: Caleb Bronn
 * Last update: 22 Feb 2026

 * header file for Database Server
 */

#ifndef SERVER_H
#define SERVER_H

#include <occi.h>  // main header for Oracle Call Interface
	using namespace oracle::occi;
#include <bits/stdc++.h>	// for vector
#include <iostream>
#include <string>
	using namespace std;


/**
 * ServerException is a very simple exception class that is thrown 
 * when something goes wrong in the Server. All the implementation
 * for this class is done inline.
 */
class ServerException {
private:
	string location;
	string message;
	
public:

	/**
 	* Creates a ServerException object.
 	* @param where_thrown The origin of the member function that threw the exception.
 	* @param msg An indication of what the problem was that triggered the exception.
 	*/
	ServerException(const string& where_thrown, const string& msg) {
		location = where_thrown;
		message = msg;
	}

	/** 
	 * Provides a string version of the ServerException object.
	 * @return A debug message providing you with the location and a description of the 
	 * problem.
 	*/
	string to_string() const {
		return "*** ServerException in "+ location + ": "+ message;
	}

	/**
 	* Allows for a direct stream of the error message using the << operator.
 	* @param out The ostream object.
 	* @param he The ServerException to pass into the output stream.
 	* @return The ostream object that will print the debug info to the console.
 	*/
 	friend ostream& operator << (ostream& out, const ServerException& e) {
 		out << e.to_string();
		return out;
	}
}; // end of ServerException


/**
 * @brief Server class that connects to the database and manages database queries
 */
class Server {
private:
	Environment* env;	// Oracle environment
	Connection* conn;	// used to establish connection with database

	// Location of the Oracle database on CSCI servers
	const string DB_ADDRESS = "sunfire.csci.viu.ca";

	// Prepared SQL queries go here
		// e.g. string create_account_sql;
	string insert_order_sql;
	string insert_menu_sql;

	// Prepared query statements go here
		// e.g. Statement* create_account_query;
	Statement* insert_order_query;
	Statement* insert_menu_query;

public:
	Server();	// constructor
	~Server();	// destructor

	/**
	 * @brief Connect to the database
	 * @param username Your username on Oracle
	 * @param password Your Oracle password
	 */
	bool connect(const string username, const string password);

	void createTable(const string& table_name);

	void dropTable(const string& table_name);

	//void insertOrder(const string& custName, const string& items,const string& destination);

	void insertMenu(const string& name, const string& description, double price);

	void populateMenu();

	void displayTable(const string& table_name);

	void insertOrder(const string& custName, const string& items,const string& destination);
};



#endif