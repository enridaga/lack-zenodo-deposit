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
| **Total entities** | **{{ kg_total_entities }}** |
| Persons (`lack:Person`) | {{ kg_total_persons }} |
| Collectives (`lack:Collective`) | {{ kg_total_collectives }} |
| Wikidata links (`owl:sameAs`) | {{ kg_wikidata_links }} |
| DBpedia links | {{ kg_dbpedia_links }} |

### Relations

| | Count |
|---|---|
| **Asserted (extracted)** | **{{ kg_asserted }}** |
| **Inferred (entailed)** | **{{ kg_inferred }}** |
| **Total after inferencing** | **{{ kg_total }}** |

{{ stats_dashboard }}

---

## Relation Extraction

Relationships between persons and organisations are extracted automatically from source text using a large language model pipeline guided by the [LACK ontology](ontology.html).

### Relation types extracted

| Relation | Count |
|---|---|
| `lack:memberOf` | {{ kg_rel_memberOf }} |
| `lack:employedBy` | {{ kg_rel_employedBy }} |
| `lack:leadsAt` | {{ kg_rel_leadsAt }} |
| `lack:contributedTo` | {{ kg_rel_contributedTo }} |
| `lack:fundedBy` | {{ kg_rel_fundedBy }} |
| `lack:hasPartner` | {{ kg_rel_hasPartner }} |
| `lack:associatedWith` | {{ kg_rel_associatedWith }} |
| `lack:sponsored` | {{ kg_rel_sponsored }} |
| `lack:derivedFrom` | {{ kg_rel_derivedFrom }} |
| `lack:activeSince` | {{ kg_rel_activeSince }} |
| `lack:founded` | {{ kg_rel_founded }} |
| `lack:hasMember` | {{ kg_rel_hasMember }} |
| `lack:acquired` | {{ kg_rel_acquired }} |
| `lack:organised` | {{ kg_rel_organised }} |
| **Total** | **{{ kg_asserted }}** |

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
| Wikidata links | {{ kg_wikidata_links }} | {{ kg_wikidata_pct }} |
| DBpedia links | {{ kg_dbpedia_links }} | {{ kg_dbpedia_pct }} |
| Unlinked entities | {{ kg_unlinked }} | {{ kg_unlinked_pct }} |

---

## Inferencing

After the asserted graph is constructed, OWL inferencing is applied using the LACK ontology to materialise:

- **Inverse properties** — e.g. every `lack:employedBy` triple generates a `lack:hasEmployee` triple; every `lack:memberOf` generates `lack:hasMember`
- **`lack:associatedWith` entailments** — as the top-level superproperty, it is entailed by all other relation types

This adds {{ kg_inferred }} triples, bringing the total graph to **{{ kg_total }} triples**.

| | Count |
|---|---|
| Asserted triples | {{ kg_asserted_inf }} |
| Inferred triples | {{ kg_inferred_inf }} |
| **Total** | **{{ kg_total_inf }}** |

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
- [x] SPARQL endpoint live (`sparql.climatesense.kmi.tools`, powered by QLever)
<!-- - [ ] Formal entity linking evaluation (gold standard)
- [ ] Relation extraction error analysis
- [ ] Desmog claim clustering (pairwise similarity)
- [ ] KG v2.0 with additional sources -->