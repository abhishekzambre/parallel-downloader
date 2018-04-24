# Parallel Downloader

Python application to download large file in chunks using parallel threads.

##### Features list

- Check if the file server supports byte range GET requests.
- If byte range GET is supported, download multiple chunks of the file in parallel.
- If byte range GET is not supported, download the whole file at once.
- If the file was downloaded in multiple chunks, those chunks must be put back together in the correct order and result in a playable video.
- Handling of errors and retries.
- Check downloaded file for integrity.
- Benchmarks for various chunk sizes for parallel downloads.
- Limiting the number of concurrent chunks being downloaded to some maximum value.
- Resuming partially-downloaded chunks on error.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

Below are the prerequisites for this application.

##### python3

Download and install [python3](https://www.python.org/downloads/).

##### python3 modules

Below is the dependency modules list. Please make sure modules are installed and working properly.

- [os](https://docs.python.org/3/library/os.html)
- [sys](https://docs.python.org/3/library/sys.html)
- [requests](http://docs.python-requests.org/en/master/)
- [threading](https://docs.python.org/3/library/threading.html)
- [shutil](https://docs.python.org/3/library/shutil.html)
- [urllib.request](https://docs.python.org/3/library/urllib.request.html)
- [timeit](https://docs.python.org/3/library/timeit.html)
- [time](https://docs.python.org/3/library/time.html)
- [math](https://docs.python.org/3/library/math.html)
- [base64](https://docs.python.org/3/library/base64.html)
- [queue](https://docs.python.org/3/library/queue.html)
- [crcmod](https://github.com/gsutil-mirrors/crcmod)

Please note, all the modules come prepackaged with python3 except for 'crcmod' module.

## Executing the script

Execute script with arguments as follows.

- url: URL of a remote file to be downloaded.
- threads: Number of parallel threads.

For example:
```
python3 main.py -url "https://storage.googleapis.com/vimeo-test/work-at-vimeo-2.mp4" -threads 10
```

## Verifying the output

After successful execution, the file will be downloaded in the same directory from which the script is executed.

Check script output for performance and benchmark results.

## Implementation details

- Created 'Downloader' class.
- Important class variables include remote file's URL, number of threads, remote file size, remote file's checksum etc.
- The header will be requested from the remote server, to check multiple parameters (e.g. byte range support, checksum etc).
- If remote server does not support byte range GET requests, the entire file will be downloaded.
- If remote server supports byte range GET requests, a certain number of threads will be created.
- For each chunk of a file, a chunk id and byte range will be added to the queue.
- Each thread will pick up a job from the queue and will start downloading.
- If download thread gets an error (IOError), the job will be put back into the queue, with 'was_interrupted' flag.
- After picking up job from the queue and if 'was_interrupted' flag is set, the thread will check for the partial file.
- If a partial file is found, the thread will start downloading from chunk byte range + partial file size.
- If 'was_interrupted' flag is not set, the thread will download chunk normally.
- All threads will run till queue is not empty.
- During each download, durations will be stored for each thread.
- Once all chunks are downloaded, they will be merged into a single file.
- If the remote file has a checksum, the downloaded file's checksum will be calculated to perform the integrity check.
- Finally, benchmark results will be calculated and displayed.

## Future Scope

- Calculating checksum for integrity check during download rather than at the end.
- Graphical User Interface using libraries such as [Tkinter](https://wiki.python.org/moin/TkInter) or [Kivy](https://kivy.org/).
- Support for the variety of integrity check algorithms, currently only Google Cloud crc32c is supported.

## Authors

* **Abhishek Zambre** - [abhiz.me](http://abhiz.me)
