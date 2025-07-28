# MostFitPersonBot

This bot is meant to make exercising competitive with your friends.  
The bot is easy to build but might have some problems...

There are currently 4 commands:

- `/run` — gives points based on how long you ran, average heart rate, and distance.  
- `/gym` — gives 25 points when used; can only be used once per day.  
- `/top` — shows the current top 3 users.  
- `/daily_summary` — shows the top 3 of that day plus a report on how many points you managed to get.

---

# Setup

1. Install `uv` if you do not have it already. You will also require **Python 3.13+**:
    ```bash
    pip install uv
    ```
2. Run:
    ```bash
    uv sync
    ```
    to sync project dependencies.

3. To run the bot, use:
    ```bash
    uv run main.py
    ```
    in the project directory.  
    **You need a Discord bot token to run it.**

4. Get your bot token:
   1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   2. Log in with your Discord account.
   3. Create a new application:
      - Click **New Application**.
      - Give your app a name and click **Create**.
   4. Add a bot to your application:
      - In the left sidebar, click **Bot**.
      - Click **Add Bot**, then confirm.
   5. Copy your bot token:
      - Under the **Bot** section, find the **Token** area.
      - Click **Copy** to copy your bot token.

5. Use the token in your project by:
   - Adding it to a `.env` file (recommended), or
   - Directly in your code (not recommended for security reasons).

---

You're ready to run the bot!
