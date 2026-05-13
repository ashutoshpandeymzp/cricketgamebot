from telegram import Update
from telegram.ext import ContextTypes

from database.users import (
    create_user,
    add_coins,
    remove_coins,
    get_balance
)

# =========================================
# YOUR TELEGRAM ID
# =========================================
ADMIN_ID = 5923479038


# =========================================
# CHECK ADMIN
# =========================================
def is_admin(user_id):

    return user_id == ADMIN_ID


# =========================================
# ADD COINS
# =========================================
async def addcoins(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    if not is_admin(user.id):

        return

    if len(context.args) < 2:

        await update.message.reply_text(
            "Usage:\n/addcoins userid amount"
        )

        return

    target_id = int(context.args[0])

    amount = int(context.args[1])

    create_user(target_id)

    add_coins(
        target_id,
        amount
    )

    await update.message.reply_text(

        f"✅ Added {amount} coins\n"

        f"💰 New Balance: "
        f"{get_balance(target_id)}"
    )


# =========================================
# REMOVE COINS
# =========================================
async def removecoins(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    if not is_admin(user.id):

        return

    if len(context.args) < 2:

        await update.message.reply_text(
            "Usage:\n/removecoins userid amount"
        )

        return

    target_id = int(context.args[0])

    amount = int(context.args[1])

    create_user(target_id)

    remove_coins(
        target_id,
        amount
    )

    await update.message.reply_text(

        f"❌ Removed {amount} coins\n"

        f"💰 New Balance: "
        f"{get_balance(target_id)}"
    )