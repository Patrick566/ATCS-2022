from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
    def __init__(self, user=None, logged_in=False):
        self.user = user
        self.logged_in = logged_in
    """
    The menu to print once a user has logged in
    """
    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    def print_startup(self):
        print("Please select a menu option:")
        print("1. Login")
        print("2. Register User")
        print("0. Exit")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self):
        while(self.logged_in != True):
            username = input("What will your twitter handle be?\n")
            password = input("Enter a password:\n")
            password2 = input("Re-enter password:\n")
            other_user = db_session.query(User).where(User.username == username).first()
            if(password != password2):
                print("Those passwords don't match. Try again.\n\n")
            elif(other_user != None):
                print("That usernae is already taken. Try again.\n")
            else:
                person = User(username, password)
                print(person)
                self.user = person
                self.logged_in = True
                db_session.add(person)
                db_session.commit()
                print("\nWelcome " + username + "!")
                

    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        while(self.logged_in != True):
            username = input("Username: ")
            password = input("Password: ")
            user = db_session.query(User).where(User.username == username).first()
            if user is not None and user.password == password:
                print("Welcome " + username + "!")
                person = User(username, password)
                self.user = person
                self.logged_in = True
            else:
                print("Invalid username or password\n")

    
    def logout(self):
        self.user = None
        self.logged_in = False
        self.end()
        

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        self.print_startup()
        option = int(input(""))
        if(option == 1):
            self.login()
        elif(option == 2):
            self.register_user()
        else:
            self.logout()


    def follow(self):
        f = input("Who would you like to follow?\n")
        follow = db_session.query(User).where(User.username == f).first()
        id = self.user
        following = Follower(id.id follow.id)

    def unfollow(self):
        pass

    def tweet(self):
        pass
    
    def view_my_tweets(self):
        pass
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        pass

    def search_by_user(self):
        pass

    def search_by_tag(self):
        pass

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()
        if self.logged_in:
            self.print_menu()
            option = int(input(""))
            if option == 1:
                self.view_feed()
            elif option == 2:
                self.view_my_tweets()
            elif option == 3:
                self.search_by_tag()
            elif option == 4:
                self.search_by_user()
            elif option == 5:
                self.tweet()
            elif option == 6:
                self.follow()
            elif option == 7:
                self.unfollow()
            else:
                self.logout()
        
