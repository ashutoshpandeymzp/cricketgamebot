from telegram import Update

from telegram.ext import ContextTypes

from database.users import (
    create_user,
    get_balance,
    add_coins,
    remove_coins
)

from database.matchbets import (

    active_matches,

    create_match,

    find_match,

    place_bet,

    close_bets,

    remove_match
)

# =========================================
# BOT ADMINS
# =========================================
BOT_ADMINS = [

    5923479038
]

# =========================================
# CHECK ADMIN
# =========================================
async def is_admin(

    update,
    context

):

    user = update.effective_user

    return user.id in BOT_ADMINS


# =========================================
# OPEN BETS
# =========================================
async def openbets(

    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # ADMIN CHECK
    if not await is_admin(
        update,
        context
    ):

        return

    # ARGUMENTS
    if len(context.args) < 2:

        await update.message.reply_text(

            "Usage:\n"

            "/openbets team1 team2"
        )

        return

    team1 = context.args[0].lower()

    team2 = context.args[1].lower()

    # CHECK EXISTING
    if find_match(team1) or find_match(team2):

        await update.message.reply_text(
            "❌ Match already exists"
        )

        return

    # CREATE MATCH
    create_match(
        team1,
        team2
    )

    await update.message.reply_text(

        f"🏏 Betting Open!\n\n"

        f"Teams:\n"

        f"• {team1}\n"

        f"• {team2}\n\n"

        f"Place bets using:\n"

        f"/bet team amount"
    )


# =========================================
# BET LIST
# =========================================
async def betlist(

    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if len(active_matches) == 0:

        await update.message.reply_text(
            "❌ No active matches"
        )

        return

    text = "🏏 ACTIVE BETS\n\n"

    for match in active_matches:

        if match["open"]:

            text += (

                f"• {match['teams'][0]} "
                f"vs "
                f"{match['teams'][1]}\n"
            )

    await update.message.reply_text(
        text
    )


# =========================================
# PLACE BET
# =========================================
async def bet(

    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    create_user(user.id)

    # ARGUMENTS
    if len(context.args) < 2:

        await update.message.reply_text(

            "Usage:\n"

            "/bet team amount"
        )

        return

    team = context.args[0].lower()

    # AMOUNT
    try:

        amount = int(
            context.args[1]
        )

    except:

        await update.message.reply_text(
            "❌ Invalid amount"
        )

        return

    # VALIDATE
    if amount <= 0:

        await update.message.reply_text(
            "❌ Amount must be greater than 0"
        )

        return

    # FIND MATCH
    match = find_match(team)

    if match is None:

        await update.message.reply_text(
            "❌ No active bet found for that team"
        )

        return

    # BETTING CLOSED
    if not match["open"]:

        await update.message.reply_text(
            "❌ Betting closed"
        )

        return

    # CHECK BALANCE
    balance = get_balance(
        user.id
    )

    if balance < amount:

        await update.message.reply_text(

            f"❌ Not enough balance\n\n"

            f"💰 Balance: {balance}"
        )

        return

    # PLACE BET
    success = place_bet(

        user.id,

        team,

        amount
    )

    if not success:

        await update.message.reply_text(

            "❌ You already placed a bet"
        )

        return

    # REMOVE COINS
    remove_coins(
        user.id,
        amount
    )

    new_balance = get_balance(
        user.id
    )

    await update.message.reply_text(

        f"✅ Bet Placed!\n\n"

        f"🏏 Team: {team}\n"

        f"💰 Amount: {amount}\n\n"

        f"💳 Balance: {new_balance}"
    )


# =========================================
# CLOSE BETS
# =========================================
async def closebets(

    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # ADMIN CHECK
    if not await is_admin(
        update,
        context
    ):

        return

    # ARGUMENTS
    if len(context.args) < 1:

        await update.message.reply_text(

            "Usage:\n"

            "/closebets team"
        )

        return

    team = context.args[0].lower()

    success = close_bets(team)

    if not success:

        await update.message.reply_text(
            "❌ Match not found"
        )

        return

    await update.message.reply_text(

        f"🔒 Betting Closed for {team}"
    )


# =========================================
# RESULT
# =========================================
async def result(

    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # ADMIN CHECK
    if not await is_admin(
        update,
        context
    ):

        return

    # ARGUMENTS
    if len(context.args) < 1:

        await update.message.reply_text(

            "Usage:\n"

            "/result team"
        )

        return

    winning_team = context.args[0].lower()

    match = find_match(
        winning_team
    )

    if match is None:

        await update.message.reply_text(
            "❌ Match not found"
        )

        return

    winners = []

    # PAY WINNERS
    for bet_data in match["bets"]:

        if bet_data["team"] == winning_team:

            winnings = bet_data["amount"] * 2

            add_coins(

                bet_data["user_id"],

                winnings
            )

            winners.append(

                f"• User {bet_data['user_id']} "
                f"won {winnings}"
            )

    text = (

        f"🏆 {winning_team.upper()} WON!\n\n"
    )

    if len(winners) == 0:

        text += "No winners."

    else:

        text += "\n".join(winners)

    await update.message.reply_text(
        text
    )

    # REMOVE MATCH
    remove_match(
        winning_team
    )
