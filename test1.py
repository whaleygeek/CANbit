# test1.py  04/11/2016  D.J.Whale

import microbit #will auto connect

# testing

f = open("log.txt", "w")

while True:
    msg = microbit.get_next_message()
    if msg is not None:
        # Don't log RX messages to screen
        if not msg.startswith("RX,"):
            print(msg)
            
        # But do log RX messages to file
        f.write(msg + '\n')
        f.flush()

# END
