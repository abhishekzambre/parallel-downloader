# Parallel Downloader

Python application to download large file in chunks using parallel threads.

Below functions are performed by the application.

1. Check if the file server supports byte range GET requests
   - If so, download multiple chunks of the file in parallel, otherwise download the whole file at once.
   - If the file was downloaded in multiple chunks, those chunks must be put back together in the correct order and result in a playable video.
2. Handle errors and retries.
3. Check downloaded file for integrity.

Additionally, below bonus functions are performed as well.

1. Benchmarks for various chunk sizes for parallel downloads.
2. Limiting the number of concurrent chunks being downloaded to some maximum value.
3. Resuming partially-downloaded chunks on error.
4. Calculating checksum for integrity check during download rather than at the end.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them.
