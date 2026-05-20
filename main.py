import os

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

# =========================================
# PROFILE SYSTEM
# =========================================
from games.profile import (
    start,
    wallet,
    daily
)

# =========================================
# CASINO GAMES
# =========================================
from games.flip import flip

from games.dice import dice

from games.aviator import fly

from games.blackjack import (
    bj,
    blackjack_buttons
)

# =========================================
# IMPOSTER GAME
# =========================================
from games.imposter import (
    startgame,
    join_button,
    leave_button,
    start_button,
    auto_hint,
    vote_button
)

# =========================================
# BETTING SYSTEM
# =========================================
from games.betting import (

    openbets,

    bet,

    closebets,

    result,

    betlist
)

# =========================================
# ADMIN COMMANDS
# =========================================
from games.admin import (
    addcoins,
    removecoins
)

# =========================================
# BOT TOKEN
# =========================================
TOKEN = os.getenv(
    "BOT_TOKEN"
)

# =========================================
# CREATE APP
# =========================================
app = ApplicationBuilder().token(
    TOKEN
).build()

# =========================================
# PROFILE COMMANDS
# =========================================
app.add_handler(
    CommandHandler(
        "start",
        start
    )
)

app.add_handler(
    CommandHandler(
        "wallet",
        wallet
    )
)

app.add_handler(
    CommandHandler(
        "daily",
        daily
    )
)

# =========================================
# ADMIN COMMANDS
# =========================================
app.add_handler(
    CommandHandler(
        "addcoins",
        addcoins
    )
)

app.add_handler(
    CommandHandler(
        "removecoins",
        removecoins
    )
)

# =========================================
# CASINO COMMANDS
# =========================================
app.add_handler(
    CommandHandler(
        "flip",
        flip
    )
)

app.add_handler(
    CommandHandler(
        "dice",
        dice
    )
)

app.add_handler(
    CommandHandler(
        "fly",
        fly
    )
)

app.add_handler(
    CommandHandler(
        "bj",
        bj
    )
)

# =========================================
# BETTING COMMANDS
# =========================================
app.add_handler(
    CommandHandler(
        "openbets",
        openbets
    )
)

app.add_handler(
    CommandHandler(
        "bet",
        bet
    )
)

app.add_handler(
    CommandHandler(
        "closebets",
        closebets
    )
)

app.add_handler(
    CommandHandler(
        "result",
        result
    )
)

app.add_handler(
    CommandHandler(
        "betlist",
        betlist
    )
)

# =========================================
# IMPOSTER COMMANDS
# =========================================
app.add_handler(
    CommandHandler(
        "startgame",
        startgame
    )
)

# =========================================
# BLACKJACK BUTTONS
# =========================================
app.add_handler(
    CallbackQueryHandler(
        blackjack_buttons,
        pattern="^(hit|stay|double)$"
    )
)

# =========================================
# IMPOSTER BUTTONS
# =========================================
app.add_handler(
    CallbackQueryHandler(
        join_button,
        pattern="^join_game$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        leave_button,
        pattern="^leave_game$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        start_button,
        pattern="^start_game$"
    )
)

app.add_handler(
    CallbackQueryHandler(
        vote_button,
        pattern="^vote_"
    )
)

# =========================================
# AUTO HINT SYSTEM
# =========================================
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        auto_hint
    )
)

# =========================================
# START BOT
# =========================================
print("🏏 BOT RUNNING...")

app.run_polling(
    drop_pending_updates=True
)
