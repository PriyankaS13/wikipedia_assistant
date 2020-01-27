import os
import unittest

import mysql.connector

from download_utils import DownloadLatest
from load_data import LoadMonthlyData


class TestPreprocessing(unittest.TestCase):
    def test_invalid_url(self):
        with self.assertRaises(Exception) as context:
            downloads = DownloadLatest(config='app.ini', section='test_url')

    def test_invalid_file_path(self):
        with self.assertRaises(Exception) as context:
            downloads = DownloadLatest(config='app.ini', section='test_files')

    def test_db(self):
        with self.assertRaises(Exception) as context:
            downloads = LoadMonthlyData(config='app.ini', section='test_db')

    def test_directory_delete(self):
        d = DownloadLatest()
        d.cleanup_download_path(d.download_path)
        self.assertFalse(os.path.exists(d.download_path), "Path not cleared")

    def test_download_file(self):
        d = DownloadLatest(section="test_download")
        d.get_latest_files()
        full_path = os.path.join(d.download_path, "".join(d.files))
        self.assertTrue(os.path.isfile(full_path), "File not downloaded")

    def test_table_creation(self):
        d = DownloadLatest(section="test_download")
        l = LoadMonthlyData(section="test_download")
        d.get_latest_files()
        l.upload_data(d.download_path, d.files)
        fn = "".join(d.files)
        tbl = fn.split("-")[2].split(".")[0]
        conn = mysql.connector.connect(host=l.host, user=l.user, password=l.password,
                                db=l.db, port=3306)
        cursor = conn.cursor()
        cursor.execute(f"select count(1)as record_cnt from {tbl}")
        row = cursor.fetchone()
        self.assertGreater(row[0], 1)
        conn.close()


if __name__ == '__main__':
    unittest.main()
