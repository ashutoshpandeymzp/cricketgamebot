import random

from telegram import Update

from telegram.ext import ContextTypes

from database.users import (
    create_user,
    get_balance,
    add_coins,
    remove_coins
)

# =========================================
# AVIATOR GAME
# =========================================
async def fly(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    create_user(user.id)

    # =========================================
    # CHECK ARGUMENTS
    # =========================================
    if len(context.args) < 2:

        await update.message.reply_text(

            "Usage:\n"

            "/fly amount multiplier\n\n"

            "Example:\n"

            "/fly 500 2.5"
        )

        return

    # =========================================
    # GET BET
    # =========================================
    try:

        amount = int(context.args[0])

        target = float(context.args[1])

    except:

        await update.message.reply_text(
            "❌ Invalid amount or multiplier"
        )

        return

    # =========================================
    # VALIDATE
    # =========================================
    if amount <= 0:

        await update.message.reply_text(
            "❌ Bet must be greater than 0"
        )

        return

    if target < 1.01:

        await update.message.reply_text(
            "❌ Multiplier too low"
        )

        return

    # =========================================
    # CHECK BALANCE
    # =========================================
    balance = get_balance(user.id)

    if balance < amount:

        await update.message.reply_text(

            f"❌ Not enough balance\n\n"

            f"💰 Balance: {balance}"
        )

        return

    # =========================================
    # REMOVE BET
    # =========================================
    remove_coins(
        user.id,
        amount
    )

    # =========================================
    # WEIGHTED CRASH SYSTEM
    # =========================================

    chance = random.randint(1, 100)

    # 50% UNDER 2x
    if chance <= 50:

        crash = round(
            random.uniform(1.00, 1.99),
            2
        )

    # 30% BETWEEN 2x-3x
    elif chance <= 80:

        crash = round(
            random.uniform(2.00, 3.00),
            2
        )

    # 10% BETWEEN 3x-10x
    elif chance <= 90:

        crash = round(
            random.uniform(3.00, 10.00),
            2
        )

    # 10% ABOVE 10x
    else:

        crash = round(
            random.uniform(10.00, 50.00),
            2
        )

    # =========================================
    # WIN
    # =========================================
    if crash >= target:

        # PURE PROFIT
        profit = int(
            amount * (target - 1)
        )

        # RETURN BET + PROFIT
        add_coins(
            user.id,
            amount + profit
        )

        new_balance = get_balance(
            user.id
        )

        # BIG FLIGHT
        if crash >= 10:

            await update.message.reply_text(

                f"🔥 MASSIVE FLIGHT!\n\n"

                f"✈️ Crashed at: {crash}x\n"

                f"🎯 Your Cashout: {target}x\n\n"

                f"✅ Profit: {profit} coins\n\n"

                f"💰 Balance: {new_balance}"
            )

        # NORMAL WIN
        else:

            await update.message.reply_text(

                f"✈️ Plane Flew to {crash}x\n\n"

                f"🎯 Your Cashout: {target}x\n\n"

                f"✅ Profit: {profit} coins\n\n"

                f"💰 Balance: {new_balance}"
            )

    # =========================================
    # LOSS
    # =========================================
    else:

        new_balance = get_balance(
            user.id
        )

        await update.message.reply_text(

            f"💥 Plane Crashed at {crash}x\n\n"

            f"❌ You lost {amount} coins\n\n"

            f"💰 Balance: {new_balance}"
        )
