#!/usr/bin/env bash
# site_signals.sh — one-shot probe of a website's public signals before writing a research report.
# Usage: ./site_signals.sh <domain> [search_term]
#   domain      e.g. reelfork.com
#   search_term optional brand/app name for iTunes + YouTube lookups (defaults to domain)
# Output: WHOIS age, App Store listing, third-party traffic-DB presence (absence = below
# indexing threshold = tiny traffic), YouTube channel match.
set -u
D="${1:?usage: site_signals.sh <domain> [search_term]}"
T="${2:-$D}"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"

echo "===== WHOIS ($D) ====="
whois "$D" 2>/dev/null | grep -iE "creation date|updated date|registrar:|registry expiry" | head -6

echo
echo "===== iTunes App Store (term=$T) ====="
curl -s -m 20 "https://itunes.apple.com/search?term=${T// /+}&entity=software&limit=10" -A "$UA" | python3 -c "
import sys, json
try:
    rs = json.load(sys.stdin).get('results', [])
except Exception:
    rs = []
for r in rs:
    print(r.get('trackName'), '| rel:', r.get('releaseDate'), '| rating:', r.get('averageUserRating'),
          '/', r.get('userRatingCount'), '| seller:', r.get('sellerName'), '| bundle:', r.get('bundleId'))
"

echo
echo "===== Third-party traffic DBs (absence = below indexing threshold ≈ tiny traffic) ====="
for u in "https://hypestat.com/info/$D" "https://website.informer.com/$D" "https://www.siteprice.org/website-worth/$D"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -m 20 -A "$UA" "$u")
  echo "$u -> HTTP $code"
done
echo "(also try: curl 'https://data.similarweb.com/api/v1/data?domain=$D' — often 403 from datacenter IPs)"

echo
echo "===== YouTube channel search (term=$T) ====="
curl -sL -m 20 -A "$UA" "https://www.youtube.com/results?search_query=${T// /+}" | python3 -c "
import sys, re, json
t = sys.stdin.read()
m = re.search(r'var ytInitialData = (\{.*?\});</script>', t, re.S)
if not m:
    print('no ytInitialData found'); sys.exit()
d = json.loads(m.group(1))
def walk(o):
    if isinstance(o, dict):
        cr = o.get('channelRenderer')
        if cr:
            subs = cr.get('subscriberCountText', {}).get('simpleText', '?')
            print('CHANNEL:', cr.get('title', {}).get('simpleText'), '| subs:', subs)
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for i in o: walk(i)
walk(d)
print('(for full stats browse https://www.youtube.com/@<handle>/about — subs, joined date, total views)')
"
