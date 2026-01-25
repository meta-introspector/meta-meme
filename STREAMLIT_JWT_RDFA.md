# Streamlit + JWT + RDFa Composition

## Architecture

Each Streamlit app self-composes with JWT tokens containing RDFa-encoded task data:

```lean
structure JWTPayload where
  sub : String      -- muse:Calliope
  iat : Nat         -- issued timestamp
  exp : Nat         -- expiration (iat + 4 hours)
  data : String     -- RDFa-encoded task
```

## RDFa Embedding

Tasks are embedded using Schema.org vocabulary:

```html
<div vocab='http://schema.org/' typeof='SoftwareApplication'>
  <span property='name'>TASK1</span>
  <span property='description'>Summarize Text</span>
  <meta property='complexity' content='1'/>
</div>
```

## Composition Flow

1. **Task Definition** → HackathonTask structure
2. **RDFa Encoding** → taskToRDFa converts to semantic HTML
3. **JWT Wrapping** → composeJWT embeds RDFa in token payload
4. **Streamlit Auth** → App validates JWT and extracts RDFa
5. **Protobuf API** → Clarifai calls use decoded task data

## Verified Properties

- `hackathon_tasks_count`: Proves 6 tasks exist
- `jwt_embeds_rdfa`: Axiom ensuring RDFa embedding in JWT payload

## Example

```lean
-- Calliope gets TASK1 at timestamp 1000
composeJWT "Calliope" ⟨"TASK1", "Summarize Text", 1⟩ 1000

-- Produces JWT with:
-- sub: "muse:Calliope"
-- iat: 1000
-- exp: 15400 (1000 + 14400 seconds = 4 hours)
-- data: "<div vocab='http://schema.org/'...>...</div>"
```

## Integration Points

- **ZK Witness**: JWT signatures prove task assignment without revealing content
- **HME**: Encrypted task complexity aggregated across muses
- **RDFa URL**: Complete system state shareable as single URL
- **Eigenvector**: Task distribution converges via 8! reflections
