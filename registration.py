import hashlib


class Enter:

    def __init__(self, input_user, users):
        self.nickname = input_user[0]
        self.password = hashlib.sha256(input_user[1].encode()).hexdigest()
        self.users = users

    def enter(self):
        if self.nickname in self.users:
            if self.password == self.users[self.nickname]:
                return True
            else:
                return "Wrong Password"
        else:
            return "User isn't registrated"


Users = {}
