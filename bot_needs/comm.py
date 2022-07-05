from constants.bot import COMM_CIN, COMM_COUT


def BOT_COMM(id, dir, msg, options=None, on_response=None):
    if dir == COMM_CIN:
        if not options or not on_response:
            raise ValueError("comm CIN requires an options list and an on_response callback.")
        
        
        #telegram get input
        pass
    elif dir == COMM_COUT:
        #telegram output
        pass