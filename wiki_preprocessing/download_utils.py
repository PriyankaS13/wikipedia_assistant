import configparser
import wget
import os
import shutil
import logging
logger = logging.getLogger(__file__)


class DownloadLatest:
    def __init__(self, config='app.ini', section='Prod'):
        parser = configparser.ConfigParser()
        parser.read(config)
        self.base_url = parser.get(section, "base_url", fallback=None)
        if not self.base_url:
            raise Exception("Url section is incorrect")
        file = parser.get(section, "files", fallback=None)
        if not file:
            raise Exception("file list is not defined")
        self.files = file.split(",")
        self.download_path = parser.get(section, "path", fallback=None)
        if not self.download_path:
            raise Exception("download path is missing")

    def get_latest_files(self):
        '''
        1. Clean up download directory
        2. Create download directory
        3. Download latest files from wiki dump
        :return:
        '''
        logger.info("Deleting older dumps")
        self.cleanup_download_path(self.download_path)
        self.create_download_dir(self.download_path)
        logger.info("starting download of dumps")
        for file in self.files:
            complete_url = self.base_url + file
            self.download_file(complete_url, self.download_path)

    def cleanup_download_path(self, path_to_download):
        '''
        Deleting the download dir including files
        :param path_to_download:
        :return:
        '''
        try:
            if os.path.exists(path_to_download):
                shutil.rmtree(path_to_download)
                logger.info("Deleting directory")
        except Exception as e:
            logger.error(f"Error while deleting older dumps {e.args}")
            raise e

    def create_download_dir(self, path_to_download):
        '''
         creates path_to_download directory
        :param path_to_download:
        :return:
        '''
        try:
            if not os.path.exists(path_to_download):
                os.makedirs(path_to_download)
        except Exception as e:
            logger.debug(f"Error while creating download folder {e.args}")
            raise e

    def download_file(self, url, download_path):
        '''
        Downloads latest files from the url provided and places in the download path
        :param url:
        :param download_path:
        :return:
        '''
        try:
            logger.info(f"starting download of {url} into {download_path}")
            wget.download(url, download_path)
        except Exception as e:
            logger.debug(f"Error while downloading monthly dumps {e.args}")
            raise e
