from pyrogram import Client, filters, errors, types
from config import Rkn_Bots
import asyncio, re, time, sys, os
from .database import total_user, getid, delete, addCap, updateCap, insert, chnl_ids
from pyrogram.errors import FloodWait

@Client.on_message(filters.private & filters.user(Rkn_Bots.ADMIN) & filters.command(["rknusers"]))
async def all_db_users_here(client, message):
    x = await message.reply_text("Please Wait....")
    total = await total_user()
    await x.edit(f"Tᴏᴛᴀʟ Usᴇʀ :- `{total}`")

@Client.on_message(filters.private & filters.user(Rkn_Bots.ADMIN) & filters.command(["broadcast"]))
async def broadcast(bot, message):
    if message.reply_to_message:
        rkn = await message.reply_text("Getting all IDs from database...\nPlease wait")
        all_users = await getid()
        tot = await total_user()
        success, failed, deactivated, blocked = 0, 0, 0, 0
        
        await rkn.edit(f"ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ...")
        
        for user in all_users:
            try:
                await asyncio.sleep(1)
                await message.reply_to_message.copy(user['_id'])
                success += 1
            except errors.InputUserDeactivated:
                deactivated += 1
                await delete({"_id": user['_id']})
            except errors.UserIsBlocked:
                blocked += 1
                await delete({"_id": user['_id']})
            except Exception as e:
                failed += 1
                await delete({"_id": user['_id']})
                print(f"Error broadcasting to {user['_id']}: {e}")
            try:
                await rkn.edit(f"<u>ʙʀᴏᴀᴅᴄᴀsᴛ ᴘʀᴏᴄᴇssɪɴɢ</u>\n\n• ᴛᴏᴛᴀʟ ᴜsᴇʀs: {tot}\n• sᴜᴄᴄᴇssғᴜʟ: {success}\n• ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: {blocked}\n• ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: {deactivated}\n• ᴜɴsᴜᴄᴄᴇssғᴜʟ: {failed}")
            except FloodWait as e:
                await asyncio.sleep(e.x)
        
        await rkn.edit(f"<u>ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</u>\n\n• ᴛᴏᴛᴀʟ ᴜsᴇʀs: {tot}\n• sᴜᴄᴄᴇssғᴜʟ: {success}\n• ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: {blocked}\n• ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: {deactivated}\n• ᴜɴsᴜᴄᴄᴇssғᴜʟ: {failed}")

@Client.on_message(filters.private & filters.user(Rkn_Bots.ADMIN) & filters.command("restart"))
async def restart_bot(b, m):
    msg = await b.send_message(text="**🔄 𝙿𝚁𝙾𝙲𝙴𝚂𝚂𝙴𝚂 𝚂𝚃𝙾𝙿𝙴𝙳. 𝙱𝙾𝚃 𝙸𝚂 𝚁𝙴𝚂𝚃𝙰𝚁𝚃𝙸𝙽𝙶...**", chat_id=m.chat.id)       
    await asyncio.sleep(3)
    await msg.edit("**✅️ 𝙱𝙾𝚃 𝙸𝚂 𝚁𝙴𝚂𝚃𝙰𝚁𝚃𝙴𝙳. 𝙽𝙾𝚆 𝚈𝙾𝚄 𝙲𝙰𝙽 𝚄𝚂𝙴 𝙼𝙴**")
    os.execl(sys.executable, sys.executable, *sys.argv)


@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(bot, message):
    user_id = int(message.from_user.id)
    await insert(user_id)
    await message.reply_photo(photo=Rkn_Bots.RKN_PIC,
        caption=f"<b>Hey, {message.from_user.mention}\n\nI'm an auto-caption bot. I automatically edit captions for videos, audio files, and documents posted on channels.\n\nUse <code>/set_caption</code> to set caption\nUse <code>/delcaption</code> to delete caption and set caption to default.\n\nNote: All commands work on channels only</b>",
        reply_markup=types.InlineKeyboardMarkup([[
            types.InlineKeyboardButton('Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/RknDeveloper'),
            types.InlineKeyboardButton('Sᴜᴩᴩᴏʀᴛ', url='https://t.me/Rkn_Bots_Support')
            ],[
            types.InlineKeyboardButton('🔥 Source Code 🔥', url='https://github.com/RknDeveloper/Rkn-AutoCaptionBot')
    ]])
    )

@Client.on_message(filters.command("set_caption") & filters.channel)
async def setCap(bot, message):
    if len(message.command) < 2:
        return await message.reply(
            "Usage: /set_caption <code>your caption (use {file_name} to show file name</code>)"
        )
    chnl_id = message.chat.id
    caption = (
        message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
    )
    chkData = await chnl_ids.find_one({"chnl_id": chnl_id})
    if chkData:
        await updateCap(chnl_id, caption)
        return await message.reply(f"Your New Caption: {caption}")
    else:
        await addCap(chnl_id, caption)
        return await message.reply(f"Your New Caption: {caption}")

@Client.on_message(filters.command(["delcaption", "del_caption", "delete_caption"]) & filters.channel)
async def delCap(_, msg):
    chnl_id = msg.chat.id
    try:
        await chnl_ids.delete_one({"chnl_id": chnl_id})
        return await msg.reply("<b>Success..From now I will use my default caption</b>")
    except Exception as e:
        e_val = await msg.reply(f"ERR I GOT: {e}")
        await asyncio.sleep(5)
        await e_val.delete()
        return
        
@Client.on_message(filters.channel)
async def auto_edit_caption(bot, message):
    chnl_id = message.chat.id

    if message.caption:
        return
    if message.media_group_id:
        media_group_id = message.media_group_id
        media_group_messages = await bot.get_media_group(chat_id=message.chat.id, media_group_id=media_group_id)

        if media_group_messages:
            first_message = media_group_messages[0]
            if first_message.media:
                for file_type in ("video", "audio", "document", "voice", "photo"):
                    obj = getattr(first_message, file_type, None)
                    if obj and hasattr(obj, "file_name"):
                        file_name = obj.file_name
                        if file_name: 
                            file_name = (
                                re.sub(r"@\w+\s*", "", file_name)
                                .replace("_", " ")
                                .replace(".", " ")
                            )
                            cap_dets = await chnl_ids.find_one({"chnl_id": chnl_id})
                            try:
                                if cap_dets:
                                    cap = cap_dets["caption"]
                                    replaced_caption = cap.format(file_name=file_name)
                                    await first_message.edit_caption(replaced_caption)
                                else:
                                    replaced_caption = Rkn_Bots.DEF_CAP.format(file_name=file_name)
                                    await first_message.edit_caption(replaced_caption)
                            except FloodWait as e:
                                await asyncio.sleep(e.x)
                                continue
        return

    if message.media:
        for file_type in ("video", "audio", "document", "voice", "photo"):
            obj = getattr(message, file_type, None)
            if obj and hasattr(obj, "file_name"):
                file_name = obj.file_name
                if file_name: 
                    file_name = (
                        re.sub(r"@\w+\s*", "", file_name)
                        .replace("_", " ")
                        .replace(".", " ")
                    )
                    cap_dets = await chnl_ids.find_one({"chnl_id": chnl_id})
                    try:
                        if cap_dets:
                            cap = cap_dets["caption"]
                            replaced_caption = cap.format(file_name=file_name)
                            await message.edit_caption(replaced_caption)
                        else:
                            replaced_caption = Rkn_Bots.DEF_CAP.format(file_name=file_name)
                            await message.edit_caption(replaced_caption)
                    except FloodWait as e:
                        await asyncio.sleep(e.x)
                        continue
    return
