import asyncio
import discord
import re
from discord.ext import commands
from db.db_operations import DatabaseOperations as Dbo
from db.dbmanager import DatabaseManager as Dbm
from misc import embed
from misc.utils import process_user_or_steamid, check_user, user_info, get_steamh, normalize_data
import getrequests.getinfo as getinfo
import getrequests.getachievements as getachievements
import getrequests.getgameico as getgameico
import time

class UserCommands(commands.Cog):
    def __init__(self, bot, db_path):
        self.bot = bot
        self.db_operations = Dbo(db_path)


    @commands.slash_command(name="gethours", description="Get hours of a Steam user across all its games.")
    async def gethours_command(self, ctx: discord.ApplicationContext, *, steamid: str | None = None):
        await ctx.defer()
        try:
            if steamid is None:
                steamid = await self.db_operations.get_steamid_from_db(str(ctx.author.id))
                steamid = str(steamid[0][0])
                steamid = await check_user(steamid, ctx)
            else:
                steamid = str(steamid)
                steamid = await check_user(steamid, ctx)

            if steamid:
                hours = await get_steamh(steamid)
                if hours:
                    await ctx.respond(f"Total hours: {hours}")
                else:
                    await ctx.respond("Could not retrieve hours.")
            else:
                await ctx.respond("Invalid SteamID or user not found.")
        except Exception as e:
            await ctx.respond(f"An error occurred while processing your request: {e}")

    @commands.slash_command(name="getsteamid", description="Get the Steam ID of a user.")
    async def getsteamid_command(self, ctx: discord.ApplicationContext, *, steamurl: str | None = None):
        await ctx.defer()
        if steamurl is None:
            data = await self.db_operations.get_steamid_from_db(str(ctx.author.id))
            steamid = data[0][2]
            if steamid:
                user_name = await user_info(steamid)
                result = discord.Embed(
                    title=f"{user_name}'s Steam ID",
                    description=f"{user_name}'s Steam ID is {steamid}",
                    color=discord.Color.random(),
                )
                result.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar)
                await ctx.respond(embed=result)
            else:
                await ctx.respond("No Steam ID found in the database for your account.")
            return

        match = re.search(r"(?:https?://)?steamcommunity\.com/(?:id|profiles)/([^/]+)", steamurl)
        if match:
            steamid_or_username = match.group(1)
        else:
            steamid_or_username = steamurl

        steamid = await process_user_or_steamid(steamid_or_username)
        user_name = await user_info(steamid)
        result = discord.Embed(
            title=f"{user_name}'s Steam ID",
            description=f"{user_name}'s Steam ID is {steamid}",
            color=discord.Color.random(),
        )
        result.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar)
        await ctx.respond(embed=result)

    @commands.slash_command(name="getgames", description="Get the number of all the games a user owns.")
    async def getgames_command(self, ctx: discord.ApplicationContext, *, steamid: str | None = None):
        await ctx.defer()
        if steamid is None:
            steamid = await self.db_operations.get_steamid_from_db(str(ctx.author.id))
            steamid = await check_user(steamid, ctx)
        else:
            steamid = await check_user(steamid, ctx)

        if steamid:
            games = await getinfo.get_games(steamid)
            if games:
                user_name = await user_info(steamid)
                result = discord.Embed(
                    title=f"{user_name}'s Games",
                    description=f"{user_name} owns {games} games.",
                    color=discord.Color.random(),
                )
                result.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar)
                await ctx.respond(embed=result)
            else:
                await ctx.respond("Could not retrieve games.")
        else:
            await ctx.respond("Invalid SteamID or user not found.")

    @commands.slash_command(name="getpfp", description="Get the profile picture of a user.")
    async def getpfp_command(self, ctx: discord.ApplicationContext, *, steamid: str | None = None):
        await ctx.defer()
        if steamid is None:
            steamid = await self.db_operations.get_steamid_from_db(str(ctx.author.id))
            steamid = await check_user(steamid, ctx)
        else:
            steamid = await check_user(steamid, ctx)

        if steamid:
            pic_data = await getinfo.get_pic(steamid)
            if pic_data and pic_data.get("avatar"):
                avatar = pic_data["avatar"]
                user_name = await user_info(steamid)
                result = discord.Embed(
                    title=f"{user_name}'s Profile Picture",
                    color=discord.Color.random(),
                )
                result.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar)
                result.set_image(url=avatar)
                await ctx.respond(embed=result)
            else:
                await ctx.respond(f"Couldn't find profile picture for SteamID {steamid}.")
        else:
            await ctx.respond("Invalid SteamID or user not found.")

    @commands.slash_command(name="getlink", description="Get the link to a user's profile.")
    async def getlink_command(self, ctx: discord.ApplicationContext, *, steamid: str | None = None):
        await ctx.defer()
        if steamid is None:
            steamid = await self.db_operations.get_steamid_from_db(str(ctx.author.id))
            steamid = await check_user(steamid, ctx)
        else:
            steamid = await check_user(steamid, ctx)

        if steamid:
            pic_data = await getinfo.get_pic(steamid)
            if pic_data and pic_data.get("profileurl"):
                url = pic_data["profileurl"]
                user_name = await user_info(steamid)
                result = discord.Embed(
                    title=f"{user_name}'s Profile Link",
                    description=f"[Profile Link]({url})",
                    color=discord.Color.random(),
                )
                result.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar)
                await ctx.respond(embed=result)
            else:
                await ctx.respond(f"Couldn't find profile link for SteamID {steamid}.")
        else:
            await ctx.respond("Invalid SteamID or user not found.")

    @commands.slash_command(name="getlevel", description="Get the level of a user.")
    async def getlevel_command(self, ctx: discord.ApplicationContext, *, steamid: str | None = None):
        await ctx.defer()
        if steamid is None:
            steamid = await self.db_operations.get_steamid_from_db(str(ctx.author.id))
            steamid = await check_user(steamid, ctx)
        else:
            steamid = await check_user(steamid, ctx)

        if steamid:
            level = await getinfo.get_level(steamid)
            if level is not None:
                user_name = await user_info(steamid)
                result = discord.Embed(
                    title=f"{user_name}'s Steam Level",
                    description=f"{user_name} is level {level}.",
                    color=discord.Color.random(),
                )
                result.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar)
                await ctx.respond(embed=result)
            else:
                await ctx.respond(f"Couldn't find the level for SteamID {steamid}.")
        else:
            await ctx.respond("Invalid SteamID or user not found.")

    @commands.slash_command(name="getbadges", description="Get the number of badges a user has.")
    async def getbadges_command(self, ctx: discord.ApplicationContext, *, steamid: str | None = None):
        await ctx.defer()
        if steamid is None:
            steamid = await self.db_operations.get_steamid_from_db(str(ctx.author.id))
            steamid = await check_user(steamid, ctx)
        else:
            steamid = await check_user(steamid, ctx)

        if steamid:
            badges = await getinfo.get_badges(steamid)
            if badges is not None:
                user_name = await user_info(steamid)
                result = discord.Embed(
                    title=f"{user_name}'s Badges",
                    description=f"{user_name} has {badges} badges.",
                    color=discord.Color.random(),
                )
                result.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar)
                await ctx.respond(embed=result)
            else:
                await ctx.respond(f"Couldn't find the badges for SteamID {steamid}.")
        else:
            await ctx.respond("Invalid SteamID or user not found.")

    @commands.slash_command(name="getcountry", description="Get the country of a user.")
    async def getcountry_command(self, ctx: discord.ApplicationContext, *, steamid: str | None = None):
        await ctx.defer()
        if steamid is None:
            steamid = await self.db_operations.get_steamid_from_db(str(ctx.author.id))
            steamid = await check_user(steamid, ctx)
        else:
            steamid = await check_user(steamid, ctx)

        if steamid:
            country = await getinfo.get_country(steamid)
            if country:
                user_name = await user_info(steamid)
                result = discord.Embed(
                    title=f"{user_name}'s Country",
                    description=f"{user_name} is from {country}.",
                    color=discord.Color.random(),
                )
                result.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar)
                await ctx.respond(embed=result)
            else:
                await ctx.respond(f"Couldn't find the country for SteamID {steamid}.")
        else:
            await ctx.respond("Invalid SteamID or user not found.")

    @commands.slash_command(name="getuser", description="Get a preview of a user's profile.")
    async def getuser_command(self, ctx: discord.ApplicationContext, *, steamid: str | None = None):
        await ctx.defer()
        try:
            if steamid is None:
                steamid_data = await self.db_operations.get_steamid_from_db(str(ctx.author.id))
                if not steamid_data:
                    await ctx.respond("No SteamID found linked to your Discord account.")
                    return
                steamid = str(steamid_data[0][0])

            steamid = await check_user(steamid, ctx)
            if not steamid:
                await ctx.respond("Invalid SteamID or user not found.")
                return

            start_time = time.perf_counter()

            total_hours = await get_steamh(steamid)
            total_games = await getinfo.get_games(steamid)
            user_profile = await getinfo.get_pic(steamid)
            user_name = user_profile.get("personaname", "Unknown User")
            user_avatar = await getinfo.get_pic(steamid)
            user_link = await getinfo.get_pic(steamid)
            user_level = await getinfo.get_level(steamid)
            user_badges = await getinfo.get_badges(steamid)
            user_country = await getinfo.get_country(steamid)
            user_achievements = await getachievements.main(steamid)

            result = discord.Embed(
                title=f"{user_name}'s Steam Profile",
                description="Here's a quick overview of the user's Steam profile.",
                color=discord.Color.random(),
                url=user_link["profileurl"],
            )
            result.set_thumbnail(url=user_avatar["avatar"])

            result.add_field(
                name="Total Hours Played",
                value=f"{total_hours:.2f} hours" if total_hours else "Private/Unavailable",
                inline=True,
            )
            result.add_field(
                name="Total Games Owned",
                value=f"{total_games} games" if total_games else "Private/Unavailable",
                inline=True,
            )
            result.add_field(
                name="Steam Level",
                value=f"{user_level}" if user_level else "Private/Unavailable",
                inline=True,
            )
            result.add_field(
                name="Badges",
                value=f"{user_badges}" if user_badges else "Private/Unavailable",
                inline=True,
            )
            result.add_field(
                name="Country",
                value=f"{user_country}" if user_country else "Private/Unavailable",
                inline=True,
            )
            result.add_field(
                name="Total Achievements",
                value=f"{user_achievements}" if user_achievements else "Private/Unavailable",
                inline=True,
            )

            await ctx.respond(embed=result)

            end_time = time.perf_counter()
            print(f"Execution took {end_time - start_time:.2f} seconds")

        except Exception as e:
            print(f"Error getting user info: {e}")
            await ctx.respond("An error occurred while retrieving the user's information.")

    @commands.slash_command(name="getlatestgame", description="Get Latest game of a user.")
    async def getlatestgame_command(self, ctx: discord.ApplicationContext, *, steamid: str | None = None):
        await ctx.defer()
        if steamid is None:
            steamid = await self.db_operations.get_steamid_from_db(str(ctx.author.id))
            steamid = await check_user(steamid, ctx)
        else:
            steamid = await check_user(steamid, ctx)

        if steamid:
            ico = await getgameico.ejecutar(steamid)
            if ico is not None:
                user_name = await user_info(steamid)
                result = discord.Embed(
                    title=f"{user_name}'s Latest Game", color=discord.Color.random()
                )
                result.set_image(url=ico)
                result.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar)
                await ctx.respond(embed=result)
            else:
                await ctx.respond(f"Couldn't find the latest game for SteamID {steamid}.")
        else:
            await ctx.respond("Invalid SteamID or user not found.")

    @commands.slash_command(name="getachievements", description="Gets the number of achievements a player has unlocked.")
    async def getachievements_command(self, ctx: discord.ApplicationContext, *, steamid: str | None = None):
        await ctx.defer()
        if steamid is None:
            steamid = await self.db_operations.get_steamid_from_db(str(ctx.author.id))
            steamid = await check_user(steamid, ctx)
        else:
            steamid = await check_user(steamid, ctx)

        if steamid:
            achievements = await getachievements.main(steamid)
            if achievements is not None:
                user_name = await user_info(steamid)
                result = discord.Embed(
                    title=f"{user_name}'s Achievements",
                    description=f"{user_name} has {achievements} achievements.",
                    color=discord.Color.random(),
                )
                result.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar)
                await ctx.respond(embed=result)
            else:
                await ctx.respond("Couldn't find your achievements.")
        else:
            await ctx.respond("Your SteamID is not linked.")

    @commands.slash_command(name="setup", description="Sets up user for the use of the bot.")
    async def setup_command(self, ctx: discord.ApplicationContext, *, steamid: str | None = None):
        await ctx.defer()
        if steamid:
            steamid = await process_user_or_steamid(steamid)
            discordid = str(ctx.author.id)
            discordname = ctx.author.name
            pic_data = await getinfo.get_pic(steamid)
            steam_username = pic_data.get("personaname")
            db = Dbm(db_path="./db/users.db")
            db.connect()
            discordid = int(discordid)
            steamid = int(steamid)
            db.link_steam_id(discordid, steamid, steam_username, discordname)
            await ctx.respond(f"Your SteamID {steamid} has been linked to {ctx.author}.")
        else:
            await ctx.respond(
                "If you want to setup the bot to work without putting the input, write </tutorial:1275183733116370950>."
            )

    @commands.slash_command(name="showinfo", description="Shows information for the user.")
    async def showinfo_command(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        try:
            discordid = str(ctx.author.id)
            info = await self.db_operations.get_steamid_from_db(discordid)
            info = normalize_data(info)
            embedd = discord.Embed(
                title=f"{ctx.author.name}'s Stored Information",
                color=discord.Color.random(),
            )
            if discordid:
                embed.create_embed_tables(embedd, info, default_inline=True)
                if embedd.fields:
                    await ctx.respond(embed=embedd)
                else:
                    await ctx.respond(content="No information available to display.")
            else:
                await ctx.respond(content="You have not linked your Steam account with the bot.")
        except Exception as e:
            print(f"An error occurred: {e}")
            await ctx.respond("An error occurred while processing your request.")

    @commands.slash_command(name="simpletest", description="Simple test command.")
    async def simpletest_command(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        await asyncio.sleep(1)
        await ctx.respond("This is a test message.")

    @commands.slash_command(name="tutorial", description="Guide on how to set up your Steam account with the bot.")
    async def tutorial_command(self, ctx: discord.ApplicationContext, language: str = "en"):
        await ctx.defer()
        if language.lower() not in ["es", "en"]:
            language = "en"

        if language == "en":
            tutorial_text = (
                "# Welcome to the Steam Bot Setup Tutorial!\n\n"
                "## 1. Setting Up Your SteamID\n"
                "To link your Steam account with the bot, you'll need to  "
                "provide your SteamID. Here's how you can do it:\n"
                "### 1. Find Your SteamID:\n"
                "###   - If you already know your SteamID, you can skip this step. "
                "Otherwise, use one of the following methods:\n"
                "      The Method: Open your Steam profile in a browser "
                "and copy the URL and paste it in, </tutorial:1275183733116370950>, "
                "the output is your steamID.\n\n"
                "## 2. Linking Your SteamID with the Bot\n"
                "Once you have your SteamID, you can link it to "
                "your Discord account using the following command:\n"
                "</setup:1275183733116370947> `steamid:<your_steamid>`\n"
                "Replace <your_steamid> with your actual SteamID.\n\n"
                "## 3. Verifying Your Setup\n"
                "To check if your SteamID is successfully linked, "
                "use the following command:\n"
                "</showinfo:1275183733116370949>\n"
                "The bot will respond with your linked SteamID "
                "if everything is set up correctly.\n\n"
                "## 4. Using Other Commands\n"
                "Now that your SteamID is linked, you can use other "
                "commands to get information about "
                "your Steam profile. For example:\n"
                "</gethours:1275183732927758366> - Get total hours played"
                " across all your games.\n"
                "</getgames:1275183732927758368> - Get the number of games you own.\n"
                "</getlevel:1275183732927758371> - Get your Steam level.\n"
                "</getbadges:1275183732927758372> - Get the number of badges you have.\n"
                "</getcountry:1275183732927758374> - Get your country.\n"
                "</getuser:1275183732927758375> - Get a preview of your Steam profile.\n"
                "</getlatestgame:1275183733116370944> - Get the icon of your latest game.\n"
                "</getachievements:1275183733116370946> - Get the number of"
                " achievements you have unlocked.\n\n"
                "# Need More Help?\n"
                "If you need further assistance, feel free to ask in the support channel or"
                " reach out to  <@543132514848604170>."
            )
        else:  # Spanish by default or if language is 'es'
            tutorial_text = (
                "# ¡Bienvenido al Tutorial de Configuración del Bot de Steam!\n\n"
                "## 1. Configuración de tu SteamID\n"
                "Para vincular tu cuenta de Steam con el bot, "
                " necesitarás proporcionar tu SteamID. "
                "Aquí te explicamos cómo hacerlo:\n"
                "### 1. Encuentra tu SteamID:\n"
                "###    - Si ya conoces tu SteamID, puedes "
                "saltarte este paso. De lo contrario, "
                "usa uno de los siguientes métodos:\n"
                "    Método: Abre tu perfil de Steam en un navegador, "
                "copia la URL y pégala en "
                "`/getsteamid`. El resultado será tu SteamID.\n\n"
                "## 2. Vincula tu SteamID con el Bot\n"
                "Una vez que tengas tu SteamID, puedes vincularla "
                "a tu cuenta de Discord usando el siguiente comando:\n"
                "`</setup:1275183733116370947> steamid:<tu_steamid>`\n"
                "Reemplaza `<tu_steamid>` con tu SteamID real.\n\n"
                "## 3. Verifica tu Configuración\n"
                "Para comprobar si tu SteamID se ha "
                "vinculado correctamente, usa el siguiente "
                "comando:\n"
                "`</showinfo:1275183733116370949>`\n"
                "El bot responderá con tu SteamID vinculada "
                "si todo está configurado correctamente.\n\n"
                "## 4. Usar Otros Comandos\n"
                "Ahora que tu SteamID está vinculada, "
                "puedes usar otros comandos para obtener "
                "información sobre tu perfil de Steam. Por ejemplo:\n"
                "`</gethours:1275183732927758366>` - Obtén el total de horas "
                "jugadas en todos tus juegos.\n"
                "`</getgames:1275183732927758368>` - Obtén el número "
                "de juegos que posees.\n"
                "`</getlevel:1275183732927758371>` - Obtén tu nivel de Steam.\n"
                "`</getbadges:1275183732927758372>` - Obtén el número de "
                "insignias que tienes.\n"
                "`</getcountry:1275183732927758374>` - Obtén tu país.\n"
                "`</getuser:1275183732927758375>` - Obtén una vista previa "
                "de tu perfil de Steam.\n"
                "`</getlatestgame:1275183733116370944>` - Obtén el icono de "
                "tu juego más reciente.\n"
                "`</getachievements:1275183733116370946>` - Obtén el número de logros "
                "que has desbloqueado.\n\n"
                "# ¿Necesitas más ayuda?\n"
                "Si necesitas más asistencia, no dudes  "
                "en preguntar en el canal de soporte o"
                "contactar a cualquier <@543132514848604170> ."
            )

        await ctx.respond(tutorial_text)