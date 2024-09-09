import discord
import datetime


def create_embed(
    em_title: str,
    em_description: str,
    em_color: discord.Color,
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
        create_embed_tables(Embed, tables)

    if image is not None:
        try:
            Embed.set_image(url=image)
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


def create_embed_tables(embed: discord.Embed, tables: list, default_inline=True):
    """
    Adds fields to an embed based on a list of tables.

    Parameters
    ----------
    embed : discord.Embed
        The embed to add fields to.
    tables : list
        A list of tuples containing the data to add to the embed.
        Each tuple should have the following structure:

        - len(obj) == 6:
            - obj[0]: The ID of the user.
            - obj[1]: The Steam ID of the user.
            - obj[2]: The username of the user.
            - obj[3]: The created date of the user.
            - obj[4]: The updated date of the user.
            - obj[5]: The updated date of the user as a string.
        - len(obj) == 5:
            - obj[0]: The ID of the user.
            - obj[1]: The Discord ID of the user.
            - obj[2]: The username of the user.
            - obj[3]: The created date of the user.
            - obj[4]: The updated date of the user.
    default_inline : bool
        Whether the fields should be inline or not. Defaults to True.

    Returns
    -------
    None
    """
    try:
        if not tables:
            print("No data to add to the embed.")
            embed.add_field(
                name="No Data", value="No information available.", inline=False
            )
            return

        for obj in tables:
            if len(obj) == 6 and isinstance(obj[5], str):
                embed.add_field(
                    name="Steam Info",
                    value=f"ID: {obj[0]}\nSteam ID: {obj[1]}\nUser: "
                    f"{obj[3]}\nCreated: {obj[4]}\nUpdated: {obj[5]}",
                    inline=default_inline,
                )
            elif len(obj) == 5:
                embed.add_field(
                    name=f"Discord Info: {obj[0]}",
                    value=f"ID: {obj[0]}\nDiscord ID: {obj[1]}\nUser:"
                    f" {obj[2]}\nCreated: {obj[3]}\nUpdated: {obj[4]}",
                    inline=default_inline,
                )
            else:
                print(f"Unexpected data format: {obj}")

    except (ValueError, IndexError, TypeError) as error:
        print(f"An error occurred while adding the tables: {error}")
        embed.add_field(name="Create Table Error", value=str(error), inline=False)
