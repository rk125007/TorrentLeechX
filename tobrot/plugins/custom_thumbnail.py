"""ThumbNail utilities, © @AnyDLBot"""


import os

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from tobrot import DOWNLOAD_LOCATION, CLEAR_THUMBNAIL


async def save_thumb_nail(client, message):
    thumbnail_location = os.path.join(DOWNLOAD_LOCATION, "thumbnails")
    thumb_image_path = os.path.join(
        thumbnail_location, str(message.from_user.id) + ".jpg"
    )
    ismgs = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ")
    if message.reply_to_message is not None:
        if not os.path.isdir(thumbnail_location):
            os.makedirs(thumbnail_location)
        download_location = thumbnail_location + "/"
        downloaded_file_name = await client.download_media(
            message=message.reply_to_message, file_name=download_location
        )
        # https://stackoverflow.com/a/21669827/4723940
        Image.open(downloaded_file_name).convert("RGB").save(downloaded_file_name)
        metadata = extractMetadata(createParser(downloaded_file_name))
        height = 0
        if metadata.has("height"):
            height = metadata.get("height")
        # resize image
        # ref: https://t.me/PyrogramChat/44663
        img = Image.open(downloaded_file_name)
        # https://stackoverflow.com/a/37631799/4723940
        # img.thumbnail((320, 320))
        img.resize((320, height))
        img.save(thumb_image_path, "JPEG")
        # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
        os.remove(downloaded_file_name)
        await ismgs.edit(
            "🟢 ᴛʜᴜᴍʙɴᴀɪʟ sᴀᴠᴇᴅ 🟢"
            + f"\n\nᴡɪʟʟ ᴜsᴇ ᴜɴᴛɪʟ <code>/{CLEAR_THUMBNAIL}</code>"
        )
    else:
        await ismgs.edit("🔴 ʀᴇᴘʟʏ ᴛᴏ ᴘʜᴏᴛᴏ 🔴")


async def clear_thumb_nail(client, message):
    thumbnail_location = os.path.join(DOWNLOAD_LOCATION, "thumbnails")
    thumb_image_path = os.path.join(
        thumbnail_location, str(message.from_user.id) + ".jpg"
    )
    ismgs = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ")
    if os.path.exists(thumb_image_path):
        os.remove(thumb_image_path)
        await ismgs.edit("⚫ ᴛʜᴜᴍʙɴᴀɪʟ ᴅᴇʟᴇᴛᴇᴅ ⚫")
    else:
        await ismgs.edit("ɴᴏᴛʜɪɴɢ ᴛᴏ ᴄʟᴇᴀʀ")