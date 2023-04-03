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
            name = input("Username: ")
            key = input("Password: ")
            user = db_session.query(User).where(User.username == name).first()
            if user is not None and user.password == key:
                print("Welcome " + name + "!")
                person = User(name, key)
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
        friend = input("Who would you like to follow?\n")
        follow = db_session.query(User).where(User.username == friend).first()
        already_follow = db_session.query(Follower).where((Follower.follower_id == self.user.username) and (Follower.following_id == friend)).first() is not None
        if(already_follow):
            print("You already follow " + friend)
        else:
            following = Follower(self.user.username, follow.username)
            db_session.add(following)
            print("You now follow " + friend)
            db_session.commit()
        
    def unfollow(self):
        unfriend = input("Who would you like to unfollow?\n")
        unfollow =  db_session.query(Follower).where((Follower.follower_id == self.user.username) and (Follower.following_id == unfriend)).first()
        db_session.delete(unfollow)
        print("You no longer follow " + unfriend)
        db_session.commit()


    def tweet(self):
        tweet_text = input("Create Tweet: ")
        tweet_tags = input("Enter your tags seperated by spaces: ")
        tweet = Tweet(tweet_text, datetime.now(), self.user.username)

        db_session.add(tweet)
        tags = tweet_tags.split(" ")
        ids = []
        for tag in tags:
            c = db_session.query(Tag).where(Tag.content == tag).first()
            if c is None:
                new_tag = Tag(tag)
                db_session.add(new_tag)
                db_session.commit()
                c = db_session.query(Tag).where(Tag.content == tag).first()
            ids.append(c.id)
        for id in ids:
                db_session.add(TweetTag(tweet.id, id))
                
        db_session.commit()
        
        
    def view_my_tweets(self):
        my_tweets = db_session.query(Tweet).where(Tweet.username == self.user.username).all()
        self.print_tweets(my_tweets)
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        feed = db_session.query(Tweet).join(Follower, Follower.following_id == Tweet.username).where(Follower.follower_id == self.user.username).order_by(Tweet.timestamp.desc()).limit(5)
        self.print_tweets(feed)

    def search_by_user(self):
        search = input("Whose tweets would you like to view?\n")
        their_tweets = db_session.query(Tweet).where(Tweet.username == search).all()
        self.print_tweets(their_tweets)

    def search_by_tag(self):
        search = input("Which tag would you like to search?\n")
        tag = db_session.query(Tag).where(Tag.content == search).first()
        intermediate = db_session.query(TweetTag).where(TweetTag.tag_id == tag.id).all()
        tag_tweets = []
        for tt in intermediate:
            tag_tweets.append(db_session.query(Tweet).where(Tweet.id == tt.tweet_id).first())
        self.print_tweets(tag_tweets)

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()
        while self.logged_in:
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