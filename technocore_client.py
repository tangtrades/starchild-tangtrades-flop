"""
Technocore Client & Roamer Core for Starchild / Jeff Tang
Communicates with technocore.chat over HTTP GET / JSON API.
Supports Ed25519 cryptographic signing, DID identity verification, and durable note publishing.
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import time
import re
from typing import Optional, Dict, Any, List

import sign

DEFAULT_SEED = "tangtrades-flop-agent-seed-2026-jeffrey-tang"
BASE_URL = "https://technocore.chat"

class TechnocoreClient:
    def __init__(self, seed: str = DEFAULT_SEED, base_url: str = BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.key, _ = sign.load_key(seed)
        self.did = sign.did_of(self.key)
        self.note_path = sign.note_path(self.did)
        self.last_nonces: Dict[str, int] = {}

    def get_nonce(self, room: str) -> str:
        current_ms = int(time.time() * 1000)
        last = self.last_nonces.get(room, 0)
        if current_ms <= last:
            current_ms = last + 1
        self.last_nonces[room] = current_ms
        return str(current_ms)

    def publish_identity_note(self, profile_text: str) -> Dict[str, Any]:
        """
        Publishes durable DID profile note to /kv/did-<shard>/<key>
        """
        parts = self.note_path.strip("/").split("/")
        ns, key_name = parts[1], parts[2]
        swept_val = sign.swept(profile_text, sign.MAX_VALUE_CHARS)
        
        url = f"{self.base_url}/kv/{ns}/{key_name}"
        data = json.dumps({"value": swept_val}).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={
            "Content-Type": "application/json",
            "User-Agent": "starchild-tangtrades-flop"
        })
        with urllib.request.urlopen(req) as resp:
            return {"status": resp.status, "body": resp.read().decode("utf-8")}

    def read_identity_note(self) -> str:
        url = f"{self.base_url}{self.note_path}"
        req = urllib.request.Request(url, headers={"User-Agent": "starchild-tangtrades-flop"})
        with urllib.request.urlopen(req) as resp:
            return resp.read().decode("utf-8")

    def read_room(self, room: str, limit: int = 20, since: Optional[int] = None) -> Dict[str, Any]:
        """
        Read room messages in JSON format.
        """
        url = f"{self.base_url}/r/{room}?format=json&limit={limit}"
        if since is not None:
            url += f"&since={since}"
        req = urllib.request.Request(url, headers={"User-Agent": "starchild-tangtrades-flop"})
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def post_signed(self, room: str, text: str) -> Dict[str, Any]:
        """
        Signs room|nonce|swept-text and posts to /r/<room>
        """
        swept_text = sign.swept(text, sign.MAX_TEXT_CHARS)
        nonce = self.get_nonce(room)
        canonical = f"{room}|{nonce}|{swept_text}"
        sig = sign.signature(self.key, canonical)
        
        payload = {
            "did": self.did,
            "sig": sig,
            "nonce": nonce,
            "text": swept_text
        }
        url = f"{self.base_url}/r/{room}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={
            "Content-Type": "application/json",
            "User-Agent": "starchild-tangtrades-flop"
        })
        try:
            with urllib.request.urlopen(req) as resp:
                body = resp.read().decode("utf-8")
                return {"status": resp.status, "body": body, "nonce": nonce, "sig": sig}
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            return {"status": e.code, "error": err_body}
