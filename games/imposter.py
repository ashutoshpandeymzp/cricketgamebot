from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ContextTypes
)

import random

from database.users import (
    create_user,
    add_coins
)

from database.words import ALL_WORDS

# =========================================
# ACTIVE GAMES
# =========================================
imposter_games = {}

# =========================================
# START GAME
# =========================================
async def startgame(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # ONLY GROUPS
    if update.effective_chat.type == "private":

        await update.message.reply_text(
            "❌ Imposter game only works in groups"
        )

        return

    group_id = update.effective_chat.id

    # PREVENT DOUBLE GAME
    if group_id in imposter_games:

        await update.message.reply_text(
            "⚠️ A game is already running"
        )

        return

    imposter_games[group_id] = {

        "players": [],
        "started": False,
        "imposter": None,
        "common_word": None,
        "imposter_word": None,
        "hints": {},
        "votes": {},
        "vote_phase": False,
        "caught": False
    }

    keyboard = [

        [
            InlineKeyboardButton(
                "🎮 JOIN GAME",
                callback_data="join_game"
            )
        ],

        [
            InlineKeyboardButton(
                "❌ LEAVE GAME",
                callback_data="leave_game"
            )
        ],

        [
            InlineKeyboardButton(
                "🚀 START GAME",
                callback_data="start_game"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(
        keyboard
    )

    await update.message.reply_text(

        "🎮 Imposter Game Created!\n\n"

        "Click buttons below to join or leave.",

        reply_markup=reply_markup
    )


# =========================================
# JOIN BUTTON
# =========================================
async def join_button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user = query.from_user

    group_id = query.message.chat.id

    if group_id not in imposter_games:

        return

    game = imposter_games[group_id]

    # GAME STARTED
    if game["started"]:

        await query.answer(
            "Game already started",
            show_alert=True
        )

        return

    player_ids = [

        p["id"]

        for p in game["players"]
    ]

    # ALREADY JOINED
    if user.id in player_ids:

        await query.answer(
            "Already joined",
            show_alert=True
        )

        return

    game["players"].append({

        "id": user.id,
        "name": user.first_name
    })

    await query.message.reply_text(
        f"✅ {user.first_name} joined the game"
    )


# =========================================
# LEAVE BUTTON
# =========================================
async def leave_button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user = query.from_user

    group_id = query.message.chat.id

    if group_id not in imposter_games:

        return

    game = imposter_games[group_id]

    # GAME STARTED
    if game["started"]:

        await query.answer(
            "Game already started",
            show_alert=True
        )

        return

    new_players = []

    removed = False

    for player in game["players"]:

        if player["id"] != user.id:

            new_players.append(player)

        else:

            removed = True

    game["players"] = new_players

    if removed:

        await query.message.reply_text(
            f"❌ {user.first_name} left the game"
        )

    else:

        await query.answer(
            "You are not in game",
            show_alert=True
        )


# =========================================
# START BUTTON
# =========================================
async def start_button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user = query.from_user

    group_id = query.message.chat.id

    if group_id not in imposter_games:

        return

    game = imposter_games[group_id]

    # CHECK ADMIN
    member = await context.bot.get_chat_member(
        group_id,
        user.id
    )

    if member.status not in [
        "administrator",
        "creator"
    ]:

        await query.answer(
            "Only admins can start game",
            show_alert=True
        )

        return

    # GAME ALREADY STARTED
    if game["started"]:

        await query.answer(
            "Game already started",
            show_alert=True
        )

        return

    # MIN PLAYERS
    if len(game["players"]) < 3:

        await query.answer(
            "Need at least 3 players",
            show_alert=True
        )

        return

    # RANDOM IMPOSTER
    imposter = random.choice(
        game["players"]
    )

    game["imposter"] = imposter["id"]

    # =========================================
    # RANDOM WORD LOGIC
    # =========================================

        # =========================================
    # TRUE RANDOM WORD SYSTEM
    # =========================================

    # FLATTEN ALL WORDS
    all_words_flat = []

    for pair in ALL_WORDS:

        all_words_flat.extend(pair)

    # REMOVE DUPLICATES
    all_words_flat = list(
        set(all_words_flat)
    )

    # RANDOM MAIN WORD
    common_word = random.choice(
        all_words_flat
    )

    # RANDOM IMPOSTER WORD
    imposter_word = random.choice(
        all_words_flat
    )

    # ENSURE DIFFERENT WORDS
    while imposter_word == common_word:

        imposter_word = random.choice(
            all_words_flat
        )

    game["common_word"] = common_word

    game["imposter_word"] = imposter_word

    game["started"] = True

    # SEND WORDS
    for player in game["players"]:

        try:

            # IMPOSTER
            if player["id"] == imposter["id"]:

                await context.bot.send_message(

                    chat_id=player["id"],

                    text=(

                        "🏏 Your Secret Word:\n\n"

                        f"{imposter_word}\n\n"

                        "Send ONE hint."
                    )
                )

            # NORMAL PLAYER
            else:

                await context.bot.send_message(

                    chat_id=player["id"],

                    text=(

                        "🏏 Your Secret Word:\n\n"

                        f"{common_word}\n\n"

                        "Send ONE hint."
                    )
                )

        except:

            pass

    game["common_word"] = common_word

    game["imposter_word"] = imposter_word

    game["started"] = True

    # SEND WORDS
    for player in game["players"]:

        try:

            # IMPOSTER
            if player["id"] == imposter["id"]:

                await context.bot.send_message(

                    chat_id=player["id"],

                    text=(

                        "🏏 Your Secret Word:\n\n"

                        f"{imposter_word}\n\n"

                        "Send ONE hint."
                    )
                )

            # NORMAL PLAYER
            else:

                await context.bot.send_message(

                    chat_id=player["id"],

                    text=(

                        "🏏 Your Secret Word:\n\n"

                        f"{common_word}\n\n"

                        "Send ONE hint."
                    )
                )

        except:

            pass

    await query.message.reply_text(

        "✅ Game Started!\n\n"

        "Words sent in DM.\n"

        "Players now send hints privately."
    )


# =========================================
# AUTO HINT SYSTEM
# =========================================
async def auto_hint(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # ONLY PRIVATE CHAT
    if update.effective_chat.type != "private":

        return

    user = update.effective_user

    hint_text = update.message.text

    found_game = None

    found_group = None

    # FIND GAME
    for group_id, game in imposter_games.items():

        for player in game["players"]:

            if player["id"] == user.id:

                found_game = game

                found_group = group_id

                break

    if found_game is None:

        return

    # ALREADY SENT
    if user.id in found_game["hints"]:

        await update.message.reply_text(
            "⚠️ You already sent your hint"
        )

        return

    found_game["hints"][user.id] = hint_text

    await update.message.reply_text(
        "✅ Hint submitted"
    )

    # ALL HINTS RECEIVED
    if len(found_game["hints"]) == len(found_game["players"]):

        found_game["vote_phase"] = True

        text = "📝 ALL HINTS\n\n"

        for player in found_game["players"]:

            player_hint = found_game["hints"].get(
                player["id"],
                "No hint"
            )

            text += (
                f"{player['name']} ➜ "
                f"{player_hint}\n"
            )

        # VOTE BUTTONS
        keyboard = []

        for player in found_game["players"]:

            keyboard.append(

                [
                    InlineKeyboardButton(

                        player["name"],

                        callback_data=(
                            f"vote_"
                            f"{player['id']}"
                        )
                    )
                ]
            )

        reply_markup = InlineKeyboardMarkup(
            keyboard
        )

        await context.bot.send_message(

            chat_id=found_group,

            text=(
                text +
                "\n🗳️ Vote the Imposter!"
            ),

            reply_markup=reply_markup
        )


# =========================================
# VOTE BUTTONS
# =========================================
async def vote_button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user = query.from_user

    group_id = query.message.chat.id

    if group_id not in imposter_games:

        return

    game = imposter_games[group_id]

    if not game["vote_phase"]:

        return

    # ALREADY VOTED
    if user.id in game["votes"]:

        await query.answer(
            "You already voted",
            show_alert=True
        )

        return

    voted_id = int(
        query.data.split("_")[1]
    )

    game["votes"][user.id] = voted_id

    total_votes = len(game["votes"])

    total_players = len(game["players"])

    remaining = total_players - total_votes

    # BUILD LIVE VOTE TABLE
    vote_text = "🗳️ LIVE VOTING\n\n"

    for voter_id, target_id in game["votes"].items():

        voter_name = "Unknown"

        target_name = "Unknown"

        for player in game["players"]:

            if player["id"] == voter_id:

                voter_name = player["name"]

            if player["id"] == target_id:

                target_name = player["name"]

        vote_text += (
            f"• {voter_name} ➜ {target_name}\n"
        )

    vote_text += (

        f"\n📊 Votes: "
        f"{total_votes}/{total_players}\n"

        f"⏳ Remaining: "
        f"{remaining}"
    )

    await query.message.reply_text(
        vote_text
    )

    # ALL PLAYERS VOTED
    if len(game["votes"]) == len(game["players"]):

        await context.bot.send_message(

            chat_id=group_id,

            text="✅ All votes received!\n\nCalculating results..."
        )

        await endgame_logic(
            context,
            group_id
        )


# =========================================
# ENDGAME LOGIC
# =========================================
async def endgame_logic(
    context,
    group_id
):

    game = imposter_games[group_id]

    vote_count = {}

    for voted_id in game["votes"].values():

        if voted_id not in vote_count:

            vote_count[voted_id] = 0

        vote_count[voted_id] += 1

    eliminated = max(

        vote_count,

        key=vote_count.get
    )

    imposter_id = game["imposter"]

    imposter_name = "Unknown"

    for player in game["players"]:

        if player["id"] == imposter_id:

            imposter_name = player["name"]

    # IMPOSTER CAUGHT
    if eliminated == imposter_id:

        game["caught"] = True

        await context.bot.send_message(

            chat_id=group_id,

            text=(

                "🎯 Imposter Caught!\n\n"

                f"🤫 Imposter: "
                f"{imposter_name}\n\n"

                "Imposter now gets "
                "ONE final guess.\n\n"

                "Use:\n"

                "/guess word"
            )
        )

    # IMPOSTER ESCAPED
    else:

        create_user(imposter_id)

        add_coins(
            imposter_id,
            500
        )

        await context.bot.send_message(

            chat_id=group_id,

            text=(

                "😈 Imposter Escaped!\n\n"

                f"🤫 Imposter: "
                f"{imposter_name}\n"

                "💰 Won 500 coins!"
            )
        )

        del imposter_games[group_id]


# =========================================
# FINAL GUESS
# =========================================
async def guess(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    group_id = update.effective_chat.id

    user = update.effective_user

    if group_id not in imposter_games:

        return

    game = imposter_games[group_id]

    if not game["caught"]:

        await update.message.reply_text(
            "Imposter was not caught"
        )

        return

    # ONLY IMPOSTER
    if user.id != game["imposter"]:

        await update.message.reply_text(
            "Only imposter can guess"
        )

        return

    if len(context.args) < 1:

        await update.message.reply_text(
            "Usage:\n/guess word"
        )

        return

    guessed_word = " ".join(
        context.args
    ).lower()

    real_word = game["common_word"].lower()

    imposter_name = "Unknown"

    for player in game["players"]:

        if player["id"] == game["imposter"]:

            imposter_name = player["name"]

    # CORRECT GUESS
    if guessed_word == real_word:

        create_user(user.id)

        add_coins(
            user.id,
            500
        )

        await update.message.reply_text(

            "😈 Imposter guessed correctly!\n\n"

            f"🏏 Word was: "
            f"{real_word}\n"

            f"💰 {imposter_name} "
            "won 500 coins!"
        )

    # WRONG GUESS
    else:

        for player in game["players"]:

            if player["id"] != game["imposter"]:

                create_user(player["id"])

                add_coins(
                    player["id"],
                    200
                )

        await update.message.reply_text(

            "❌ Wrong Guess!\n\n"

            f"🏏 Word was: "
            f"{real_word}\n\n"

            "🎉 Other players "
            "won 200 coins each!"
        )

    del imposter_games[group_id]