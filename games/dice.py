from telegram import Update
from telegram.ext import ContextTypes

import random

from database.users import (
    create_user,
    get_balance,
    add_coins,
    remove_coins
)


async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    create_user(user.id)

    if len(context.args) < 2:

        await update.message.reply_text(
            "Usage:\n/dice 4 500"
        )

        return

    try:

        chosen = int(context.args[0])

        amount = int(context.args[1])

    except:

        await update.message.reply_text(
            "Enter valid numbers"
        )

        return

    if chosen < 1 or chosen > 6:

        await update.message.reply_text(
            "Choose a number between 1 and 6"
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

    rolled = random.randint(1, 6)

    # WIN
    if rolled == chosen:

        winnings = amount * 5

        add_coins(
            user.id,
            winnings
        )

        await update.message.reply_text(
            f"🎲 Dice Rolled: {rolled}\n\n"
            f"🎉 YOU WON!\n"
            f"💰 +{winnings} coins\n"
            f"🏦 Balance: {get_balance(user.id)}"
        )

    # LOSE
    else:

        remove_coins(
            user.id,
            amount
        )

        await update.message.reply_text(
            f"🎲 Dice Rolled: {rolled}\n\n"
            f"💀 You Lost {amount} coins\n"
            f"🏦 Balance: {get_balance(user.id)}"
        )