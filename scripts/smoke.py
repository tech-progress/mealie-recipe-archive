import hashlib
import json
import os
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


BASE = f"http://127.0.0.1:{os.environ['LOCAL_PORT']}"


def request(path, method="GET", data=None, token=None, content_type=None, expected=(200,)):
    headers = {"Origin": BASE}
    if isinstance(data, dict):
        content_type = "application/json"
        data = json.dumps(data).encode()
    if content_type:
        headers["Content-Type"] = content_type
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = urllib.request.urlopen(urllib.request.Request(BASE + path, data=data, method=method, headers=headers), timeout=60)
    except urllib.error.HTTPError as error:
        response = error
    body = response.read()
    assert response.code in expected, (method, path, response.code, body[:500])
    return body


def compose(*args, input_data=None):
    return subprocess.run(["docker", "compose", *args], input=input_data, check=True, stdout=subprocess.PIPE, timeout=900).stdout


def login(email, password, expected=(200,)):
    body = urllib.parse.urlencode({"username": email, "password": password}).encode()
    result = request("/api/auth/token", "POST", body, content_type="application/x-www-form-urlencoded", expected=expected)
    return json.loads(result).get("access_token")


def retained(token, slug, image_path, expected_digest):
    recipe = json.loads(request(f"/api/recipes/{slug}", token=token))
    assert recipe["name"] == "Railway archive soup"
    image = request(image_path, token=token)
    assert hashlib.sha256(image).hexdigest() == expected_digest
    request(image_path, expected=(401, 403))
    request(f"/api/recipes/{slug}", expected=(401, 403))


source_notice = json.loads(request("/api/template-source"))
assert source_notice["recipeSource"] == "https://github.com/tech-progress/mealie-recipe-archive/tree/v" + Path("VERSION").read_text().strip()
assert source_notice["upstreamSource"].endswith("/v3.28.0")
login("changeme@example.com", "MyPassword", expected=(400, 401, 403))
token = login(os.environ["MEALIE_ADMIN_EMAIL"], os.environ["MEALIE_ADMIN_PASSWORD"])
assert token
source = {"@context": "https://schema.org", "@type": "Recipe", "name": "Railway archive soup", "description": "Controlled portable recipe fixture", "recipeIngredient": ["1 cup water", "1 carrot"], "recipeInstructions": [{"@type": "HowToStep", "text": "Simmer the ingredients."}]}
slug = json.loads(request("/api/recipes/create/html-or-json", "POST", {"data": json.dumps(source)}, token=token, expected=(200, 201)))
png = compose("exec", "-T", "app", "/opt/mealie/bin/python", "-c", "from PIL import Image; import io,sys; stream=io.BytesIO(); Image.new('RGB',(160,120),'orange').save(stream,format='PNG'); sys.stdout.buffer.write(stream.getvalue())")
boundary = "railway-recipe-image-boundary"
multipart = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"extension\"\r\n\r\npng\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"fixture.png\"\r\nContent-Type: image/png\r\n\r\n".encode() + png + f"\r\n--{boundary}--\r\n".encode())
request(f"/api/recipes/{slug}/image", "PUT", multipart, token=token, content_type=f"multipart/form-data; boundary={boundary}")
recipe = json.loads(request(f"/api/recipes/{slug}", token=token))
image_path = f"/api/media/recipes/{recipe['id']}/images/original.webp"
digest = hashlib.sha256(request(image_path, token=token)).hexdigest()
retained(token, slug, image_path, digest)
group = json.loads(request("/api/admin/groups", "POST", {"name": "Isolated qualification group"}, token=token, expected=(201,)))
household = json.loads(request("/api/admin/households", "POST", {"name": "Isolated household", "groupId": group["id"]}, token=token, expected=(201,)))
other_password = os.urandom(16).hex()
request("/api/admin/users", "POST", {"username": "isolated", "email": "isolated@example.invalid", "fullName": "Isolated", "password": other_password, "group": group["name"], "household": household["name"], "admin": False}, token=token, expected=(201,))
other_token = login("isolated@example.invalid", other_password)
request(f"/api/recipes/{slug}", token=other_token, expected=(403, 404))
request(image_path, token=other_token, expected=(403, 404))
print("PASS: upstream default login rejected; generated login; controlled schema.org import; retained image; anonymous and cross-group recipe/media denial")
compose("restart", "app")
compose("up", "-d", "--wait", "--wait-timeout", "300")
retained(token, slug, image_path, digest)
print("PASS: recipe, image bytes and authentication survive restart")
request("/api/admin/backups", "POST", token=token, expected=(201,))
backups = json.loads(request("/api/admin/backups", token=token))["imports"]
assert backups
backup_name = backups[0]["name"]
compose("cp", f"app:/app/data/backups/{backup_name}", ".local/portable-backup.zip")
backup = Path(".local/portable-backup.zip").read_bytes()
compose("down", "--volumes")
restore_code = "from pathlib import Path; import sys; Path('/tmp/restore.zip').write_bytes(sys.stdin.buffer.read()); from mealie.db.init_db import main; main(); from mealie.services.backups_v2.backup_v2 import BackupV2; BackupV2().restore(Path('/tmp/restore.zip'))"
compose("run", "--rm", "--no-deps", "-T", "--entrypoint", "/opt/mealie/bin/python", "app", "-c", restore_code, input_data=backup)
compose("up", "-d", "--wait", "--wait-timeout", "300")
token = login(os.environ["MEALIE_ADMIN_EMAIL"], os.environ["MEALIE_ADMIN_PASSWORD"])
retained(token, slug, image_path, digest)
other_token = login("isolated@example.invalid", other_password)
request(image_path, token=other_token, expected=(403, 404))
login("changeme@example.com", "MyPassword", expected=(400, 401, 403))
print("PASS: native portable ZIP restored into a newly created empty volume; recipe/image digest/users/access retained; default credentials remain rejected")
