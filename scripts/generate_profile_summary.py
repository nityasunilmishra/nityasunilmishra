#!/usr/bin/env python3
import json
import os
import urllib.request
from html import escape

USERNAME = os.environ.get("PROFILE_USERNAME", "nityasunilmishra")
TOKEN = os.environ.get("GITHUB_TOKEN")

headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "profile-summary-generator",
}
if TOKEN:
    headers["Authorization"] = f"Bearer {TOKEN}"

def fetch_json(url: str):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

profile = fetch_json(f"https://api.github.com/users/{USERNAME}")
repos = fetch_json(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated")

followers = int(profile.get("followers", 0))
public_repos = int(profile.get("public_repos", 0))
stars = sum(int(repo.get("stargazers_count", 0)) for repo in repos)
forks = sum(int(repo.get("forks_count", 0)) for repo in repos)

language_counts = {}
for repo in repos:
    lang = repo.get("language")
    if lang:
        language_counts[lang] = language_counts.get(lang, 0) + 1

top_languages = ", ".join(
    [f"{name} ({count})" for name, count in sorted(language_counts.items(), key=lambda item: item[1], reverse=True)[:3]]
) or "No public languages"

svg = f'''<svg width="760" height="220" viewBox="0 0 760 220" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="760" y2="220" gradientUnits="userSpaceOnUse">
      <stop stop-color="#0F172A"/>
      <stop offset="1" stop-color="#111827"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#38BDF8"/>
      <stop offset="1" stop-color="#14B8A6"/>
    </linearGradient>
  </defs>
  <rect width="760" height="220" rx="20" fill="url(#bg)"/>
  <rect x="20" y="20" width="720" height="180" rx="16" fill="#0B1220" stroke="#1E293B"/>
  <text x="40" y="58" fill="#E2E8F0" font-family="Segoe UI, Arial, sans-serif" font-size="22" font-weight="600">GitHub Profile Summary</text>
  <text x="40" y="88" fill="#94A3B8" font-family="Segoe UI, Arial, sans-serif" font-size="13">{escape(USERNAME)} • auto-generated from GitHub data</text>

  <g>
    <rect x="40" y="110" width="150" height="58" rx="12" fill="#0F172A" stroke="#1E293B"/>
    <text x="58" y="132" fill="#94A3B8" font-family="Segoe UI, Arial, sans-serif" font-size="12">Followers</text>
    <text x="58" y="154" fill="#F8FAFC" font-family="Segoe UI, Arial, sans-serif" font-size="24" font-weight="700">{followers}</text>
  </g>

  <g>
    <rect x="214" y="110" width="150" height="58" rx="12" fill="#0F172A" stroke="#1E293B"/>
    <text x="232" y="132" fill="#94A3B8" font-family="Segoe UI, Arial, sans-serif" font-size="12">Repos</text>
    <text x="232" y="154" fill="#F8FAFC" font-family="Segoe UI, Arial, sans-serif" font-size="24" font-weight="700">{public_repos}</text>
  </g>

  <g>
    <rect x="388" y="110" width="150" height="58" rx="12" fill="#0F172A" stroke="#1E293B"/>
    <text x="406" y="132" fill="#94A3B8" font-family="Segoe UI, Arial, sans-serif" font-size="12">Stars</text>
    <text x="406" y="154" fill="#F8FAFC" font-family="Segoe UI, Arial, sans-serif" font-size="24" font-weight="700">{stars}</text>
  </g>

  <g>
    <rect x="562" y="110" width="150" height="58" rx="12" fill="#0F172A" stroke="#1E293B"/>
    <text x="580" y="132" fill="#94A3B8" font-family="Segoe UI, Arial, sans-serif" font-size="12">Forks</text>
    <text x="580" y="154" fill="#F8FAFC" font-family="Segoe UI, Arial, sans-serif" font-size="24" font-weight="700">{forks}</text>
  </g>

  <text x="40" y="188" fill="#CBD5E1" font-family="Segoe UI, Arial, sans-serif" font-size="12">Top languages: {escape(top_languages)}</text>
  <rect x="40" y="176" width="420" height="7" rx="3.5" fill="#0F172A"/>
  <rect x="40" y="176" width="260" height="7" rx="3.5" fill="url(#accent)"/>
</svg>
'''

os.makedirs("assets", exist_ok=True)
with open("assets/profile-summary.svg", "w", encoding="utf-8") as f:
    f.write(svg)
