def decide(handtotal, softhand):
    if softhand:
        # soft
        if handtotal <= 17:
            return "HIT"
        else:
            return "STAND"
    else:
        # hard
        if handtotal <= 16:
            return "HIT"
        else:
            return "STAND"