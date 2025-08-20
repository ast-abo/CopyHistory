# Build Instructions
## Windows/Linux
```
git clone https://github.com/ast-abo/CopyHistory
cd CopyHistory
pyinstaller --onefile --noconsole src/CopyHistory.py
cd dist
CopyHistory.exe
```

# Features
- Text copy history
- Image copy history
- File copy history
- Favoriting (F to favorite up to 5 per tab)
- Paste last 5 items (Ctrl + Alt + 5)
- Paste last text (Ctrl + Alt + v) 
- Copy last text (Ctrl + Alt + c)

# Optimization Techniques

## Memory limits
Cleared arrays to free up memory when it hit the hard limit.

## Data Compression
Image compression in order to minimize the amount of memory used per image.
