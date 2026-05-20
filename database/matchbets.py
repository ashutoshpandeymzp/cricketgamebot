# =========================================
# ACTIVE MATCHES
# =========================================

active_matches = []


# =========================================
# CREATE MATCH
# =========================================
def create_match(

    team1,
    team2
):

    match = {

        "teams": [

            team1.lower(),

            team2.lower()
        ],

        "open": True,

        "bets": []
    }

    active_matches.append(
        match
    )


# =========================================
# FIND MATCH
# =========================================
def find_match(team):

    team = team.lower()

    for match in active_matches:

        if team in match["teams"]:

            return match

    return None


# =========================================
# PLACE BET
# =========================================
def place_bet(

    user_id,
    team,
    amount
):

    match = find_match(team)

    if match is None:

        return False

    # CHECK CLOSED
    if not match["open"]:

        return False

    # PREVENT DOUBLE BET
    for bet in match["bets"]:

        if bet["user_id"] == user_id:

            return False

    match["bets"].append({

        "user_id": user_id,

        "team": team.lower(),

        "amount": amount
    })

    return True


# =========================================
# CLOSE BETS
# =========================================
def close_bets(team):

    match = find_match(team)

    if match is None:

        return False

    match["open"] = False

    return True


# =========================================
# REMOVE MATCH
# =========================================
def remove_match(team):

    match = find_match(team)

    if match is None:

        return False

    active_matches.remove(
        match
    )

    return True
