
# Build Instructions
pyinstaller --onefile --noconsole CopyHistory.py

# Optimization Techniques

## Memory limits
I kept track of the memory usage of images and files when an image was added and it went about the memory limit
I removed references until the memory limit was below 80% of the limit.

## Data Compression
I compressed images as they were stored and uncompressed them as needed to limit memory use in storage.

# Features
- Text copy history
- Image copy history
- File copy history
- Favoriting
- Paste last 5 items
- Paste last item
- Paste item at the end of the list