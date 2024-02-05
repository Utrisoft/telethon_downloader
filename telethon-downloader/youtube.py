import os
import time
from yt_dlp import YoutubeDL
from moviepy.editor import AudioFileClip


from logger import logger
from env import YOUTUBE_FORMAT, YOUTUBE_AUDIO_FORMAT, TG_DOWNLOAD_PATH, PATH_YOUTUBE


async def youtube_download_mp3(url, user, client):
    await client.send_message(entity=user, message=f'downloading...')

    try:
        youtube_path = PATH_YOUTUBE

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            file_name = ydl.prepare_filename(info_dict)
            total_downloads = 1
            if '_type' in info_dict and info_dict["_type"] == 'playlist':
                total_downloads = len(info_dict['entries'])
                logger.info('info_dict :::::::::::: [{}][{}]'.format(
                    info_dict["_type"], len(info_dict['entries'])))
                youtube_path = os.path.join(
                    PATH_YOUTUBE, info_dict['uploader'], info_dict['title'])
                ydl_opts = {'format': YOUTUBE_AUDIO_FORMAT,
                            'outtmpl': f'{youtube_path}/%(title)s.%(ext)s', 'cachedir': 'False', 'ignoreerrors': True, "retries": 10, 'merge_output_format': 'mp3'}
                ydl_opts.update(ydl_opts)
            else:
                # Comprobar si info_dict["uploader"] contiene la palara topic
                if 'topic' in info_dict["uploader"]:
                    file_name = f'{info_dict["title"]}.webm'
                else:
                    file_name = f'{info_dict["uploader"]} - {info_dict["title"]}.webm'
                youtube_path = os.path.join(
                    PATH_YOUTUBE)
                ydl_opts = {'format': YOUTUBE_AUDIO_FORMAT,
                            'outtmpl': f'{youtube_path}/%(title)s.%(ext)s', 'cachedir': 'False', 'ignoreerrors': True, "retries": 10, 'merge_output_format': 'mp3'}
                ydl_opts.update(ydl_opts)

        with YoutubeDL(ydl_opts) as ydl:
            logger.info(f'DOWNLOADING SONG YOUTUBE [{url}] [{file_name}]')
            await client.send_message(entity=user, message=f'downloading {total_downloads} song...')
            res_youtube = ydl.download([url])

            if (res_youtube == False):
                os.chmod(youtube_path, 0o777)
                file_path = f'{youtube_path}/{file_name}'
                mp3_file_path = file_path.replace('.webm', '.mp3')
                # Convertimos el webm a mp3
                convert_webm_to_mp3(file_path, mp3_file_path)

                # Borramos el webm
                os.remove(file_path)

                logger.info(
                    f'DOWNLOADED {total_downloads} SONG YOUTUBE [{file_name}] [{mp3_file_path}]')
                end_time_short = time.strftime('%H:%M', time.localtime())
                await client.send_message(entity=user, message=f'Downloading finished {total_downloads} song at {end_time_short}\n"{mp3_file_path}"')
            else:
                logger.info(
                    f'ERROR: ONE OR MORE YOUTUBE SONGS NOT DOWNLOADED [{total_downloads}] [{url}] [{youtube_path}]')
                await client.send_message(entity=user, message=f'ERROR: one or more songs not downloaded')
    except Exception as e:
        logger.info('ERROR: %s DOWNLOADING YT: %s' %
                    (e.__class__.__name__, str(e)))
        logger.info(
            f'ERROR: Exception ONE OR MORE YOUTUBE SONGS NOT DOWNLOADED')


def convert_webm_to_mp3(input_file, output_file):
    """
    Convert a WebM audio file to an MP3 audio file.

    Args:
        input_file (str): The path to the input WebM audio file.
        output_file (str): The path to the output MP3 audio file.

    Returns:
        None
    """
    audio = AudioFileClip(input_file)
    audio.write_audiofile(output_file)


async def youtube_download_mkv(url, user, client):
    await client.send_message(entity=user, message=f'downloading...')

    try:
        youtube_path = PATH_YOUTUBE

        ydl_opts = {'format': YOUTUBE_FORMAT,
                    'outtmpl': f'{youtube_path}/%(title)s.%(ext)s', 'cachedir': 'False', "retries": 10, 'merge_output_format': 'mkv'}

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            file_name = ydl.prepare_filename(info_dict)
            total_downloads = 1
            if '_type' in info_dict and info_dict["_type"] == 'playlist':
                total_downloads = len(info_dict['entries'])
                # logger.info('info_dict :::::::::::: [{}][{}]'.format(info_dict["_type"],len(info_dict['entries'])))
                youtube_path = os.path.join(
                    PATH_YOUTUBE, info_dict['uploader'], info_dict['title'])
                ydl_opts = {'format': YOUTUBE_FORMAT,
                            'outtmpl': f'{youtube_path}/%(title)s.%(ext)s', 'cachedir': 'False', 'ignoreerrors': True, "retries": 10, 'merge_output_format': 'mkv'}
                ydl_opts.update(ydl_opts)
            else:
                youtube_path = os.path.join(
                    PATH_YOUTUBE, info_dict['uploader'])
                ydl_opts = {'format': YOUTUBE_FORMAT,
                            'outtmpl': f'{youtube_path}/%(title)s.%(ext)s', 'cachedir': 'False', 'ignoreerrors': True, "retries": 10, 'merge_output_format': 'mkv'}
                ydl_opts.update(ydl_opts)

        with YoutubeDL(ydl_opts) as ydl:
            logger.info(f'DOWNLOADING VIDEO YOUTUBE [{url}] [{file_name}]')
            await client.send_message(entity=user, message=f'downloading {total_downloads} videos...')
            res_youtube = ydl.download([url])

            if (res_youtube == False):
                os.chmod(youtube_path, 0o777)
                filename = os.path.basename(file_name)
                logger.info(
                    f'DOWNLOADED {total_downloads} VIDEO YOUTUBE [{file_name}] [{youtube_path}][{filename}]')
                end_time_short = time.strftime('%H:%M', time.localtime())
                await client.send_message(entity=user, message=f'Downloading finished {total_downloads} video at {end_time_short}\n{youtube_path}')
            else:
                logger.info(
                    f'ERROR: ONE OR MORE YOUTUBE VIDEOS NOT DOWNLOADED [{total_downloads}] [{url}] [{youtube_path}]')
                await client.send_message(entity=user, message=f'ERROR: one or more videos not downloaded')
    except Exception as e:
        logger.info('ERROR: %s DOWNLOADING YT: %s' %
                    (e.__class__.__name__, str(e)))
        logger.info(
            f'ERROR: Exception ONE OR MORE YOUTUBE VIDEOS NOT DOWNLOADED')


async def youtube_download(url, download_video, user, client):
    if download_video:
        await youtube_download_mkv(url, user, client)
    else:
        await youtube_download_mp3(url, user, client)

# async def youtube_download(url, update, message):
#     try:
#         url = update.message.message
#         youtube_path = PATH_YOUTUBE

#         ydl_opts_mp3 = {
#             'format': 'bestaudio/best',
#             'postprocessors': [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }],
#         }

#         ydl_opts_mkv = {'format': YOUTUBE_FORMAT,
#                         'outtmpl': f'{youtube_path}/%(title)s.%(ext)s', 'cachedir': 'False', "retries": 10, 'merge_output_format': 'mkv'}

#         ydl_opts = ydl_opts_mkv

#         with YoutubeDL(ydl_opts) as ydl:
#             info_dict = ydl.extract_info(url, download=False)
#             file_name = ydl.prepare_filename(info_dict)
#             total_downloads = 1
#             if '_type' in info_dict and info_dict["_type"] == 'playlist':
#                 total_downloads = len(info_dict['entries'])
#                 # logger.info('info_dict :::::::::::: [{}][{}]'.format(info_dict["_type"],len(info_dict['entries'])))
#                 youtube_path = os.path.join(
#                     PATH_YOUTUBE, info_dict['uploader'], info_dict['title'])
#                 ydl_opts = {'format': YOUTUBE_FORMAT,
#                             'outtmpl': f'{youtube_path}/%(title)s.%(ext)s', 'cachedir': 'False', 'ignoreerrors': True, "retries": 10, 'merge_output_format': 'mkv'}
#                 ydl_opts.update(ydl_opts)
#             else:
#                 youtube_path = os.path.join(
#                     PATH_YOUTUBE, info_dict['uploader'])
#                 ydl_opts = {'format': YOUTUBE_FORMAT,
#                             'outtmpl': f'{youtube_path}/%(title)s.%(ext)s', 'cachedir': 'False', 'ignoreerrors': True, "retries": 10, 'merge_output_format': 'mkv'}
#                 ydl_opts.update(ydl_opts)

#         with YoutubeDL(ydl_opts) as ydl:
#             logger.info(f'DOWNLOADING VIDEO YOUTUBE [{url}] [{file_name}]')
#             await message.edit(f'downloading {total_downloads} videos...')
#             res_youtube = ydl.download([url])

#             if (res_youtube == False):
#                 os.chmod(youtube_path, 0o777)
#                 filename = os.path.basename(file_name)
#                 logger.info(
#                     f'DOWNLOADED {total_downloads} VIDEO YOUTUBE [{file_name}] [{youtube_path}][{filename}]')
#                 end_time_short = time.strftime('%H:%M', time.localtime())
#                 await message.edit(f'Downloading finished {total_downloads} video at {end_time_short}\n{youtube_path}')
#             else:
#                 logger.info(
#                     f'ERROR: ONE OR MORE YOUTUBE VIDEOS NOT DOWNLOADED [{total_downloads}] [{url}] [{youtube_path}]')
#                 await message.edit(f'ERROR: one or more videos not downloaded')
#     except Exception as e:
#         logger.info('ERROR: %s DOWNLOADING YT: %s' %
#                     (e.__class__.__name__, str(e)))
#         logger.info(
#             f'ERROR: Exception ONE OR MORE YOUTUBE VIDEOS NOT DOWNLOADED')
#
#
#
