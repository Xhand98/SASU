import discord
import datetime

def create_embed(em_title: str, em_description: str, em_color: discord.Color, author: tuple = None, footer: tuple = None, tables: list = None, image: str = None, thumbnail: str = None, em_timestamp: datetime.datetime = None): 
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

def create_embed_tables(embed: discord.Embed, tables: list, default_inline=True):
    try:
        if not tables:
            print("No data to add to the embed.")
            embed.add_field(name='No Data', value='No information available.', inline=False)
            return

        for obj in tables:
            if len(obj) == 6 and isinstance(obj[5], str):
                embed.add_field(name=f"Steam Info", value=f"ID: {obj[0]}\nSteam ID: {obj[1]}\nUser: {obj[3]}\nCreated: {obj[4]}\nUpdated: {obj[5]}", inline=default_inline)
            elif len(obj) == 5:
                embed.add_field(name=f"Discord Info: {obj[0]}", value=f"ID: {obj[0]}\nDiscord ID: {obj[1]}\nUser: {obj[2]}\nCreated: {obj[3]}\nUpdated: {obj[4]}", inline=default_inline)
            else:
                print(f'Unexpected data format: {obj}')

    except (ValueError, IndexError, TypeError) as error:
        print(f'An error occurred while adding the tables: {error}')
        embed.add_field(name='Create Table Error', value=str(error), inline=False)