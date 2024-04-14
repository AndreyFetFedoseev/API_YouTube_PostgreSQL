from typing import Any
from googleapiclient.discovery import build
import psycopg2


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
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=f'{database_name}', **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE channel (
                channel_id SERIAL PRIMARY KEY,
                title VARCHAR(150) NOT NULL,
                views INT,
                subscribers INT,
                videos INT,
                channel_url TEXT
            )
        """)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE videos (
                video_id SERIAL PRIMARY KEY,
                channel_id INT REFERENCES channel(channel_id),
                title VARCHAR NOT NULL,
                publish_date DATE,
                video_url TEXT
            )
        """)
    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for channel in data:
            channel_stat = channel['channel']['statistics']
            cur.execute("""
                INSERT INTO channel (title, views, subscribers, videos, channel_url)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING channel_id
                """,
                        (channel['channel']['snippet']['title'], channel_stat['viewCount'],
                         channel_stat['subscriberCount'], channel_stat['videoCount'],
                         f"https://wwww.youtube.com/channel/{channel_stat['channel']['id']}")
                        )
            channel_id = cur.fetchone()[0]  # (1,)
            videos_data = channel['videos']
            for video in videos_data:
                cur.execute("""
                                INSERT INTO videos (channel_id, title, publish_date, video_url)
                                VALUES (%s, %s, %s, %s)
                                """,
                            (channel_id, video['snippet']['title'], video['publish_date'],
                             f"https://wwww.youtube.com/watch?v={video['id']['videoId']}")
                            )
    conn.commit()
    conn.close()
