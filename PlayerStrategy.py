def decide(handtotal, softhand, opponentcard):
    if opponentcard[:-1] == "A":
        opponentvalue = 11
    elif opponentcard[:-1] in ["J", "Q", "K"]:
        opponentvalue = 10
    else:
        opponentvalue = int(opponentcard[:-1])
    if softhand:
        # softhand logic
        # HAND TOTAL IS BETWEEN 12 AND 21
        if handtotal <= 17:
            return "HIT"
        elif handtotal >= 19:
            return "STAND"
        else:
            if opponentvalue <= 8:
                return "STAND"
            else:
                return "HIT"
    else:
        # hardhand logic
        # HAND TOTAL IS BETWEEN 4 AND 21
        if handtotal <= 11:
            return "HIT"
        elif handtotal == 12:
            if 4 <= opponentvalue <= 6:
                return "STAND"
            else:
                return "HIT"
        elif 13 <= handtotal <= 16:
            if opponentvalue <= 6:
                return "STAND"
            else:
                return "HIT"
        else:
            return "STAND"
