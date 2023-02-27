import nextcord
import openai
import os
from nextcord.ext import commands

intents = nextcord.Intents(messages = True, guilds = True)
intents.guild_messages = True
intents.members = True
intents.message_content = True
intents.voice_states = True
intents.emojis_and_stickers = True
all_intents = intents.all()
all_intents= True


bot = commands.Bot(command_prefix='-', intents = intents)
openai.api_key=os.environ['api_token']

@bot.event
async def on_ready():
    print(f'logged in as: {bot.user.name}')
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="-help"))

    
@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = nextcord.Embed(description=f'**Cooldown active**\ntry again in `{error.retry_after:.2f}`s*',color=ctx.author.color)
        await ctx.send(embed=em)
        
@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=nextcord.Embed(description="Missing `arguments`", color=ctx.author.color))


@commands.cooldown(1, 2, commands.BucketType.user)
@bot.command(name='ping', help=f"displays bot's latency", description=',ping')
async def ping_command(ctx:commands.Context):    
    em = nextcord.Embed(description=f'**Pong!**\n\n`{round(bot.latency*1000)}`ms', color=ctx.author.color)
    await ctx.send(embed=em)

@commands.cooldown(1, 2, commands.BucketType.user)
@bot.command(name='hey', help='ask me anything by writing -hey [question]')
async def hey_command(ctx: commands.Context, *,args):
    async with ctx.typing():
        solution = []
        complition = openai.Completion.create(engine='text-davinci-003', prompt=args, max_tokens=4000)
        solution.append(complition.choices[0]['text'])
        for i in solution:
            await ctx.reply(embed=nextcord.Embed(description=f'{i}', color=ctx.author.color))
    
if __name__ == '__main__':
    bot.run(os.environ['bot_token'])    