class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.friends = 0

    def add_friend(self, user):
        self.friends += 1
        user.friends += 1


user1 = User("001", "Wolf")
user2 = User("002", "Fox")

user1.add_friend(user2)
print(user2.friends)
