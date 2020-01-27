from configparser import ConfigParser
import os
import logging
logger = logging.getLogger(__file__)


class LoadMonthlyData:

    def __init__(self, config='app.ini', section="Prod"):
        parser = ConfigParser()
        parser.read(config)
        self.host = parser.get(section, "db_host", fallback=None)
        if not self.host:
            raise Exception("invalid host name")
        self.user = parser.get(section, "db_user", fallback=None)
        if not self.user:
            raise Exception("invalid user")
        self.db = parser.get(section, "db_name", fallback=None)
        if not self.db:
            raise Exception("invalid database name")
        self.password = os.environ.get('db_password', None)
        if not self.password:
            raise Exception("invalid db password")
        sql = parser.get(section, "sql", fallback=None)
        if not sql:
            raise Exception("no files to execute")
        self.sql_files = sql.split(",")

        self.create_db_sql = parser.get(section, "create_db_sql", fallback=None)
        if not self.create_db_sql:
            raise Exception("no files to execute")

    def upload_data(self, file_path, files):
        try:
            logger.info("uploading monthly feed to db")
            for file in files:
                full_path = os.path.join(file_path, file)
                upload_cmd = f"gunzip < {full_path}| mysql -h{self.host} -u{self.user} -p{self.password} -D {self.db}"
                os.system(upload_cmd)
        except Exception as e:
            logger.debug(f"Error while uploading data {e.args}")
            raise e

    def pre_compute_tables(self):
        logger.info("Pre computing most outdated page for top 10 categories")
        for queries in self.sql_files:
            try:
                cmd = f"mysql -h{self.host} -u{self.user} -p{self.password} -D {self.db}<{queries}"
                os.system(cmd)
            except Exception as e:
                logger.debug(f"Error occurred while pre computing data {e.args}")
                raise e

    def create_db(self):
        try:
            cmd = f"mysql -h{self.host} -u{self.user} -p{self.password} < {self.create_db_sql}"
            os.system(cmd)
        except Exception as e:
            logger.debug(f"Error occurred while creating DB {e.args}")
            raise e

