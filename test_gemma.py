import urllib.request, json, re

with open(".env") as f:
    content = f.read()

match = re.search(r"GOOGLE_API_KEY\s*=\s*(.+)", content)
key = match.group(1).strip().strip(chr(34))

req = urllib.request.Request(
    "https://generativelanguage.googleapis.com/v1beta/models/gemma-4-26b-a4b-it:generateContent?key=" + key,
    data=json.dumps({"contents":[{"parts":[{"text":"Reply with exactly: gemma-ready"}]}]}).encode(),
    headers={"Content-Type":"application/json"}
)
try:
    print(urllib.request.urlopen(req).read().decode()[:500])
except urllib.error.HTTPError as e:
    print(e.read().decode()[:500])
