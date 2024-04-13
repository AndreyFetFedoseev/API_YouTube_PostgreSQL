from typing import Any

from googleapiclient.discovery import build


def get_youtube_data(key: str, channel_ids: list[str]) -> list[dict[str, Any]]:
    youtube = build('youtube', 'v3', developerKey=key)

    data = []
    data_videos = []
    next_page_token = None
    for channel_id in channel_ids:
        channel_data = youtube.channels().list(part='snippet, statistics', id=channel_id).execute()
        while True:
            channel_video = youtube.search().list(part='snippet,id', channelId=channel_id, type='video', order='date',
                                                  maxResults=50, pageToken=next_page_token).execute()
            data_videos.extend(channel_video['items'])

            next_page_token = channel_video.get('nextPageToken')
            if not next_page_token:
                break
        data.append(
            {'channel': channel_data['items'][0],
             'videos': data_videos}
        )
    return data


def create_database(database_name: str, params: dict) -> None:
    pass


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    pass
