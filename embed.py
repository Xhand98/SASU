import discord
import datetime

def create_embed(em_title: str, em_description: str, em_color: discord.Color.red, author: tuple = None, footer: tuple = None, tables: list = None, image: str = None, thumbnail: str = None, em_timestamp: datetime.datetime = None):
    Embed: discord.Embed = discord.Embed(
        title=em_title,
        description=em_description,
        color=em_color,
        timestamp=em_timestamp
    )

    if author is not None:
        try:
            Embed.set_author(name=author[0], icon_url=author[1])
        except (ValueError, IndexError, TypeError, discord.errors.HTTPException) as error:
            print('An error occurred while adding the author')
            Embed.set_author(name=f'Create Author Error \r \r Error: {error}')

    if footer is not None:
        try:
            Embed.set_footer(text=footer[0], icon_url=footer[1])
        except (ValueError, IndexError, TypeError, discord.errors.HTTPException) as error:
            print('An error occurred while adding the footer')
            Embed.set_footer(text=f'Create Footer Error \r \r Error: {error}')

    if tables is not None:
        create_embed_tables(Embed, tables)

    if image is not None:
        try:
            Embed.set_image(url=image)
        except (ValueError, IndexError, TypeError, discord.HTTPException) as error:
            print('An error occurred while adding an image to the embed')
            Embed.add_field(name='Add Image Error', value=error, inline=False)

    if thumbnail is not None:
        try:
            Embed.set_thumbnail(url=thumbnail)
        except (ValueError, IndexError, TypeError, discord.HTTPException) as error:
            print('An error occurred while adding a thumbnail to the embed')
            Embed.add_field(name='Add Thumbnail Error', value=error, inline=False)

    return Embed

def create_embed_tables(embed: discord.Embed, tables: list):
    try:
        for obj in tables:  # Espaciado entre columnas
            embed.add_field(name=obj[0], value=obj[1], inline=obj[2])

            if len(obj) > 3:
                create_embed_tables(embed, obj[3])
    except (ValueError, IndexError, TypeError) as error:
        print('An error occurred while adding the tables')
        embed.add_field(name='Create Table Error', value=error, inline=False)
