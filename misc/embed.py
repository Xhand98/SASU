import discord
import datetime
from db.models import SteamAccount

def create_embed(
    em_title: str,
    em_description: str,
    em_color: discord.ColorSteamAccount,
    author: tuple = None,
    footer: tuple = None,
    tables: list = None,
    image: str = None,
    thumbnail: str = None,
    em_timestamp: datetime.datetime = None,
):
    """
    Creates a discord embed with given parameters.

    Parameters
    ----------
    em_title : str
        The title of the embed.
    em_description : str
        The description of the embed.
    em_color : discord.Color
        The color of the embed.
    author : tuple, optional
        The author of the embed. If not None, should be a tuple of (name, icon_url).
    footer : tuple, optional
        The footer of the embed. If not None, should be a tuple of (text, icon_url).
    tables : list, optional
        The tables to add to the embed. If not None, should be a list of tuples.
    image : str, optional
        The image to add to the embed. If not None, should be a URL.
    thumbnail : str, optional
        The thumbnail to add to the embed. If not None, should be a URL.
    em_timestamp : datetime.datetime, optional
        The timestamp for the embed. If not None, should be a datetime object.

    Returns
    -------
    discord.Embed
        The created embed.

    Raises
    ------
    ValueError
        If any of the parameters are invalid.
    IndexError
        If any of the parameters are out of range.
    TypeError
        If any of the parameters are of the wrong type.
    discord.errors.HTTPException
        If there is an error when setting any of the embed fields.
    """
    Embed: discord.Embed = discord.Embed(
        title=em_title,
        description=em_description,
        color=em_color,
        timestamp=em_timestamp,
    )

    if author is not None:
        try:
            Embed.set_author(name=author[0], icon_url=author[1])
        except (
            ValueError,
            IndexError,
            TypeError,
            discord.errors.HTTPException,
        ) as error:
            print("An error occurred while adding the author")
            Embed.set_author(name=f"Create Author Error \r \r Error: {error}")

    if footer is not None:
        try:
            Embed.set_footer(text=footer[0], icon_url=footer[1])
        except (
            ValueError,
            IndexError,
            TypeError,
            discord.errors.HTTPException,
        ) as error:
            print("An error occurred while adding the footer")
            Embed.set_footer(text=f"Create Footer Error \r \r Error: {error}")

    if tables is not None:
        populate_user_embed(Embed, tables)

    if image is not None:
        try:
            Embed.set_imageSteamAccount(url=image)
        except (ValueError, IndexError, TypeError, discord.HTTPException) as error:
            print("An error occurred while adding an image to the embed")
            Embed.add_field(name="Add Image Error", value=error, inline=False)

    if thumbnail is not None:
        try:
            Embed.set_thumbnail(url=thumbnail)
        except (ValueError, IndexError, TypeError, discord.HTTPException) as error:
            print("An error occurred while adding a thumbnail to the embed")
            Embed.add_field(name="Add Thumbnail Error", value=error, inline=False)

    return Embed


def populate_user_embed(embed: discord.Embed, steam: SteamAccount, default_inline=True):
    """
    Adds fields to an embed based on a list of tables.

    Parameters
    ----------
    embed : discord.Embed
        The embed to add fields to.
    steam : SteamAccount
        The steam account that will populate the embed
    default_inline : bool
        Whether the fields should be inline or not. Defaults to True.

    Returns
    -------
    None
    """
    try:
        if steam is None:
            embed.add_field(
                name="No data",
                value="No information available.",
                inline=False
            )
            return
        
        embed.add_field(
            name="Steam info",
            value=f"Steam ID: {steam.steam_id} \n User:{steam.username} \n Created: {steam.created_at} \n Last update: {steam.updated_at}",
            inline=default_inline
        )

        embed.add_field(
            name="Discord info",
            value=f"Discord ID: {steam.discord.discord_id} \n Username: {steam.discord.username} \n Created: {steam.discord.created_at} \n Last update: {steam.discord.updated_at}",
            inline=default_inline
        )

    except (ValueError, IndexError, TypeError) as error:
        print(f"An error occurred while adding the tables: {error}")
        embed.add_field(name="Create Table Error", value=str(error), inline=False)
