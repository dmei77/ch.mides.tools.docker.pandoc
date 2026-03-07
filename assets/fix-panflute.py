"""Fix panflute SyntaxWarning with Python 3.12+ (invalid escape sequence in docstring)."""
import glob

for path in glob.glob("/*/panflute/io.py", recursive=False):
    pass

import os
for root, dirs, files in os.walk("/"):
    if root.endswith("/panflute") and "io.py" in files:
        filepath = os.path.join(root, "io.py")
        content = open(filepath).read()
        if "\\*" in content:
            content = content.replace("\\*", "*")
            open(filepath, "w").write(content)
            print(f"Fixed: {filepath}")
