# Parallel Downloader

Python application to download large file in chunks using parallel threads.

Below functions are performed by the application.

- [x] Check if the file server supports byte range GET requests.
- [x] If byte range GET is supported, download multiple chunks of the file in parallel.
- [x] If byte range GET is not supported, download the whole file at once.
- [x] If the file was downloaded in multiple chunks, those chunks must be put back together in the correct order and result in a playable video.
- [x] Handling of errors and retries.
- [x] Check downloaded file for integrity.
- [x] Benchmarks for various chunk sizes for parallel downloads.
- [x] Limiting the number of concurrent chunks being downloaded to some maximum value.
- [x] Resuming partially-downloaded chunks on error.
- [ ] Calculating checksum for integrity check during download rather than at the end.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them.

###### python3

Download and install [python3](https://www.python.org/downloads/) (version: 3.6.5).

###### python3 modules

Below is the dependency modules list.

- os
- requests
- threading
- shutil
- queue
- urllib.request
- time
- math
- hashlib
- [crcmod](https://github.com/gsutil-mirrors/crcmod)

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

## Implementation

TBD

## Future Scope

- Custom download location.
- Graphical User Interface using libraries such as [Tkinter](https://wiki.python.org/moin/TkInter) or [Kivy](https://kivy.org/)
- Support for variety of integrity check algorithms.

## Authors

* **Abhishek Zambre** - [abhiz.me](http://abhiz.me)

