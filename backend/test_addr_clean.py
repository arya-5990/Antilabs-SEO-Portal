import re
import sys

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

addr = " No-contact delivery   Plot No, 1133, AB Rd, in front of DPS School, Rau, Indore, Madhya Pradesh 453331"

# Filter out Private Use Area (PUA) unicode characters
addr_clean = "".join(c for c in addr if not (0xE000 <= ord(c) <= 0xF8FF))

# Clean up other potential icon symbols
addr_clean = re.sub(r'[^\w\s,.-]', '', addr_clean)

# Strip leading spaces
addr_clean = addr_clean.strip()

# Strip leading status indicators
addr_clean = re.sub(r'^\s*(No-contact delivery|Dine-in|Takeout|Delivery|Open|Closed)\b\s*', '', addr_clean, flags=re.I)

# Strip leading spaces/separators again
addr_clean = re.sub(r'^[^\w\s]*', '', addr_clean).strip()

print("Cleaned Address:", addr_clean)
