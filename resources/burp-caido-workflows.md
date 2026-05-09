# Burp And Caido Workflows

## Baseline A Feature

1. Use the app normally once.
2. Send the request to Repeater.
3. Change one parameter at a time.
4. Record status, length, redirect, body marker, timing.

## SQLi Boolean Diff

```text
Request A: id=1 AND 1=1-- -
Request B: id=1 AND 1=2-- -
```

Expected signal: stable length/body difference. If true, open [../playbooks/web-blind-sqli.md](../playbooks/web-blind-sqli.md).

## Authz/IDOR Diff

```text
GET /api/users/1
GET /api/users/2
GET /api/users/admin
```

Expected signal: object changes without authorization failure.

## Content-Type Confusion

Send same semantic data as:

```text
application/json
application/x-www-form-urlencoded
multipart/form-data
application/xml
```

Expected signal: parser-specific behavior or bypass.

## Upload Testing

In Repeater:

- Change filename extension.
- Change part `Content-Type`.
- Preserve magic bytes but append payload.
- Try duplicate filename fields.

Open [../playbooks/web-file-upload.md](../playbooks/web-file-upload.md).

## Admin Bot

1. Submit webhook image payload.
2. Confirm visit.
3. Submit JS beacon payload.
4. Inspect CSP errors using local reproduction.

Open [../playbooks/web-xss-admin-bot.md](../playbooks/web-xss-admin-bot.md).

