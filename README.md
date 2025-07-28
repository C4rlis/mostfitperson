#MostFitPersonBot

This bot is meant to make exercising competitive with your friends, the bot is easy to build and might have some problems...

There are currently 4 commands "/run, /top, /gym and /daily_summary"
"/run" gives points based on how long you ran, avg heart rate and distance.
"/gym" gives 25 points when used it can only be used once per day
"/top" gives the current top 3
"/daily_summary" gives the top 3 of that day + a report on how many point you managed to get.









#Setup

1. Install uv if you do not have it already, also you will require Python 3.13+
   ```bash
   pip install uv
    ```
2. Run "uv sync" to sync with the project dependencies
      
3. To run "uv run main.py" in the project directory, you need to have a "bot token" to run it.

3. Go to the Discord Developer Portal.

4.  Log in with your Discord account.

5. Create a new application:

    Click the "New Application" button.

    Give your app a name and click Create.

6. Add a bot to your application:

    In the left sidebar, click "Bot".

    Click "Add Bot", then confirm.

7. Copy your bot token:

    Under the "Bot" section, find the "Token" area.

    Click "Copy" to copy your bot token.
8. Use this token to run your bot:

    For example, add it to your .env file or directly in your code (not recommended for security reasons).
