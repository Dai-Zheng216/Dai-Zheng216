from pathlib import Path
import hashlib
import re

root = Path(__file__).resolve().parents[2]
readme = root / "README.md"
text = readme.read_bytes().decode("utf-8")
pattern = re.compile(r'(https://raw\.githubusercontent\.com/[^/]+/[^/]+/[^/]+/dist/(github-contribution-grid-snake(?:-dark)?\.svg))(?:\?[^"\s<>]*)?')

def versioned(match):
    svg = root / "dist" / match.group(2)
    version = hashlib.sha256(svg.read_bytes()).hexdigest()[:16]
    return match.group(1) + "?v=" + version

updated, count = pattern.subn(versioned, text)
if count != 3:
    raise RuntimeError(f"Expected 3 snake image references, found {count}")
if updated != text:
    readme.write_bytes(updated.encode("utf-8"))
print(f"Updated {count} snake image references with content versions")
