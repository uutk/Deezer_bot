from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from yarl import URL
from urllib.parse import quote

from config import spotify_client
from .spotify_api import REDIRECT_URL
from utils import encode_url


def auth_keyboard(user_id):
    url = URL('https://accounts.spotify_api.com/authorize').update_query({
        'client_id': spotify_client,
        'response_type': 'code',
        'redirect_uri': quote(REDIRECT_URL),
        'scope': 'user-read-currently-playing%20user-modify-playback-state',
        'state': user_id
    })
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text='Authorize', url=str(url)))
    return markup


def current_track_keyboard(track):
    markup = InlineKeyboardMarkup(2)
    markup.row(InlineKeyboardButton(
        text='Open track', url=track.external_urls.spotify))
    markup.row(InlineKeyboardButton(
        text='Download track',
        callback_data=f'spotify:download_track:{track.id}'))
    markup.row(
        InlineKeyboardButton(
            text='Album',
            callback_data=f'spotify:album:{track.album.id}'),
        InlineKeyboardButton(
            text='Artist',
            callback_data=f'spotify:artist:{track.artists[0].id}'))
    markup.row(
        InlineKeyboardButton(
            text='◀️',
            callback_data=f'spotify:previous_track'),
        InlineKeyboardButton(
            text='️️▶️',
            callback_data=f'spotify:next_track'))
    markup.row(InlineKeyboardButton(
        text='Update', callback_data='spotify:update_current'))
    markup.row(InlineKeyboardButton(
        text='Close', callback_data='delete'))
    return markup
