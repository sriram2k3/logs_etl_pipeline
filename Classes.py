from abc import ABC, abstractmethod
import requests
from datetime import datetime
import ipaddress
import mysql.connector
from collections import Counter
import os
from dotenv import load_dotenv

# base class to make source check dynamic for any kinda source .txt or url
class LogSource(ABC):
    @abstractmethod
    def fetch_log(self):
        pass

# file fetch class
class FileLogSource(LogSource):
    def __init__(self, filepath):
        self.filename = filepath
    def fetch_log(self):
        try:
            with open(self.filename,"r") as file:
                for line in file:
                    yield line.strip()
        except Exception as e:
            raise e
#url fetch class
class UrlLogSource(LogSource):
    def __init__(self, url):
        self.path = url
    def fetch_log(self):
        try:
            response = requests.get(self.path,stream = True)
            if response.status_code != 200:
                raise Exception(response.status_code)

            for line in response.iter_lines(decode_unicode = True):
                if line:
                    yield line.strip()
            return None
        except Exception as e:
            raise e

# Parsing Log
class LogRecord:
    def __init__(self, line):
        self.line = line
        self.timestamp = datetime.now()
        self.ip = ""
        self.status = ""
        self.to_parse = self.parse()

    def parse(self):
        try:
            self.line = self.line.split()
            self.timestamp = datetime.fromisoformat(self.line[0] + " " + self.line[1]).strftime('%Y-%m-%d %H:%M:%S')
            self.status = self.line[2]
            self.ip = ipaddress.ip_address(self.line[3])
            return None
        except ValueError as e:
            raise e
    def is_blocked(self):
        return self.status.lower() == "block"

# storing record objects
class Collection:
    def __init__(self):
        self.log = None
        self.logs = []
        self.blocked_ips = {}

    def add_log(self,log):
        self.log = log
        if isinstance(self.log, LogRecord):
            self.logs.append(self.log)
        return None

    def top_blocked_ips(self,num):
        blocked_ips = Counter(
            log.ip for log in self.logs if log.is_blocked()
        )
        return blocked_ips.most_common(num)

class DbLoader:
    load_dotenv()

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connection = self._get_connection()
    def _get_connection(self):
        self.conn = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            database = os.getenv("DB_DATABASE")
        )
        print("Connection established...\n")
        return self.conn

    def add_data(self, collection: list):
        self.cursor = self.connection.cursor()
        query = "INSERT INTO logs VALUES (%s,%s,%s)"
        try:
            for log in collection:
                self.cursor.execute(query, (log.timestamp, log.status, str(log.ip)))
        except Exception as e:
            raise e
        finally:
            print("Logs Loaded to MySQL DB Successfully !!!")
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

