from telegram import Update
from telegram.ext import ContextTypes

import random

from database.users import (
    create_user,
    get_balance,
    add_coins,
    remove_coins
)


async def flip(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    create_user(user.id)

    if len(context.args) < 2:

        await update.message.reply_text(
            "Usage:\n/flip heads 500"
        )

        return

    choice = context.args[0].lower()

    try:

        amount = int(context.args[1])

    except:

        await update.message.reply_text(
            "Enter valid amount"
        )

        return

    if choice not in ["heads", "tails"]:

        await update.message.reply_text(
            "Choose heads or tails"
        )

        return

    if get_balance(user.id) < amount:

        await update.message.reply_text(
            "❌ Not enough coins"
        )

        return

    result = random.choice([
        "heads",
        "tails"
    ])

    if result == choice:

        add_coins(user.id, amount)

        await update.message.reply_text(
            f"🪙 Result: {result}\n\n"
            f"🎉 Won {amount} coins\n"
            f"🏦 Balance: {get_balance(user.id)}"
        )

    else:

        remove_coins(user.id, amount)

        await update.message.reply_text(
            f"🪙 Result: {result}\n\n"
            f"💀 Lost {amount} coins\n"
            f"🏦 Balance: {get_balance(user.id)}"
        )