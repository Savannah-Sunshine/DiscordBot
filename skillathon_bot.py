import os
import asyncio
import random
from typing import Optional, Union

from discord.abc import PrivateChannel
# from discord.guild import GuildChannel
from discord.threads import Thread


# This function will load environment variables
# that are stored in 'secrets.env'
def load_env():
    with open('secrets.env') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            key, value = line.split('=')
            os.environ[key] = value


# Don't forget to actually call the function!
load_env()

import logging
import discord


class SkillathonBot(discord.Client):
    # This is the constructor for the bot
    def __init__(self, channel_id: Optional[int] = None):
        # adding intents module to prevent intents error in __init__ method in newer versions of Discord.py
        intents = discord.Intents.default()  # Select all the intents in your bot settings
        intents.message_content = True # Must be same as the intents you selected in your bot settings
        # ^^^ Can read what people are messaging
        super().__init__(intents=intents)
        self.channel_id = channel_id
        self.message_queue = asyncio.Queue()
        self.game_task = None

    async def on_ready(self):
        # print out information when the bot wakes up
        logging.info('Logged in as')
        logging.info(self.user.name)
        logging.info(self.user.id)
        logging.info('------')

    async def close(self):
        logging.info("-- Bot Closing --")
        await super().close()

    # Every time a message is sent in a channel, this is called
    async def on_message(self, message: discord.Message):
        # ignore messages from the bot itself or those not from my channel
        if message.author.id == self.user.id or message.channel.id != self.channel_id:
            return
        # logging.info(f'Message: {message.content[:20]}')

        if message.content.startswith('!hello'):
            await self.send_message(f'Hello World: {message.author.mention}')
        elif message.content.startswith('game'):
            if self.game_task is not None:
                await self.send_message("Game already in progress")
                return
            self.game_task = asyncio.create_task(self.play_game())
        elif message.content is not None and message.content.isdigit():
            self.message_queue.put_nowait(int(message.content))


    async def send_message(self, message:str):
        await self.get_channel(self.channel_id).send(message)


    async def play_game(self):
        await self.send_message("Let's Play! Guess between 1 and 100")
        secret_number = random.randint(1, 100)

        while True:
            guess = await self.message_queue.get()
            if guess == secret_number:
                await self.send_message("You Win!")
                break
            elif guess < secret_number:
                await self.send_message("Too Low!")
            else:
                await self.send_message("Too High!")


def main():
    bot = SkillathonBot(int(os.environ['BOT_CHANNEL_ID']))
    bot.run(os.environ['DISCORD_TOKEN'])


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s - %(message)s'
    )
    main()
