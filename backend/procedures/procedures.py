########################################################################################################################
# This file contains the main procedures to initialize and update the data present in the database
#####
# Since there will only ever be one database we have to connect to, the database connection can be build in here.
########################################################################################################################

def do(update: bool = True):
    # TODO: create connection to the database
    if update:
        #  The update procedure shall be triggered.
        #  This means, we only have to get data newer than out last entry
        pass
    else:
        # the initialization procedure shall be triggered.
        #
        pass


    pass


def init():
    pass


def update():
    pass

