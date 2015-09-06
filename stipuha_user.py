import csv

class StipuhaUser:

    _users = None

    # User states
    INIT = 0
    GETTING_STIPUHA = 10
    WITH_STIPUHA = 20
    ALL_STATES = [INIT, GETTING_STIPUHA, WITH_STIPUHA]

    FILE = "stipuha_users.csv"
    USER_ID_FIELD = "user_id"
    STIPUHA_FIELD = "stipuha"
    STATE_FIELD = "state"

    @staticmethod
    def load_users_from_disk(filename):
        StipuhaUser._users = dict()
        with open(filename, 'r+') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                StipuhaUser._users[row[StipuhaUser.USER_ID_FIELD]] = \
                    StipuhaUser(user_id=row[StipuhaUser.USER_ID_FIELD],
                                state=int(row[StipuhaUser.STATE_FIELD]),
                                stipuha=int(row[StipuhaUser.STIPUHA_FIELD]))

    @staticmethod
    def write_users_to_disk(filename):
        if StipuhaUser._users is None:
            return
        with open(filename, 'w+') as csvfile:
            writer = csv.DictWriter(csvfile,  fieldnames=[StipuhaUser.USER_ID_FIELD,
                                                          StipuhaUser.STATE_FIELD,
                                                          StipuhaUser.STIPUHA_FIELD])
            writer.writeheader()
            for user in StipuhaUser._users.iteritems():
                writer.writerow({StipuhaUser.USER_ID_FIELD: user[0],
                                 StipuhaUser.STATE_FIELD: user[1].get_state(),
                                 StipuhaUser.STIPUHA_FIELD: user[1].get_stipuha()})

    @staticmethod
    def get_user_by_id(user_id):
        if StipuhaUser._users is None:
            StipuhaUser.load_users_from_disk(StipuhaUser.FILE)
        if user_id not in StipuhaUser._users:
            StipuhaUser._users[user_id] = StipuhaUser(user_id)
        return StipuhaUser._users[user_id]

    def __init__(self, user_id, state=INIT, stipuha=0):
        self._stipuha = stipuha
        self._user_id = user_id
        self._state = state

    def set_stipuha(self, stipuha):
        if isinstance(stipuha, (int, long)):
            self._stipuha = stipuha

    def get_stipuha(self):
        return self._stipuha

    def get_user_id(self):
        return self._user_id

    def get_state(self):
        return self._state

    def set_state(self, state):
        if state in StipuhaUser.ALL_STATES:
            self._state = state



