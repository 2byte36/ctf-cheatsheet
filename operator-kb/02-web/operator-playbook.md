# Web Operator Playbook

## Operational Playbook Router

| If you see | Open playbook | First action |
|---|---|---|
| URL/search/login parameter changes content | [SQLi](../../playbooks/web-sqli.md) | `curl -sk 'http://HOST/path?id=1%27'` |
| SQLi signal but no output | [Blind SQLi](../../playbooks/web-blind-sqli.md) | `python3 ../../scripts/web/blind_sqli_boolean.py --url 'http://HOST/?id=INJECT' --expr 'SELECT database()' --true MARKER` |
| ping/DNS/converter wraps a command | [Command Injection](../../playbooks/web-command-injection.md) | `python3 ../../scripts/web/command_injection_probe.py --url 'http://HOST/ping?host=INJECT'` |
| file/path/download parameter | [LFI / Traversal](../../playbooks/web-lfi-path-traversal.md) | `python3 ../../scripts/web/lfi_wordlist_probe.py --url 'http://HOST/view?file=INJECT'` |
| URL fetcher/webhook/PDF/link preview | [SSRF](../../playbooks/web-ssrf.md) | `python3 ../../scripts/web/ssrf_probe.py --url 'http://HOST/fetch?url=INJECT'` |
| `{{...}}`, template errors, rendered input | [SSTI](../../playbooks/web-ssti.md) | `curl -sk 'http://HOST/?name={{7*7}}'` |
| report/admin bot/moderation | [XSS Admin Bot](../../playbooks/web-xss-admin-bot.md) | Submit `<img src="https://webhook.site/ID?x=1">` |
| avatar/document/archive upload | [File Upload](../../playbooks/web-file-upload.md) | `curl -sk -F 'file=@test.png;type=image/png' http://HOST/upload` |
| JWT/cookie/session claims | [JWT Session](../../playbooks/web-jwt-session.md) | `python3 ../../scripts/web/jwt_decode.py TOKEN` |
| Node JSON merge endpoint | [Prototype Pollution](../../playbooks/web-prototype-pollution.md) | POST `{"__proto__":{"polluted":"yes"}}` |
| `/graphql` endpoint | [GraphQL](../../playbooks/web-graphql.md) | POST `{"query":"{__typename}"}` |

## Mindset

Web challenges are trust-boundary puzzles. Find where attacker-controlled data crosses into:

- Database/query language
- Template engine
- File path or archive parser
- URL fetcher/internal network
- XML/parser stack
- Browser/admin bot
- Auth/session/identity provider
- Background worker or CI/CD system
- Smart contract or blockchain RPC

The strongest workflow is normal-use capture before mutation. Do not fuzz blind until you know routes, auth state, content types, and expected response shapes.

## First-Pass Workflow

```bash
curl -sk -i "$URL" | sed -n '1,80p'
curl -sk "$URL" | tee work/index.html
curl -sk "$URL/robots.txt"
curl -sk "$URL/sitemap.xml"
```

Extract routes and JS clues:

```bash
rg -a -o 'src="[^"]+|href="[^"]+' work/index.html | sed 's/^[^"]*"//' | sort -u
rg -a -o '/[A-Za-z0-9_./{}:-]+' work/*.js 2>/dev/null | sort -u
rg -a -i 'api|admin|debug|flag|token|secret|graphql|upload|callback|webhook' work
```

Probe methods and content types:

```bash
for m in GET POST PUT PATCH DELETE OPTIONS TRACE; do
  curl -sk -X "$m" -i "$URL/api/thing" | sed -n '1,20p'
done

curl -sk -i "$URL/api/login" -H 'Content-Type: application/json' -d '{"user":"guest"}'
curl -sk -i "$URL/api/login" -H 'Content-Type: application/x-www-form-urlencoded' -d 'user=guest'
curl -sk -i "$URL/api/login" -H 'Content-Type: application/xml' -d '<user>guest</user>'
```

## Enumeration Checklist

- Headers, cookies, CSP, CORS, server versions.
- HTML comments, hidden inputs, localStorage/sessionStorage.
- JS bundles, source maps, route strings, hardcoded API paths.
- `robots.txt`, `sitemap.xml`, `.well-known/`, backup files, `.git/`, `.bzr/`.
- Alternate verbs and content types.
- Role and object ID changes.
- Upload file extension, magic bytes, MIME sniffing, parser-specific behavior.
- SSRF URL parser behavior, redirects, DNS, loopback variants.
- Admin bot/report flow and callback proof.
- Docker/source topology without using setup secrets as inputs.

## Attack Families

| Family | Fast Indicators | First Payloads |
|---|---|---|
| SQLi/NoSQLi | errors, boolean differences, search/filter/sort | `'`, `"`, `1 OR 1=1--`, `{"$ne":null}` |
| SSTI | reflected template syntax | `{{7*7}}`, `${7*7}`, `<%= 7*7 %>` |
| LFI/traversal | filename/path parameters | `../../../../etc/passwd`, `php://filter/convert.base64-encode/resource=index.php` |
| SSRF | URL fetchers, webhooks, PDF/export | `http://127.0.0.1/`, `http://[::1]/`, decimal/octal IPs |
| XXE/XML | XML, SVG, DOCX, SOAP | external entity file read or OOB DTD |
| Command/code injection | shell-looking wrappers, converters | `;id`, `|id`, newline, brace expansion |
| Deserialization | cookies/blobs/type metadata | PHP serialized, pickle, Java, .NET TypeNameHandling |
| Client-side/admin bot | report URL, CSP, DOM reflection | XSS beacon, CSRF, XS-Leak |
| Auth/session | JWT, cookies, roles, OAuth/SAML | alg none/confusion, weak secrets, IDOR, state/redirect bugs |
| Prototype pollution | Node, merge/deep object APIs | `__proto__`, `constructor.prototype` |
| Web3 | contracts/RPC/private testnet | proxy storage, delegatecall, ABI mismatch, reentrancy |

## Competition Tradecraft

### Bot Challenge Hosting Ladder

1. Use `webhook.site` for proof-of-visit and one-shot exfil.
2. Use static hosting when the bot must render attacker HTML/JS.
3. Use a dynamic server only for stateful callbacks, custom headers, or multi-step bot logic.

### Remote Parity

Source and Docker identify reachable bugs. They do not provide valid exploit inputs if the values come only from setup files. Do not solve by using seeded admin credentials, local `.env`, hardcoded flags, or container management commands.

### Chain Shapes

- JS/source route discovery -> hidden endpoint -> IDOR/auth bypass -> flag.
- XSS -> admin bot -> privileged fetch/action -> exfil.
- Upload/parser mismatch -> source/file read -> key/session forge.
- SSRF -> internal API/Docker/metadata -> file read/RCE.
- SQLi -> write primitive -> SSTI/upload/deserialization.

## Niche/Specialized Tactics To Preserve

- Unicode/case-folding URL and XSS bypasses.
- CSS font/container-query exfiltration.
- CSP nonce/base tag/link prefetch bypasses.
- HTTP request smuggling/cache poisoning.
- Gopher/wget/SoapClient CRLF protocol smuggling.
- URL parser disagreements: `parse_url`, curl, proxy, browser, framework.
- ExifTool, WeasyPrint, CairoSVG, React Server Components, Next.js middleware bypass.
- Bazaar/Git repo reconstruction and source-map recovery.
- Web3: EIP-1967 proxy storage, delegatecall storage context, transient storage collision, Groth16 verifier misuse.

## Rabbit Holes

- Running `sqlmap` before mapping auth and content type.
- Ignoring JS bundles and source maps.
- Treating local setup secrets as the solve.
- Testing only browser-visible fields, not optional JSON fields.
- Missing second-order rendering in admin/export/worker paths.
- Assuming localhost filters or URL validation are robust.
- Building full RCE before proving file read, SSRF, or template execution.

## Source Deep Dives

- Recon and chain discipline: [ctf-web/SKILL.md](../../ctf-web/SKILL.md)
- SQLi: [ctf-web/sql-injection.md](../../ctf-web/sql-injection.md)
- Server-side: [ctf-web/server-side.md](../../ctf-web/server-side.md)
- Advanced server-side: [ctf-web/server-side-advanced-4.md](../../ctf-web/server-side-advanced-4.md)
- Client-side: [ctf-web/client-side.md](../../ctf-web/client-side.md)
- Client-side advanced: [ctf-web/client-side-advanced.md](../../ctf-web/client-side-advanced.md)
- Auth/JWT/infra: [ctf-web/auth-and-access.md](../../ctf-web/auth-and-access.md), [ctf-web/auth-jwt.md](../../ctf-web/auth-jwt.md), [ctf-web/auth-infra.md](../../ctf-web/auth-infra.md)
- Node/prototype: [ctf-web/node-and-prototype.md](../../ctf-web/node-and-prototype.md)
- Web3: [ctf-web/web3.md](../../ctf-web/web3.md)
- CVE matching: [ctf-web/cves.md](../../ctf-web/cves.md)
