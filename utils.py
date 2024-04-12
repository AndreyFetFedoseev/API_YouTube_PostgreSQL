from typing import Any

from googleapiclient.discovery import build

def get_youtube_data(key: str, channel_ids: list[str]) -> list[dict[str, Any]]:

    youtube = build('youtube', 'v3', developerKey=API_KEY)

    request = youtube.channels().list(
        part="snippet",
        id="UClQ5yO2ZLZIs_Ii7J-C57ww"
    )
    response = request.execute()


def create_database(database_name:str, params: dict) -> None:
    pass


def save_data_to_database(data:list[dict[str, Any]], database_name:str, params: dict) -> None:
    pass
