from telegram import Update
from telegram.ext import ContextTypes

import time

from database.users import (
    create_user,
    get_balance,
    add_coins,
    get_last_daily,
    set_last_daily
)

# =========================================
# START
# =========================================
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    create_user(user.id)

    await update.message.reply_text(

        "🏏 Welcome to Kricketer Bot!\n\n"

        "Available Commands:\n\n"

        "🎰 Casino Games\n"
        "/flip heads 500\n"
        "/dice 4 500\n"
        "/fly 500 5\n"
        "/bj 500\n\n"

        "🕵️ Imposter Game\n"
        "/startgame\n"
        "/begin\n\n"

        "💰 Economy\n"
        "/wallet\n"
        "/daily"
    )


# =========================================
# WALLET
# =========================================
async def wallet(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    create_user(user.id)

    balance = get_balance(
        user.id
    )

    await update.message.reply_text(

        f"💰 Your Balance:\n\n"

        f"🪙 {balance} coins"
    )


# =========================================
# DAILY
# =========================================
async def daily(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    create_user(user.id)

    current_time = time.time()

    cooldown = 24 * 60 * 60

    last_daily = get_last_daily(
    user.id
)

    # CAN CLAIM
    if current_time - last_daily >= cooldown:

        add_coins(
            user.id,
            1000
        )

        set_last_daily(
    user.id,
    current_time
)

        await update.message.reply_text(

            "🎁 Daily Reward Claimed!\n\n"

            "💰 +1000 coins\n"

            f"🏦 Balance: "
            f"{get_balance(user.id)}"
        )

    # STILL ON COOLDOWN
    else:

        remaining = int(

            cooldown -

            (
                current_time -
                last_daily
            )
        )

        hours = remaining // 3600

        minutes = (
            remaining % 3600
        ) // 60

        await update.message.reply_text(

            "⏳ Daily already claimed\n\n"

            f"Try again in:\n"

            f"{hours}h {minutes}m"
        )