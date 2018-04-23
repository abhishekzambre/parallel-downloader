import os
import requests
import threading
import shutil
import urllib.request
import time
import math
import hashlib
# import crcmod


class Downloader:
    def __init__(self, url=None, number_of_threads=1):
        """Constructor of Downloader class
        :param url: URL of file to be downloaded (optional)
        :param number_of_threads: Maximum number of threads (optional)
        """
        self.url = url
        self.number_of_threads = number_of_threads
        self.file_size = self.get_file_size()
        self.if_byte_range = self.is_byte_range_supported()
        self.remote_md5 = self.get_remote_md5()
        self.if_contains_md5 = True if self.remote_md5 != -1 or self.remote_md5 is not None else False
        self.downloaded_md5 = None
        self.range_list = list()
        self.start_time = None
        self.end_time = None
        self.target_filename = os.path.basename(self.url)
        self.status_refresh_rate = 2
        self.download_durations = [None] * self.number_of_threads

    def get_url(self):
        """Returns URL of a file to be downloaded"""
        return self.url

    def set_url(self, url):
        """Set new URL of a file to be downloaded
        :param url: string
        """
        if not url:
            raise ValueError("URL field is empty")
        if not isinstance(url, str):
            raise TypeError("URL must be of string type")
        self.url = url

    def get_number_of_threads(self):
        """Returns maximum number of threads allowed"""
        return self.number_of_threads

    def set_number_of_threads(self, number_of_threads):
        """Set new maximum number of threads allowed (must be a positive number)
        :param number_of_threads: integer
        """
        if number_of_threads <= 0:
            raise ValueError("Number of maximum threads should be positive")
        if not isinstance(number_of_threads, int):
            raise TypeError("Number of maximum threads should be integer")
        self.number_of_threads = number_of_threads

    def get_file_size(self):
        """Get remote file size in bytes from url
        :return: integer
        """
        self.file_size = requests.head(self.url, headers={'Accept-Encoding': 'identity'}).headers.get('content-length', None)
        return int(self.file_size)

    def is_byte_range_supported(self):
        """Return True if accept-range is supported by the url else False
        :return: boolean
        """
        server_byte_response = requests.head(self.get_url(), headers={'Accept-Encoding': 'identity'}).headers.get('accept-ranges')
        if not server_byte_response or server_byte_response == "none":
            return False
        else:
            return True

    def is_contains_md5(self):
        return self.if_contains_md5

    def get_remote_md5(self):
        server_md5_response = requests.head(self.get_url(), headers={'Accept-Encoding': 'identity'}).headers.get(
            'x-goog-hash')
        if server_md5_response:
            response_split = server_md5_response.split(', ')
            for response in response_split:
                if response.startswith("md5"):
                    return response.split('=')[1]
        return None

    def start_download(self):

        self.build_range()

        self.clean_temp_dir()

        self.start_time = time.time()

        workers = list()

        for chunk_id, chunk_range in enumerate(self.range_list):
            workers.append(threading.Thread(target=self.download_chunk, args=(chunk_id, chunk_range)))

        for th in workers:
            th.start()

        print(self.get_status_header())
        while threading.active_count() > 1:
            print(self.get_download_status())
            time.sleep(self.status_refresh_rate)

        for th in workers:
            th.join()
        print(self.get_download_status())

        with open(self.target_filename, "ab") as target_file:
            for i in range(self.number_of_threads):
                with open("temp/part" + str(i), "rb") as chunk_file:
                    target_file.write(chunk_file.read())

        self.end_time = time.time()

    def clean_temp_dir(self):
        if os.path.isdir("temp"):
            shutil.rmtree("temp")
        os.makedirs("temp")

    def download_chunk(self, chunk_id, chunk_range):
        """Download chunk of a file by providing byte range in download header
        :param chunk_id: Chunk id to maintain order
        :param chunk_range: Byte range of a chunk to be downloaded
        :return:
        """
        req = urllib.request.Request(self.get_url())
        req.headers['Range'] = 'bytes={}'.format(chunk_range)
        with urllib.request.urlopen(req) as response, open('temp/part' + str(chunk_id), 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        self.download_durations[chunk_id] = time.time()

    def get_status_header(self):
        """Returns header for the download status"""
        status_header = list()
        for i in range(self.number_of_threads):
            status_header.append("chunk" + str(i+1))
        return '\t\t'.join(status_header)

    def get_download_status(self):
        """Returns current download status per thread in string format
        :return: string
        """
        download_status = list()
        for i in range(self.number_of_threads):
            if os.path.isfile("temp/part" + str(i)):
                download_status.append(str(round(os.stat("temp/part" + str(i)).st_size/(self.file_size/self.number_of_threads) * 100, 2)) + "%")
            else:
                download_status.append("0.00%")
        return '\t\t'.join(download_status)

    def get_downloaded_md5(self):
        BLOCKSIZE = 65536
        md5 = hashlib.md5()
        with open(self.target_filename, 'rb') as target_file:
            buf = target_file.read(BLOCKSIZE)
            while len(buf) > 0:
                md5.update(buf)
                buf = target_file.read(BLOCKSIZE)
        print(md5.hexdigest())
        self.downloaded_md5 = md5.hexdigest()
        # print(self.downloaded_md5)

    def check_integrity(self):
        self.get_downloaded_md5()
        return self.remote_md5 == self.downloaded_md5

    def build_range(self):
        """Creates the list of byte-range to be downloaded by each thread.
        Total file size is divided by maximum limit of a thread
        """
        i = 0
        chunk_size = int(math.ceil(int(self.file_size) / int(self.number_of_threads)))
        for _ in range(self.number_of_threads):
            if(i + chunk_size) < self.file_size:
                entry = '%s-%s' % (i, i + chunk_size - 1)
            else:
                entry = '%s-%s' % (i, self.file_size)
            i += chunk_size
            self.range_list.append(entry)

    def get_target_filename(self):
        """Returns the target file name"""
        return self.target_filename

    def get_metadata(self):
        return {
            "url": self.url,
            "number_of_threads": self.number_of_threads,
            "file_size": self.file_size,
            "if_byte_range": self.if_byte_range,
            "if_contains_md5": self.if_contains_md5,
            "remote_md5": self.remote_md5,
            "downloaded_md5": self.downloaded_md5,
            "range_list": self.range_list
        }


if __name__ == '__main__':
    obj = Downloader("https://storage.googleapis.com/vimeo-test/work-at-vimeo-2.mp4", 10)

    # obj = Downloader("http://i.imgur.com/z4d4kWk.jpg", 3)

    obj.start_download()

    print(obj.get_metadata())
    obj.get_downloaded_md5()
