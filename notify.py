import json
import mimetypes
import os
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parent
WEBHOOK = os.environ.get('DISCORD_WEBHOOK_URL', '').strip()
if not WEBHOOK.startswith('https://discord.com/api/webhooks/') and not WEBHOOK.startswith('https://discordapp.com/api/webhooks/'):
    raise SystemExit('Missing or invalid DISCORD_WEBHOOK_URL secret.')

config = json.loads((ROOT / 'config.json').read_text(encoding='utf-8'))
message = config.get('message', '').strip()
if not message:
    raise SystemExit('config.json message must not be empty.')

content = '@everyone\n' + message
if len(content) > 2000:
    raise SystemExit('Discord message exceeds 2000 characters.')

payload = {'content': content, 'allowed_mentions': {'parse': ['everyone']}}
image_name = config.get('image_file', '').strip()
image_path = ROOT / 'assets' / image_name if image_name else None

if image_name:
    if Path(image_name).name != image_name or not image_path.is_file():
        raise SystemExit('Image must be a file inside assets/.')
    if image_path.stat().st_size > 8 * 1024 * 1024:
        raise SystemExit('Image exceeds the conservative 8 MB size limit.')
    boundary = 'discord-weekly-notifier-boundary'
    mime = mimetypes.guess_type(image_name)[0] or 'application/octet-stream'
    data = (f'--{boundary}\r\nContent-Disposition: form-data; name="payload_json"\r\nContent-Type: application/json\r\n\r\n'.encode()
            + json.dumps(payload, ensure_ascii=False).encode() + b'\r\n'
            + f'--{boundary}\r\nContent-Disposition: form-data; name="files[0]"; filename="{image_name}"\r\nContent-Type: {mime}\r\n\r\n'.encode()
            + image_path.read_bytes() + b'\r\n'
            + f'--{boundary}--\r\n'.encode())
    headers = {'Content-Type': f'multipart/form-data; boundary={boundary}', 'User-Agent': 'WeeklyDiscordNotifier/1.0'}
else:
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    headers = {'Content-Type': 'application/json', 'User-Agent': 'WeeklyDiscordNotifier/1.0'}

try:
    with urlopen(Request(WEBHOOK + ('&' if '?' in WEBHOOK else '?') + 'wait=true', data=data, headers=headers, method='POST'), timeout=30) as response:
        print('Discord message sent successfully (HTTP %s).' % response.status)
except HTTPError as e:
    raise SystemExit(f'Discord request failed (HTTP {e.code}). Check webhook permissions and configuration.') from e
