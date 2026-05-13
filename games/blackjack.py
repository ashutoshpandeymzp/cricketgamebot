from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import ContextTypes

import random

from database.users import (
    create_user,
    get_balance,
    add_coins,
    remove_coins
)

# STORE ACTIVE BLACKJACK GAMES
blackjack_games = {}


# =========================================
# START BLACKJACK
# =========================================
async def bj(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    create_user(user.id)

    if len(context.args) < 1:

        await update.message.reply_text(
            "Usage:\n/bj 500"
        )

        return

    try:

        amount = int(context.args[0])

    except:

        await update.message.reply_text(
            "Enter valid amount"
        )

        return

    if amount <= 0:

        await update.message.reply_text(
            "Amount must be greater than 0"
        )

        return

    if get_balance(user.id) < amount:

        await update.message.reply_text(
            "❌ Not enough coins"
        )

        return

    player = random.randint(4, 12)

    dealer = random.randint(4, 12)

    blackjack_games[user.id] = {

        "player": player,
        "dealer": dealer,
        "bet": amount
    }

    keyboard = [
        [
            InlineKeyboardButton(
                "🃏 Hit",
                callback_data="hit"
            ),

            InlineKeyboardButton(
                "✋ Stay",
                callback_data="stay"
            ),

            InlineKeyboardButton(
                "💰 Double",
                callback_data="double"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(
        keyboard
    )

    await update.message.reply_text(
        f"🃏 Blackjack Started\n\n"
        f"Your Score: {player}\n"
        f"Dealer Score: {dealer}",
        reply_markup=reply_markup
    )


# =========================================
# BLACKJACK BUTTONS
# =========================================
async def blackjack_buttons(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user = query.from_user

    if user.id not in blackjack_games:

        return

    game = blackjack_games[user.id]

    player = game["player"]

    dealer = game["dealer"]

    bet = game["bet"]

    action = query.data

    # =====================================
    # HIT
    # =====================================
    if action == "hit":

        new_card = random.randint(1, 10)

        player += new_card

        game["player"] = player

        # BUST
        if player > 21:

            remove_coins(
                user.id,
                bet
            )

            await query.edit_message_text(
                f"🃏 Drew: {new_card}\n\n"
                f"💥 Bust!\n"
                f"Your Score: {player}\n\n"
                f"💀 Lost {bet} coins\n"
                f"🏦 Balance: {get_balance(user.id)}"
            )

            del blackjack_games[user.id]

        else:

            keyboard = [
                [
                    InlineKeyboardButton(
                        "🃏 Hit",
                        callback_data="hit"
                    ),

                    InlineKeyboardButton(
                        "✋ Stay",
                        callback_data="stay"
                    ),

                    InlineKeyboardButton(
                        "💰 Double",
                        callback_data="double"
                    )
                ]
            ]

            reply_markup = InlineKeyboardMarkup(
                keyboard
            )

            await query.edit_message_text(
                f"🃏 Drew: {new_card}\n\n"
                f"Your Score: {player}\n"
                f"Dealer Score: {dealer}",
                reply_markup=reply_markup
            )

    # =====================================
    # STAY
    # =====================================
    elif action == "stay":

        # DEALER MUST HIT BELOW 17
        while dealer < 17:

            dealer += random.randint(1, 10)

        # DEALER BUST
        if dealer > 21:

            add_coins(
                user.id,
                bet
            )

            result = (
                f"🎉 Dealer Busted!\n"
                f"💰 Won {bet} coins"
            )

        # PLAYER WINS
        elif player > dealer:

            add_coins(
                user.id,
                bet
            )

            result = (
                f"🎉 You Won!\n"
                f"💰 Won {bet} coins"
            )

        # DEALER WINS
        elif player < dealer:

            remove_coins(
                user.id,
                bet
            )

            result = (
                f"💀 You Lost!\n"
                f"Lost {bet} coins"
            )

        # DRAW
        else:

            result = "🤝 Draw"

        await query.edit_message_text(
            f"🃏 Final Result\n\n"
            f"Your Score: {player}\n"
            f"Dealer Score: {dealer}\n\n"
            f"{result}\n\n"
            f"🏦 Balance: {get_balance(user.id)}"
        )

        del blackjack_games[user.id]

    # =====================================
    # DOUBLE
    # =====================================
    elif action == "double":

        if get_balance(user.id) < bet * 2:

            await query.answer(
                "Not enough coins",
                show_alert=True
            )

            return

        game["bet"] *= 2

        new_card = random.randint(1, 10)

        player += new_card

        game["player"] = player

        while dealer < 17:

            dealer += random.randint(1, 10)

        # PLAYER BUST
        if player > 21:

            remove_coins(
                user.id,
                game["bet"]
            )

            result = (
                f"💥 Bust!\n"
                f"💀 Lost {game['bet']} coins"
            )

        # DEALER BUST
        elif dealer > 21:

            add_coins(
                user.id,
                game["bet"]
            )

            result = (
                f"🎉 Dealer Busted!\n"
                f"💰 Won {game['bet']} coins"
            )

        # PLAYER WIN
        elif player > dealer:

            add_coins(
                user.id,
                game["bet"]
            )

            result = (
                f"🎉 You Won!\n"
                f"💰 Won {game['bet']} coins"
            )

        # DEALER WIN
        else:

            remove_coins(
                user.id,
                game["bet"]
            )

            result = (
                f"💀 You Lost!\n"
                f"Lost {game['bet']} coins"
            )

        await query.edit_message_text(
            f"💰 Double Activated\n\n"
            f"Your Score: {player}\n"
            f"Dealer Score: {dealer}\n\n"
            f"{result}\n\n"
            f"🏦 Balance: {get_balance(user.id)}"
        )

        del blackjack_games[user.id]