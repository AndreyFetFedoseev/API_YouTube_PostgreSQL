import os

from config import config
from utils import get_youtube_data, create_database, save_data_to_database


def main():
    API_KEY = os.getenv('API_KEY')

    params = config()

    channel_ids = [
        'UCepPgPC1WzzWcjcrzU_vqcg',  # AISPIK
        # 'UClQ5yO2ZLZIs_Ii7J-C57ww',  # Апполинария Гордиенко
        'UCECdSNRGBOi5im0sfZvlkIg'  # fct-altai
    ]

    data = get_youtube_data(API_KEY, channel_ids)
    create_database('youtube', params)
    save_data_to_database(data, 'youtube', params)


if __name__ == '__main__':
    main()
