# RFC 0001 — IPLD DAG-CBOR Enumeration of the `meme:` URL
- **Status:** Draft
- **Category:** Standards Track (project-local)
- **Supersedes:** none
- **Depends on:** `RequestProject.MemeUrl` (the compact `meme:` codec), `RequestProject.Biome` (the A001379 biome table)
- **Codec:** IPLD DAG-CBOR (multicodec `dag-cbor`, code `0x71`)
- **Date:** 2026-07-10
## Abstract
This document specifies a canonical, content-addressed representation of the
project's "memes" — the FRACTRAN Hilbert-life biomes of `RequestProject.Biome`,
each already namable by a compact `meme:` URL (`RequestProject.MemeUrl`) — as
[IPLD](https://ipld.io/) [DAG-CBOR](https://ipld.io/specs/codecs/dag-cbor/)
blocks. It defines (1) the DAG-CBOR shape of a single meme, (2) the
deterministic encoding rules that make the block content-addressable, (3) the
[CID](https://github.com/multiformats/cid) derived from it, (4) an *enumeration*
structure — a canonical catalog block that links every biome in the table — and
(5) the bijection between a meme block and its `meme:` URL. The goal is that any
party can independently enumerate the same set of biomes, obtain byte-identical
blocks, and therefore the same CIDs, without coordination.
## 1. Terminology
The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this
document are to be interpreted as described in RFC 2119.
- **Meme.** The minimal data that names one biome animation: the render `order`
  and `frameMs`, the A001379 `index`, and the fifteen p-adic `exps`. See
  `RequestProject.MemeUrl.Meme`.
- **Biome table.** The ordered array `RequestProject.Biome.table` of 194 rows,
  indexed `0 … 193`, with `table[i].index = i`.
- **Tracked primes.** The fifteen primes
  `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71]`
  (`RequestProject.Biome.primes`), against which `exps` is aligned position by
  position.
- **DAG-CBOR.** The IPLD codec that restricts CBOR (RFC 8949) to a
  deterministic subset and adds the CID link type (tag 42). Multicodec name
  `dag-cbor`, code `0x71`.
- **CID.** A self-describing content identifier (multiformats CIDv1):
  `<multibase>(<version=0x01><multicodec><multihash>)`.
## 2. Rationale
A `meme:` URL is already a total, round-tripping serialization of a meme
(`RequestProject.MemeUrl.ofUrl_toUrl` proves `ofUrl (toUrl m) = some m` for every
well-formed meme). It is, however, a *string*: it is not content-addressed, it
does not carry its own type, and there is no canonical way to name the *whole
set* of memes as one object.
DAG-CBOR supplies exactly the missing pieces:
1. a **deterministic** byte encoding, so that the same meme always hashes to the
   same CID regardless of who encodes it;
2. **links** (CIDs), so a single small "catalog" block can enumerate all 194
   biomes by reference; and
3. **self-description**, so a block announces that it is DAG-CBOR.
This RFC pins those pieces down precisely enough that two independent
implementations produce byte-identical blocks and therefore identical CIDs.
## 3. The meme block
### 3.1 Logical shape
A single meme is encoded as a DAG-CBOR **map** with these keys (all lower-case
ASCII):
| key       | type                     | source field          | constraint (`Meme.Valid`)        |
|-----------|--------------------------|-----------------------|----------------------------------|
| `"v"`     | unsigned integer         | schema version, `= 1` | `= 1` for this RFC               |
| `"order"` | unsigned integer         | `Meme.order`          | `< 62`                           |
| `"frame"` | unsigned integer         | `Meme.frameMs`        | `< 62³ = 238328`                 |
| `"index"` | unsigned integer         | `Meme.index`          | `< 62² = 3844`                   |
| `"exps"`  | array of unsigned int    | `Meme.exps`           | `length < 62`, each entry `< 62` |
The `"exps"` array is positional: entry `j` is the exponent of
`RequestProject.Biome.primes[j]`. For a full biome the array has length 15.
Derived quantities — the exponent sum `Σe`, the prime support, the
characteristic number `N = ∏ pᵉ`, the FRACTRAN program, the palette, the rule
set, and the seed board — **MUST NOT** be stored. They are pure functions of the
five fields above (`RequestProject.Biome` API) and storing them would create a
second source of truth and break determinism.
> **Note.** The `"v"` field is added by this RFC and has no counterpart in the
> `meme:` URL, whose version is implied by the codec module. Version `1` denotes
> the schema of this document.
### 3.2 Deterministic encoding (normative)
An encoder **MUST** follow the DAG-CBOR determinism rules:
1. **Integers** are encoded in their shortest form (major types 0/1); no leading
   zero bytes, no oversized width. Every integer here is a small non-negative
   value, so all fit the direct or 1-byte-argument encodings.
2. **Map keys** are sorted by the *bytewise lexicographic order of their encoded
   CBOR bytes*. For the ASCII string keys used here (all distinct short text
   strings) this is equivalent to sorting first by key length, then bytewise.
   The resulting canonical key order for the meme map is:
   ```
   "v"  <  "exps"  <  "frame"  <  "index"  <  "order"
   ```
   (length 1 before length 5; then "exps" < "frame" < "index" < "order"
   bytewise among the length-5 keys). Encoders **MUST** emit keys in this order;
   decoders **SHOULD** reject maps whose keys are out of order (strict mode) or
   **MAY** accept and re-canonicalize (lenient mode).
3. **Definite lengths only.** Maps and arrays **MUST** use definite-length
   headers. Indefinite-length items are forbidden.
4. **No floats, no tags** (other than CID tag 42, which does not occur inside a
   meme block), **no duplicate keys**, and no `undefined`/`simple` values.
An encoder **MUST** reject a meme that is not `Meme.Valid`; the field
constraints in §3.1 mirror that predicate.
### 3.3 Worked example — biome #14
Biome #14 has `meme:4G20E0FC00412000010011` and, with the gallery render
defaults `order = 4`, `frameMs = 140`:
- `order = 4`, `frame = 140`, `index = 14`,
- `exps = [12, 0, 0, 4, 1, 2, 0, 0, 0, 0, 1, 0, 0, 1, 1]`
  (i.e. `2¹²·7⁴·11·13²·31·59·71`, `N = 2374124840062976`).
The canonical DAG-CBOR (shown as a CBOR diagnostic map with keys in canonical
order) is:
```
{
  "v":     1,
  "exps":  [12, 0, 0, 4, 1, 2, 0, 0, 0, 0, 1, 0, 0, 1, 1],
  "frame": 140,
  "index": 14,
  "order": 4
}
```
Implementations **SHOULD** include this vector in their conformance test suite
and check that re-encoding reproduces the same bytes (and hence the same CID).
## 4. Content addressing
### 4.1 CID of a meme block
The CID of a meme block is the CIDv1
```
CIDv1 = multibase( 0x01 || 0x71 || multihash )
```
where
- version byte `0x01` (CIDv1),
- multicodec `0x71` (`dag-cbor`),
- `multihash` is the **REQUIRED** default `sha2-256` (code `0x12`, length `0x20`)
  digest of the canonical block bytes of §3, and
- the human-facing multibase is `base32` (prefix `b`), which is the CIDv1
  default; other multibases **MAY** be used for display but the binary CID is
  authoritative.
Because the block bytes are deterministic (§3.2), the CID is a pure function of
the meme's five fields. Two encoders **MUST** agree on it.
### 4.2 Alternate hashes
An implementation **MAY** additionally publish blocks under other multihash
functions (e.g. `blake3`). Such CIDs are distinct addresses for the *same*
logical meme; the `sha2-256` CID of §4.1 is the canonical one for enumeration
(§5) and cross-references.
## 5. Enumeration
### 5.1 The catalog block
The set of all memes is named by a single **catalog** block, itself a DAG-CBOR
map:
| key         | type                      | meaning                                             |
|-------------|---------------------------|-----------------------------------------------------|
| `"v"`       | unsigned integer `= 1`    | catalog schema version                              |
| `"kind"`    | text string `"a001379"`   | which enumeration this catalogs                     |
| `"order"`   | unsigned integer          | render `order` shared by all listed memes           |
| `"frame"`   | unsigned integer          | render `frameMs` shared by all listed memes         |
| `"count"`   | unsigned integer          | number of entries (`= 194` for the full table)      |
| `"primes"`  | array of unsigned int     | the fifteen tracked primes, defining `exps` order   |
| `"memes"`   | array of CID links        | one CID (tag 42) per biome, **in table index order**|
Canonical key order (by the rule of §3.2) is:
```
"v" < "kind" < "count" < "frame" < "memes" < "order" < "primes"
```
Normative requirements:
1. `"memes"` **MUST** be ordered by biome `index`, ascending, with no gaps and
   no duplicates: `memes[i]` **MUST** be the §4.1 CID of the meme for
   `Biome.table[i]`, encoded with the catalog's shared `order` and `frame`.
2. `"count"` **MUST** equal the length of `"memes"`.
3. `"primes"` **MUST** equal `RequestProject.Biome.primes`; it fixes the meaning
   of every meme's positional `"exps"` array and lets a consumer validate blocks
   without out-of-band knowledge.
4. Each element of `"memes"` **MUST** be a CID link (DAG-CBOR tag 42), not an
   inlined map. The memes are enumerated *by reference* so the catalog stays
   small and each meme remains an independently retrievable, independently
   verifiable block.
The catalog's own CID (computed as in §4.1 over the catalog bytes) is the single
name for "the whole enumeration at this `order`/`frame`". Changing `order` or
`frame` yields a different catalog CID but the *same* underlying biomes; the
biome identity that is invariant across render settings is the `index` together
with `exps`.
### 5.2 Determinism of the enumeration
Given a fixed `order` and `frame`, the catalog block is a pure function of
`RequestProject.Biome.table`. Since the table is fixed and the per-meme encoding
is deterministic (§3.2, §4.1), the catalog bytes — and thus the catalog CID —
are reproducible by any implementation. This is the sense in which the memes are
*enumerated*: the catalog CID is a checkable fingerprint of the entire set.
### 5.3 Optional CAR packaging
For transport, an implementation **MAY** bundle the catalog block and all 194
meme blocks into a single [CAR](https://ipld.io/specs/transport/car/) (Content
Addressable aRchive) file whose sole root is the catalog CID. Consumers can then
verify the whole enumeration offline: check each block's CID, then check that
`"memes"[i]` resolves to the block for `Biome.table[i]`.
## 6. Relationship to the `meme:` URL
The DAG-CBOR meme block and the `meme:` URL of `RequestProject.MemeUrl` carry
the **same information** for schema version 1 (the URL simply omits the explicit
`"v"`, which is fixed at 1). The mappings are:
- **URL → block.** Parse with `RequestProject.MemeUrl.ofUrl` to obtain a
  `Meme`; emit the §3 map with `"v" = 1`.
- **block → URL.** Read the five fields from the map; build the corresponding
  `Meme`; serialize with `RequestProject.MemeUrl.toUrl`.
Because `ofUrl (toUrl m) = some m` (`RequestProject.MemeUrl.ofUrl_toUrl`) and the
DAG-CBOR encoding is an injective, total function of the same fields, the round
trip **URL → Meme → block → Meme → URL** is the identity on well-formed memes.
Implementations **SHOULD** expose both directions and test the round trip on the
whole table (as `RequestProject.MemeUrlMain` already does for the URL codec).
An implementation **MAY** additionally record, alongside each catalog entry or
in a companion index, the human-readable `meme:` URL of each biome (as already
emitted to `out/memes/urls.tsv`), purely as a convenience; the CID list in
`"memes"` remains authoritative.
## 7. Conformance
An implementation is **conformant** if:
1. it encodes a meme exactly as in §3, rejecting non-`Valid` memes;
2. it computes CIDs as in §4.1;
3. it produces the catalog of §5.1 with the ordering and derivation
   requirements of §5.1–§5.2;
4. its biome #14 block matches the diagnostic value of §3.3 byte-for-byte; and
5. round-tripping any `meme:` URL through §6 is the identity.
## 8. Security considerations
- **Integrity.** CIDs are cryptographic hashes; a retrieved block that does not
  hash to its CID **MUST** be rejected. This protects both individual memes and
  the enumeration (via the catalog's `"memes"` links).
- **Determinism as an attack surface.** Non-canonical DAG-CBOR (unsorted keys,
  indefinite lengths, non-minimal integers) can encode the same logical meme
  under a *different* byte string and hence a different CID. Strict decoders
  **SHOULD** reject non-canonical input to prevent CID ambiguity.
- **Denial of service.** The field bounds of §3.1 cap every value; decoders
  **SHOULD** enforce them before allocating (e.g. reject an `"exps"` length
  claim `≥ 62`).
- **No code, no external references.** A meme block contains only small
  integers and (in the catalog) CID links to other meme blocks. It carries no
  executable content and no off-DAG URLs, so resolving one cannot fetch
  arbitrary network resources.
## 9. IANA / multiformats considerations
This RFC introduces no new multicodec, multihash, or multibase. It reuses:
- multicodec `dag-cbor` (`0x71`) for both meme and catalog blocks,
- multihash `sha2-256` (`0x12`) as the required digest,
- multibase `base32` (`b`) as the default textual CID form, and
- CBOR tag `42` for CID links (per the DAG-CBOR spec).
The `meme:` URI scheme is defined by `RequestProject.MemeUrl` and is unchanged
by this document.
## 10. References
- RFC 2119 — Key words for use in RFCs.
- RFC 8949 — Concise Binary Object Representation (CBOR).
- IPLD DAG-CBOR specification — https://ipld.io/specs/codecs/dag-cbor/
- Multiformats: CID, multicodec, multihash, multibase — https://multiformats.io/
- IPLD CAR (Content Addressable aRchives) — https://ipld.io/specs/transport/car/
- OEIS A001379 — the p-adic biome table underlying `RequestProject.Biome`.
- Project modules: `RequestProject.MemeUrl`, `RequestProject.MemeUrlProofs`,
  `RequestProject.Biome`.
## Appendix A — Canonical key orderings (quick reference)
Meme map (§3.1):
```
"v" (1) < "exps" (5) < "frame" (5) < "index" (5) < "order" (5)
```
Catalog map (§5.1):
```
"v" (1) < "kind" (4) < "count" (5) < "frame" (5) < "memes" (5) < "order" (5) < "primes" (6)
```
(Shorter encoded keys sort first; ties broken bytewise. Lengths in parentheses.)
## Appendix B — Tracked primes and `exps` alignment
`"exps"[j]` is the exponent of `primes[j]`:
| j    | 0 | 1 | 2 | 3 | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 | 14 |
|------|---|---|---|---|----|----|----|----|----|----|----|----|----|----|----|
| prime| 2 | 3 | 5 | 7 | 11 | 13 | 17 | 19 | 23 | 29 | 31 | 41 | 47 | 59 | 71 |
The characteristic number is `N = ∏_j primes[j] ^ exps[j]` and is *derived*, not
stored.
