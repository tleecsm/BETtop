import discord


async def send_embedded_reply(message, 
                              title, 
                              description=None,
                              footer=None,
                              image_url=None,
                              thumbnail_url=None,
                              author=None,
                              fields=None):
    embed = discord.Embed(title=title, description=description)
    if footer:
        embed.set_footer(footer)
    if image_url:
        embed.set_image(image_url)
    if thumbnail_url:
        embed.set_thumbnail(thumbnail_url)
    if author:
        embed.set_author(author)
    if fields:
        for field in fields:
            embed.add_field(**field)
    await message.channel.send(embed=embed)
