from time import time
import shutil

import db_utils
from bot import bot
from userbot import post_large_track
from utils import already_downloading
from var import var
from logger import sent_message_logger
# import server_methods


async def send_track(track, chat_id, Redownload=False):
    quality = await db_utils.get_quality_setting(chat_id)
    if not already_downloading(track.id):
        var.downloading[track.id] = int(time())
    else:
        return
    if not Redownload:
        file_id = await db_utils.get_track(track.id, quality)
        if file_id:
            await bot.send_audio(chat_id, file_id)
            var.downloading.pop(track.id)
            sent_message_logger.info(
                f'[send track {track.id} to {chat_id}] {track}')
            return True

    # try:
    #     print(
    #         f'[Deezer_server] Start downloading: {track.id} |'
    #         f' {track.artist.name} - {track.title} ')
    #     await server_methods.send_track(track, chat_id, quality)
    #     var.downloading.pop(track.id)
    #     print(
    #         f'[Deezer_server] Finished downloading: {track.id} '
    #         f'| {track.artist.name} - {track.title} ')
    #     sent_message_logger.info(
    #         f'[send track {track.id} to {chat_id}] {track}')
    #     return True
    # except Exception:
    #     pass

    try:
        if quality == 'mp3':
            path = await track.download('MP3_320')
        elif quality == 'flac':
            path = await track.download('FLAC')
    except ValueError as e:
        print(e)
        await bot.send_message(
            chat_id,
            ("🚫This track is not available "
             f"({track.artist.name} - {track.title})"))
        raise

    await bot.send_chat_action(chat_id, 'upload_audio')

    thumb = await track.get_thumb()
    await post_large_track(path, track, quality, thumb=thumb)
    file_id = await db_utils.get_track(track.id, quality)
    await bot.send_audio(chat_id, file_id)
    shutil.rmtree(path.rsplit('/', 1)[0])
    var.downloading.pop(track.id)
    sent_message_logger.info(
        f'[send track {track.id} to {chat_id}] {track}')
    return True


async def send_album(album, chat_id):
    for track in await album.get_tracks():
        print(track.title)
        await send_track(track, chat_id)


async def send_playlist(tracks, chat_id):
    for track in tracks:
        try:
            await send_track(track, chat_id)
        except Exception:
            pass


async def cache(track):
    file_id = await db_utils.get_track(track.id)
    if not file_id:
        path = await track.download()
        await post_large_track(path, track)
        shutil.rmtree(path.rsplit('/', 1)[0])
        print(f'cached track {track.artist.name} - {track.title}')
    else:
        print(
            f'skipping track {track.artist.name} - {track.title} - {file_id}')