from download_utils import DownloadLatest
from load_data import LoadMonthlyData
import logging
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('preprocessor.log')
logger.addHandler(fh)


def main():
    downloads = DownloadLatest()
    load = LoadMonthlyData()
    logger.info("calling utility to download latest file from wiki dump")
    load.create_db()
    downloads.get_latest_files()
    load.upload_data(downloads.download_path, downloads.files)
    load.pre_compute_tables()


if __name__ == "__main__":
    main()
