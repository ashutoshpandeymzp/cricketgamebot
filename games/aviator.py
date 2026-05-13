from telegram import Update
from telegram.ext import ContextTypes

import random

from database.users import (
    create_user,
    get_balance,
    add_coins,
    remove_coins
)


async def fly(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    create_user(user.id)

    if len(context.args) < 2:

        await update.message.reply_text(
            "Usage:\n/fly 500 5"
        )

        return

    try:

        amount = int(context.args[0])

        target = float(context.args[1])

    except:

        await update.message.reply_text(
            "Enter valid input"
        )

        return

    if amount <= 0:

        await update.message.reply_text(
            "Bet amount must be greater than 0"
        )

        return

    if target < 1.1:

        await update.message.reply_text(
            "Multiplier must be at least 1.1x"
        )

        return

    if get_balance(user.id) < amount:

        await update.message.reply_text(
            "❌ Not enough coins"
        )

        return

    crash = round(
        random.uniform(1.1, 10.0),
        2
    )

    # WIN
    if target < crash:

        winnings = int(amount * target)

        add_coins(
            user.id,
            winnings
        )

        await update.message.reply_text(
            f"✈️ Plane Flew Till: {crash}x\n\n"
            f"🎉 Cashed Out at {target}x\n"
            f"💰 Won {winnings} coins\n"
            f"🏦 Balance: {get_balance(user.id)}"
        )

    # LOSE
    else:

        remove_coins(
            user.id,
            amount
        )

        await update.message.reply_text(
            f"💥 Plane Crashed at {crash}x\n\n"
            f"💀 Lost {amount} coins\n"
            f"🏦 Balance: {get_balance(user.id)}"
        )