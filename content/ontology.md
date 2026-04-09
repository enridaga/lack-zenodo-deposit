---
title: Ontology
---

# LACK Ontology

**Prefix:** `lack:`  
**Namespace:** `https://purl.net/climatesense/lack/ns#`  
**Status:** Draft

```turtle
@prefix lack: <https://purl.net/climatesense/lack/ns#> .
```

Download the formal files: [Turtle (.ttl)]({{ base_url }}/lack-ontology.ttl) · [Manchester Syntax (.omn)]({{ base_url }}/lack-ontology.omn)

---

## Overview

LACK is a lightweight ontology for describing relationships between people and organisations, derived from a large corpus of real-world relation expressions relevant to lobbying against climate change awareness and policies. It provides a minimal, reusable vocabulary covering membership, employment, leadership, funding, founding, and association.

The ontology is built around two top-level types and a set of object properties connecting them.

<div class="schema-diagram">
<svg viewBox="0 0 780 500" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="LACK ontology schema diagram">
  <defs>
    <!-- Arrowhead for directed edges -->
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#5a7fa3"/>
    </marker>
    <marker id="arrow-sym" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#d4b84a"/>
    </marker>
    <marker id="arrow-self" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#5a7fa3"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="780" height="500" fill="#f8f6f1" rx="8"/>

  <!-- ── Person node ── -->
  <rect x="60" y="190" width="140" height="60" rx="8" fill="#2b2b2b" stroke="#d4b84a" stroke-width="2"/>
  <text x="130" y="216" text-anchor="middle" font-family="monospace" font-size="13" fill="#d4b84a" font-weight="bold">lack:Person</text>
  <text x="130" y="234" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#c8c3b5">individual human</text>

  <!-- ── Collective node ── -->
  <rect x="580" y="190" width="160" height="60" rx="8" fill="#2b2b2b" stroke="#d4b84a" stroke-width="2"/>
  <text x="660" y="216" text-anchor="middle" font-family="monospace" font-size="13" fill="#d4b84a" font-weight="bold">lack:Collective</text>
  <text x="660" y="234" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#c8c3b5">group / organisation</text>

  <!-- ── rdf:Statement node (reification) ── -->
  <rect x="285" y="420" width="210" height="50" rx="6" fill="#1e1e1e" stroke="#888" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="390" y="441" text-anchor="middle" font-family="monospace" font-size="11" fill="#aaa">rdf:Statement</text>
  <text x="390" y="458" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#777">(temporal reification)</text>

  <!-- ── xsd:gYear node ── -->
  <rect x="285" y="32" width="210" height="44" rx="6" fill="#1e1e1e" stroke="#888" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="390" y="51" text-anchor="middle" font-family="monospace" font-size="11" fill="#aaa">xsd:gYear</text>
  <text x="390" y="67" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#777">(datatype — years)</text>

  <!-- ════════════════════════════════════
       EDGES: Person → Collective
  ════════════════════════════════════ -->

  <!-- memberOf / hasMember  (top arc, above nodes) -->
  <path d="M 200,205 C 310,130 450,130 580,205" fill="none" stroke="#5a7fa3" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="390" y="148" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#5a7fa3">memberOf</text>

  <!-- hasMember (return arc) -->
  <path d="M 580,215 C 450,155 310,155 200,215" fill="none" stroke="#5a7fa3" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="390" y="174" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#5a7fa3">hasMember</text>

  <!-- employedBy -->
  <path d="M 200,222 L 580,222" fill="none" stroke="#5a7fa3" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="390" y="215" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#5a7fa3">employedBy</text>

  <!-- leadsAt -->
  <path d="M 200,232 L 580,232" fill="none" stroke="#5a7fa3" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="390" y="247" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#5a7fa3">leadsAt</text>

  <!-- contributedTo -->
  <path d="M 200,245 C 310,290 450,290 580,245" fill="none" stroke="#5a7fa3" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="390" y="300" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#5a7fa3">contributedTo</text>

  <!-- fundedBy / founded (lower arc) -->
  <path d="M 200,258 C 310,340 450,340 580,258" fill="none" stroke="#5a7fa3" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="390" y="358" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#5a7fa3">fundedBy / founded / sponsored</text>

  <!-- ════════════════════════════════════
       EDGES: Collective → Collective  (self-loop style, drawn as arc at bottom)
  ════════════════════════════════════ -->

  <!-- hasPartner (symmetric, bottom of Collective node) -->
  <path d="M 650,250 C 700,310 720,340 660,370 C 600,340 620,310 650,250" fill="none" stroke="#d4b84a" stroke-width="1.5" marker-end="url(#arrow-sym)"/>
  <text x="730" y="320" text-anchor="start" font-family="sans-serif" font-size="11" fill="#d4b84a">hasPartner</text>
  <text x="730" y="334" text-anchor="start" font-family="sans-serif" font-size="10" fill="#b09030">(symmetric)</text>

  <!-- associatedWith (symmetric) -->
  <path d="M 640,250 C 580,320 540,360 580,390 C 640,370 660,320 640,250" fill="none" stroke="#d4b84a" stroke-width="1.5" marker-end="url(#arrow-sym)"/>
  <text x="480" y="385" text-anchor="end" font-family="sans-serif" font-size="11" fill="#d4b84a">associatedWith</text>
  <text x="480" y="399" text-anchor="end" font-family="sans-serif" font-size="10" fill="#b09030">(symmetric, top-level)</text>

  <!-- acquired / derivedFrom (Collective → Collective, left arc) -->
  <path d="M 580,200 C 530,160 480,160 430,185" fill="none" stroke="#5a7fa3" stroke-width="1.2" marker-end="url(#arrow)" stroke-dasharray="4,2"/>
  <text x="508" y="158" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#5a7fa3">acquired / derivedFrom</text>

  <!-- organised (Collective → Collective) -->
  <path d="M 580,245 C 530,270 500,270 470,255" fill="none" stroke="#5a7fa3" stroke-width="1.2" marker-end="url(#arrow)" stroke-dasharray="4,2"/>
  <text x="522" y="274" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#5a7fa3">organised</text>

  <!-- sameAs (Collective → Collective) -->
  <path d="M 580,210 C 545,185 510,182 480,200" fill="none" stroke="#888" stroke-width="1.2" marker-end="url(#arrow)" stroke-dasharray="3,3"/>
  <text x="530" y="184" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#888">owl:sameAs</text>

  <!-- ════════════════════════════════════
       EDGES to xsd:gYear (top)
  ════════════════════════════════════ -->

  <!-- activeSince / activeUntil from Person -->
  <path d="M 130,190 L 290,76" fill="none" stroke="#888" stroke-width="1.2" marker-end="url(#arrow)" stroke-dasharray="4,2"/>
  <text x="188" y="118" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#888" transform="rotate(-28,188,118)">activeSince / activeUntil</text>

  <!-- activeSince / activeUntil from Collective -->
  <path d="M 660,190 L 492,76" fill="none" stroke="#888" stroke-width="1.2" marker-end="url(#arrow)" stroke-dasharray="4,2"/>
  <text x="598" y="118" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#888" transform="rotate(28,598,118)">activeSince / activeUntil</text>

  <!-- ════════════════════════════════════
       EDGES to rdf:Statement (reification)
  ════════════════════════════════════ -->

  <!-- since / until from rdf:Statement to xsd:gYear -->
  <path d="M 390,420 L 390,76" fill="none" stroke="#888" stroke-width="1" marker-end="url(#arrow)" stroke-dasharray="3,3"/>
  <text x="406" y="270" font-family="sans-serif" font-size="10" fill="#888">since / until</text>

  <!-- rdf:Statement annotates a triple (indicated with dashed lines to both nodes) -->
  <path d="M 340,420 L 200,250" fill="none" stroke="#888" stroke-width="1" stroke-dasharray="3,3"/>
  <path d="M 440,420 L 580,250" fill="none" stroke="#888" stroke-width="1" stroke-dasharray="3,3"/>

  <!-- ── Legend ── -->
  <rect x="20" y="430" width="230" height="58" rx="5" fill="#ffffff" stroke="#e0ddd5" stroke-width="1"/>
  <text x="30" y="448" font-family="sans-serif" font-size="11" fill="#2b2b2b" font-weight="bold">Legend</text>
  <line x1="30" y1="458" x2="70" y2="458" stroke="#5a7fa3" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="76" y="462" font-family="sans-serif" font-size="10" fill="#555">object property</text>
  <line x1="30" y1="474" x2="70" y2="474" stroke="#d4b84a" stroke-width="1.5" marker-end="url(#arrow-sym)"/>
  <text x="76" y="478" font-family="sans-serif" font-size="10" fill="#555">symmetric property</text>
  <line x1="30" y1="482" x2="70" y2="482" stroke="#888" stroke-width="1" stroke-dasharray="4,2" marker-end="url(#arrow)"/>
  <text x="76" y="486" font-family="sans-serif" font-size="10" fill="#555">datatype / reification</text>
</svg>
</div>

---

## Types

### `lack:Person`
An individual human being.

### `lack:Collective`
Any group of people organised around a shared purpose. This includes but is not limited to: companies, NGOs, think tanks, news agencies, political assemblies, events, committees, and networks.

---

## Relations

### Membership

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:memberOf` | member of | `lack:Person` | `lack:Collective` | `lack:hasMember` | `lack:associatedWith` |
| `lack:hasMember` | has member | `lack:Collective` | `lack:Person` | `lack:memberOf` | `lack:associatedWith` |

### Employment

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:employedBy` | employed by | `lack:Person` | `lack:Collective` | `lack:hasEmployee` | `lack:associatedWith` |
| `lack:hasEmployee` | has employee | `lack:Collective` | `lack:Person` | `lack:employedBy` | `lack:associatedWith` |

### Leadership

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:leadsAt` | leads at | `lack:Person` | `lack:Collective` | `lack:hasLeader` | `lack:employedBy` |
| `lack:hasLeader` | has leader | `lack:Collective` | `lack:Person` | `lack:leadsAt` | `lack:associatedWith` |

`lack:leadsAt` covers any named leadership or responsibility role within an organisation or department, including but not limited to: CEO, president, chair, director, VP, treasurer, secretary, COO, and department-level director roles. It is a sub-property of `lack:employedBy`, which is itself a sub-property of `lack:associatedWith`.

### Funding

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:fundedBy` | funded by | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:hasFunder` | `lack:associatedWith` |
| `lack:hasFunder` | has funder | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:fundedBy` | `lack:associatedWith` |

Covers funding, donation, commissioning, and award receipt.

### Founding & Creation

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:founded` | founded | `lack:Person` \| `lack:Collective` | `lack:Collective` | `lack:wasFoundedBy` | `lack:associatedWith` |
| `lack:wasFoundedBy` | was founded by | `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:founded` | `lack:associatedWith` |

Covers founding, co-founding, creation, incorporation, and launch.

### Contribution

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:contributedTo` | contributed to | `lack:Person` \| `lack:Collective` | `lack:Collective` | `lack:hasContributor` | |
| `lack:hasContributor` | has contributor | `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:contributedTo` | |

Covers contribution, authorship, distribution, presentation, and reposting.

### Partnership

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:hasPartner` | has partner | `lack:Collective` | `lack:Collective` | `lack:hasPartner` *(symmetric)* | `lack:associatedWith` |

### Sponsorship

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:sponsored` | sponsored | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:wasSponsoredBy` | `lack:associatedWith` |
| `lack:wasSponsoredBy` | was sponsored by | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:sponsored` | `lack:associatedWith` |

Covers sponsorship, promotion, patronage, and support.

### Association

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:associatedWith` | associated with | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:associatedWith` *(symmetric)* | |

General-purpose association or affiliation. Used when no more specific relation applies. This is the top-level relation from which most other relations in this ontology are derived.

### Ownership & Acquisition

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:acquired` | acquired | `lack:Collective` | `lack:Collective` | `lack:wasAcquiredBy` | `lack:associatedWith` |
| `lack:wasAcquiredBy` | was acquired by | `lack:Collective` | `lack:Collective` | `lack:acquired` | `lack:associatedWith` |

Covers acquisition, ownership, controlling interest, and shareholding.

### Derivation

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:derivedFrom` | derived from | `lack:Collective` | `lack:Collective` | `lack:hasDerivation` | `lack:associatedWith` |
| `lack:hasDerivation` | has derivation | `lack:Collective` | `lack:Collective` | `lack:derivedFrom` | `lack:associatedWith` |

### Event Organisation

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:organised` | organised | `lack:Person` \| `lack:Collective` | `lack:Collective` | `lack:wasOrganisedBy` | `lack:associatedWith` |
| `lack:wasOrganisedBy` | was organised by | `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:organised` | `lack:associatedWith` |

### Identity & Naming

We reuse `owl:sameAs` to cover identity, renaming, aliases, and doing-business-as relations.

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `owl:sameAs` | same as | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `owl:sameAs` *(symmetric)* | |

### Temporal Activity (entity-level)

These datatype properties attach temporal bounds directly to a `lack:Person` or `lack:Collective`.

| Term | Label | Domain | Range | Note |
|---|---|---|---|---|
| `lack:activeSince` | active since | `lack:Person` \| `lack:Collective` | `xsd:gYear` | Datatype property — no inverse |
| `lack:activeUntil` | active until | `lack:Person` \| `lack:Collective` | `xsd:gYear` | Datatype property — no inverse |

---

## Reification of Temporal Relations

When a relation is annotated with temporal information (`since`, `until`, or `when`), it is represented using **RDF reification** (`rdf:Statement`). The base triple is always asserted directly in addition to the reified statement.

| Term | Label | Domain | Range | Note |
|---|---|---|---|---|
| `lack:since` | since | `rdf:Statement` | `xsd:gYear` | Start year of the relation |
| `lack:until` | until | `rdf:Statement` | `xsd:gYear` | End year of the relation |

When the source annotation is `when` (a point in time rather than an interval), both `lack:since` and `lack:until` are set to the same year value.

### Example

```turtle
@prefix lack: <https://purl.net/climatesense/lack/ns#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

# Base triple always asserted
lack-entity:alice lack:employedBy lack-entity:org .

# Reified statement with interval
[] a rdf:Statement ;
    rdf:subject   lack-entity:alice ;
    rdf:predicate lack:employedBy ;
    rdf:object    lack-entity:org ;
    lack:since    "2010"^^xsd:gYear ;
    lack:until    "2020"^^xsd:gYear .

# Reified statement with point-in-time (when → since = until)
[] a rdf:Statement ;
    rdf:subject   lack-entity:alice ;
    rdf:predicate lack:memberOf ;
    rdf:object    lack-entity:boardX ;
    lack:since    "2015"^^xsd:gYear ;
    lack:until    "2015"^^xsd:gYear .
```

---

## Full Vocabulary Summary

| Term | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|
| `lack:memberOf` | `lack:Person` | `lack:Collective` | `lack:hasMember` | `lack:associatedWith` |
| `lack:hasMember` | `lack:Collective` | `lack:Person` | `lack:memberOf` | `lack:associatedWith` |
| `lack:employedBy` | `lack:Person` | `lack:Collective` | `lack:hasEmployee` | `lack:associatedWith` |
| `lack:hasEmployee` | `lack:Collective` | `lack:Person` | `lack:employedBy` | `lack:associatedWith` |
| `lack:leadsAt` | `lack:Person` | `lack:Collective` | `lack:hasLeader` | `lack:employedBy` |
| `lack:hasLeader` | `lack:Collective` | `lack:Person` | `lack:leadsAt` | `lack:associatedWith` |
| `lack:fundedBy` | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:hasFunder` | `lack:associatedWith` |
| `lack:hasFunder` | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:fundedBy` | `lack:associatedWith` |
| `lack:founded` | `lack:Person` \| `lack:Collective` | `lack:Collective` | `lack:wasFoundedBy` | `lack:associatedWith` |
| `lack:wasFoundedBy` | `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:founded` | `lack:associatedWith` |
| `lack:contributedTo` | `lack:Person` \| `lack:Collective` | `lack:Collective` | `lack:hasContributor` | |
| `lack:hasContributor` | `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:contributedTo` | |
| `lack:hasPartner` | `lack:Collective` | `lack:Collective` | *(symmetric)* | `lack:associatedWith` |
| `lack:sponsored` | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:wasSponsoredBy` | `lack:associatedWith` |
| `lack:wasSponsoredBy` | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:sponsored` | `lack:associatedWith` |
| `lack:associatedWith` | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | *(symmetric)* | |
| `lack:acquired` | `lack:Collective` | `lack:Collective` | `lack:wasAcquiredBy` | `lack:associatedWith` |
| `lack:wasAcquiredBy` | `lack:Collective` | `lack:Collective` | `lack:acquired` | `lack:associatedWith` |
| `lack:derivedFrom` | `lack:Collective` | `lack:Collective` | `lack:hasDerivation` | `lack:associatedWith` |
| `lack:hasDerivation` | `lack:Collective` | `lack:Collective` | `lack:derivedFrom` | `lack:associatedWith` |
| `lack:organised` | `lack:Person` \| `lack:Collective` | `lack:Collective` | `lack:wasOrganisedBy` | `lack:associatedWith` |
| `lack:wasOrganisedBy` | `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:organised` | `lack:associatedWith` |
| `owl:sameAs` | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | *(symmetric)* | |
| `lack:activeSince` | `lack:Person` \| `lack:Collective` | `xsd:gYear` | *(datatype property)* | |
| `lack:activeUntil` | `lack:Person` \| `lack:Collective` | `xsd:gYear` | *(datatype property)* | |
| `lack:since` | `rdf:Statement` | `xsd:gYear` | *(datatype property — reification)* | |
| `lack:until` | `rdf:Statement` | `xsd:gYear` | *(datatype property — reification)* | |

---

## Schema.org Alignment

A mapping exercise to schema.org has been conducted. Key findings:

- **Heavy reliance on `schema:memberOf + roleName`** — schema.org has no dedicated properties for most named organisational roles (CEO, chair, treasurer, VP, etc.). The recommended pattern is to use `schema:memberOf` with a `schema:Role` wrapper and a `roleName` literal to capture the specific title.
- **Inverse direction mismatches** — many relations (funded, published, created, employed) are naturally expressed person→org in LACK, but schema.org models the predicate on the receiving entity (e.g. `schema:funder` is a property of the funded thing).
- **No-match cases** — highly specific operational or contractual relations (lobbied for, conducted public relations for, created a crisis plan for, launched, incorporated) have no schema.org equivalent and are better represented with custom predicates in a domain-specific vocabulary such as LACK.

---

## Competency Questions

The following competency questions were used to drive the design of the ontology and the knowledge extraction process, and were refined based on data quality assessment after extraction. They represent the key questions that LACK is designed to answer.

### Transparency and Disclosure

- **CQ1:** Which persons and organisations are involved in lobbying against climate science or policy?
- **CQ2:** Which organisations fund a given person or organisation, and what is the evidence for each funding relationship?
- **CQ3:** Which persons are members of a given organisation, and during which period?
- **CQ4:** Who are the leaders of a given organisation, and when did they hold that role?
- **CQ5:** Which organisations has a given person been employed by, and in what time periods?

### Network Structure

- **CQ6:** Which organisations are partners of a given organisation?
- **CQ7:** Which organisations were founded by a given person or organisation?
- **CQ8:** Which organisations is a given organisation derived from, or has acquired?
- **CQ9:** Which persons or organisations are associated with a given entity (direct and indirect connections)?

### Temporal Reasoning

- **CQ10:** Which relationships involving a given entity were active during a specific time interval?
- **CQ11:** Which organisations were active during a given period?

### Identity and Deduplication

- **CQ12:** Which entities in the graph refer to the same real-world person or organisation?

