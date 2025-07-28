import discord
import sqlite3
from pathlib import Path
from discord import app_commands
import datetime

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


DB_PATH = Path("data/user_data.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            user_id TEXT,
            time REAL,
            heart_rate INTEGER,
            distance REAL,
            points REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS gym_visits (
            user_id TEXT,
            date TEXT,
            points INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

def log_run(user_id, time, hr, distance, points):
    with get_conn() as conn:
        conn.execute("""
        INSERT INTO runs (user_id, time, heart_rate, distance, points)
        VALUES (?, ?, ?, ?, ?)
        """, (user_id, time, hr, distance, points))
        conn.commit()

def get_top_users(limit=3):
    query = """
    SELECT user_id, SUM(total_points) AS total_points
    FROM (
        SELECT user_id, SUM(points) AS total_points
        FROM runs
        GROUP BY user_id
        UNION ALL
        SELECT user_id, SUM(points) AS total_points
        FROM gym_visits
        GROUP BY user_id
    )
    GROUP BY user_id
    ORDER BY total_points DESC
    LIMIT ?
    """
    with get_conn() as conn:
        cursor = conn.execute(query, (limit,))
        return cursor.fetchall()




#Points
def calculate_points(time,hr , distance):
    return time * (hr/100) + distance * 10

@client.event
async def on_ready():
    init_db()
    await tree.sync()
    print(f"Logged in as {client.user}")


@tree.command(name="daily_summary", description="Ping all users active today with their points and top 3")
async def daily_summary(interaction: discord.Interaction):
    today = datetime.date.today().isoformat()

    with get_conn() as conn:
        cursor = conn.execute("""
            SELECT user_id, SUM(points) as total_points FROM (
                SELECT user_id, points FROM runs
                WHERE DATE(timestamp) = ?
                UNION ALL
                SELECT user_id, points FROM gym_visits
                WHERE date = ?
            )
            GROUP BY user_id
            ORDER BY total_points DESC
        """, (today, today))
        results = cursor.fetchall()

    if not results:
        await interaction.response.send_message("No one was active today", ephemeral=True)
        return

    msg = f"**Daily Summary for {today}**\n\n"
    top = results[:3]

    msg += "**Top 3 Today:**\n"
    for i, (user_id, points) in enumerate(top, start=1):
        msg += f"{i}. <@{user_id}> — {points:.1f} points\n"

    msg += "\n**All Active Users Today:**\n"
    for user_id, points in results:
        msg += f"• <@{user_id}> gained **{points:.1f}** points\n"

    await interaction.response.send_message(msg)

@tree.command(name="gym", description="Log a gym visit (25 points, once per day)")
async def gym_command(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    today = datetime.date.today().isoformat()

    with get_conn() as conn:
        cursor = conn.execute("""
        SELECT 1 FROM gym_visits
        WHERE user_id = ? AND date = ?
        """, (user_id, today))
        already_logged = cursor.fetchone()

    if already_logged:
        await interaction.response.send_message("You already logged a gym visit today", ephemeral=True)
        return

    with get_conn() as conn:
        conn.execute("""
        INSERT INTO gym_visits (user_id, date, points)
        VALUES (?, ?, ?)
        """, (user_id, today, 25))
        conn.commit()

    await interaction.response.send_message("Gym visit logged! You earned **25 points**.", ephemeral=True)

@tree.command(name="run", description="Log a run and earn points")
@app_commands.describe(
    time="Time in minutes",
    hr="Average heart rate",
    distance="Distance in kilometers"
)
async def run_command(interaction: discord.Interaction, time: float, hr: int, distance: float):
    user_id = str(interaction.user.id)
    points = calculate_points(time, hr, distance)
    log_run(user_id, time, hr, distance, points)
    await interaction.response.send_message(
        f"Run logged!\nYou earned **{points:.1f}** points."
    )

@tree.command(name="top", description="Show the top 3 users by total points")
async def top_command(interaction: discord.Interaction):
    top_users = get_top_users()
    if not top_users:
        await interaction.response.send_message("No data yet.")
        return

    msg = "**Top 3 Users:**\n"
    for i, (user_id, total_points) in enumerate(top_users, start=1):
        msg += f"{i}. <@{user_id}> — {total_points:.1f} points\n"
    await interaction.response.send_message(msg, ephemeral=True)

client.run("")      #Add your discord token

