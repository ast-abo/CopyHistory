# Dependencies
- Pyinstaller
-- pip install pyinstaller


# Build Instructions
## Windows/Linux
```
git clone https://github.com/ast-abo/CopyHistory
cd CopyHistory
pyinstaller --onefile --noconsole src/CopyHistory.py
cd dist
CopyHistory.exe
```

## Mac
```
git clone https://github.com/ast-abo/CopyHistory
cd CopyHistory
pyinstaller --onefile --noconsole src/CopyHistory.py
cd dist
./CopyHistory
```

# Features
- Text copy history
- Image copy history
- File copy history
- Favoriting (F to favorite)
- Paste last 5 items (Ctrl + Alt + 5)
- Paste last text (Ctrl + Alt + v) 
- Copy last text (Ctrl + Alt + c)

# Optimization Techniques

## Memory limits
I kept track of the memory usage of images and files when an image was added and it went about the memory limit
I removed references until the memory limit was below 80% of the limit.

## Data Compression
I compressed images as they were stored and uncompressed them as needed to limit memory use in storage.