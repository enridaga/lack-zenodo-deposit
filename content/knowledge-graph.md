---
title: Knowledge Graph
---

# The LACK Knowledge Graph

The LACK knowledge graph (v1.0, released 9 April 2026) is constructed through a three-phase pipeline of ontology alignment, entity URI generation, and relation graph construction, applied to relation extraction datasets from two investigative journalism sources covering climate lobbying.

---

## KG at a Glance

### Entities

| | Count |
|---|---|
| **Total entities** | **38,584** |
| Persons (`lack:Person`) | 16,905 |
| Collectives (`lack:Collective`) | 21,679 |
| Wikidata links (`owl:sameAs`) | 13,133 |
| DBpedia links | 13,389 |

### Relations

| | Count |
|---|---|
| **Asserted (extracted)** | **65,992** |
| **Inferred (entailed)** | **174,354** |
| **Total after inferencing** | **264,516** |

{{ stats_dashboard }}

---

## Relation Extraction

Relationships between persons and organisations are extracted automatically from source text using a large language model pipeline guided by the [LACK ontology](ontology.html).

### Relation types extracted

| Relation | Count |
|---|---|
| `lack:memberOf` | 15,939 |
| `lack:employedBy` | 9,507 |
| `lack:leadsAt` | 8,755 |
| `lack:contributedTo` | 8,403 |
| `lack:fundedBy` | 6,495 |
| `lack:hasPartner` | 4,582 |
| `lack:associatedWith` | 4,315 |
| `lack:sponsored` | 4,047 |
| `lack:derivedFrom` | 3,654 |
| `lack:activeSince` | 133 |
| `lack:founded` | 74 |
| `lack:hasMember` | 39 |
| `lack:acquired` | 37 |
| `lack:organised` | 12 |
| **Total** | **65,992** |

All relations can optionally carry **temporal annotations** (`since`, `until`), represented via RDF reification on the `rdf:Statement` node. The `activeSince` property attaches a temporal bound directly to an entity rather than a relation.

### Evaluation

Evaluated on 300 relations extracted from 8 Desmog profile pages:

| Criterion | Yes | Partly | No | Accuracy | Accuracy (with partial) |
|---|---|---|---|---|---|
| True | 279 | 18 | 3 | 0.93 | 0.99 |
| Valid | 272 | 12 | 16 | 0.907 | 0.95 |
| Time info true | 239 | 34 | 27 | 0.797 | 0.91 |

Ongoing work includes error analysis, ontology refinement, and evaluation on LobbyMap sources.

---

## Entity Linking

Entities extracted from text are linked to canonical identifiers in Wikidata and DBpedia, enabling cross-source deduplication and enrichment. Entity linking is complete for v1.0.

Two methods were implemented and compared:

- **Gemini in-context** — direct linking using a large language model
- **Multi-step workflow** — Wikidata search followed by LLM verification (Groq + Llama 3.3 70B), including web search for disambiguation

The multi-step workflow was selected for production. Coverage in the current release:

| | Count | % of entities |
|---|---|---|
| Wikidata links | 13,133 | 34% |
| DBpedia links | 13,389 | 35% |
| Unlinked entities | ~12,062 | 31% |

---

## Inferencing

After the asserted graph is constructed, OWL inferencing is applied using the LACK ontology to materialise:

- **Inverse properties** — e.g. every `lack:employedBy` triple generates a `lack:hasEmployee` triple; every `lack:memberOf` generates `lack:hasMember`
- **`lack:associatedWith` entailments** — as the top-level superproperty, it is entailed by all other relation types

This adds 174,354 triples, bringing the total graph to **264,516 triples**.

| | Count |
|---|---|
| Asserted triples | 65,992 |
| Inferred triples | 174,354 |
| **Total** | **264,516** |

---

## Wikidata Enrichment

Linked entities can be enriched with information from Wikidata, including additional organisational roles, geographical context, and links to related claims and topics — supporting the research questions around alignment with climate science and policy goals.

---

## Roadmap

- [x] Relation extraction (Desmog + LobbyMap/InfluenceMap)
- [x] Ontology alignment and relation mapping
- [x] Entity URI generation (SHA1-based, stable IRIs)
- [x] Entity linking (Wikidata + DBpedia, Groq Llama 3.3 70B)
- [x] Knowledge graph construction (v1.0, 9 April 2026)
- [x] OWL inferencing
- [x] KG.ttl published for download
- [ ] Formal entity linking evaluation (gold standard)
- [ ] Relation extraction error analysis
- [ ] Desmog claim clustering (pairwise similarity)
- [ ] SPARQL endpoint (public)
- [ ] KG v2.0 with additional sources
