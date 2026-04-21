#!/usr/bin/env python3
"""
generate-case-studies.py

Reads content/case-studies.csv and queries KG.ttl to extract all triples
needed to build the case study pages. Writes case-studies.ttl containing:

  - rdfs:label for all entities in the paths (entity, proxy, target)
  - rdfs:seeAlso / rdf:type for those entities
  - All rdf:Statement instances (lack-stmt:) for each hop, with full
    provenance (prov:wasDerivedFrom, rdfs:seeAlso, dct:source,
    lack:since, lack:until, prov:wasGeneratedBy)
  - The base triples for each hop

Usage:
    python generate-case-studies.py

Input:  content/case-studies.csv, KG.ttl
Output: case-studies.ttl
"""

import csv
import os
import sys
import time

ROOT        = os.path.dirname(os.path.abspath(__file__))
CSV_PATH    = os.path.join(ROOT, "content", "case-studies.csv")
KG_PATH     = os.path.join(ROOT, "KG.ttl")
OUTPUT_PATH = os.path.join(ROOT, "case-studies.ttl")

try:
    from rdflib import Graph, Namespace, URIRef, Literal
    from rdflib.namespace import RDF, RDFS, OWL, XSD
except ImportError:
    print("ERROR: rdflib is required. Install with: pip install rdflib")
    sys.exit(1)

# ── Namespaces ─────────────────────────────────────────────────────────────────

LACK      = Namespace("https://purl.net/climatesense/lack/ns#")
LACK_ENT  = Namespace("https://purl.net/climatesense/lack/entity/")
LACK_STMT = Namespace("https://purl.net/climatesense/lack/stmt/")
LACK_PROV = Namespace("https://purl.net/climatesense/lack/prov/")
LACK_TYPE = Namespace("https://purl.net/climatesense/lack/type/")
PROV      = Namespace("http://www.w3.org/ns/prov#")
DCT       = Namespace("http://purl.org/dc/terms/")
CS        = Namespace("https://purl.net/climatesense/lack/case-study/")


# ── Load case studies CSV ──────────────────────────────────────────────────────

def load_case_studies(path):
    cases = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            cases.append({
                "id":             i,
                "entity":         URIRef(row["entity"]),
                "entity_label":   row["entity_label"],
                "relation":       URIRef(row["relation"]),
                "relation_label": row["relation_label"],
                "proxy":          URIRef(row["proxy"]),
                "proxy_label":    row["proxy_label"],
                "relation1":      URIRef(row["relation1"]),
                "relation1_label":row["relation1_label"],
                "target":         URIRef(row["target"]),
                "target_label":   row["target_label"],
            })
    return cases


# ── Load KG ────────────────────────────────────────────────────────────────────

def load_kg(path):
    print(f"Loading {path} (this may take a moment)...")
    t0 = time.time()
    g = Graph()
    g.parse(path, format="turtle")
    print(f"  Loaded {len(g):,} triples in {time.time()-t0:.1f}s")
    return g


# ── SPARQL: fetch statements for a given (subject, predicate, object) hop ──────

STMT_QUERY = """
PREFIX rdf:       <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:      <http://www.w3.org/2000/01/rdf-schema#>
PREFIX prov:      <http://www.w3.org/ns/prov#>
PREFIX dct:       <http://purl.org/dc/terms/>
PREFIX lack:      <https://purl.net/climatesense/lack/ns#>

SELECT ?stmt ?seeAlso ?source ?derivedFrom ?since ?until ?generatedBy
WHERE {
  ?stmt a rdf:Statement ;
        rdf:subject   ?subj ;
        rdf:predicate ?pred ;
        rdf:object    ?obj .
  OPTIONAL { ?stmt rdfs:seeAlso      ?seeAlso    }
  OPTIONAL { ?stmt dct:source        ?source     }
  OPTIONAL { ?stmt prov:wasDerivedFrom ?derivedFrom }
  OPTIONAL { ?stmt lack:since        ?since      }
  OPTIONAL { ?stmt lack:until        ?until      }
  OPTIONAL { ?stmt prov:wasGeneratedBy ?generatedBy }
}
"""

def fetch_statements(kg, subject, predicate, obj):
    """Return list of dicts, one per rdf:Statement matching the triple."""
    results = []
    for row in kg.query(
        STMT_QUERY,
        initBindings={"subj": subject, "pred": predicate, "obj": obj}
    ):
        results.append({
            "stmt":        row.stmt,
            "seeAlso":     row.seeAlso,
            "source":      row.source,
            "derivedFrom": row.derivedFrom,
            "since":       row.since,
            "until":       row.until,
            "generatedBy": row.generatedBy,
        })
    return results


# ── SPARQL: fetch entity metadata (label, type, seeAlso, sameAs) ───────────────

ENTITY_QUERY = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>

SELECT ?label ?type ?seeAlso ?sameAs
WHERE {
  OPTIONAL { ?e rdfs:label  ?label  }
  OPTIONAL { ?e rdf:type    ?type   }
  OPTIONAL { ?e rdfs:seeAlso ?seeAlso }
  OPTIONAL { ?e owl:sameAs  ?sameAs }
}
"""

def fetch_entity_triples(kg, entity_uri):
    """Return all metadata triples for a given entity URI."""
    rows = list(kg.query(
        ENTITY_QUERY,
        initBindings={"e": entity_uri}
    ))
    return rows


# ── Build output graph ─────────────────────────────────────────────────────────

def build_output_graph(kg, cases):
    out = Graph()

    # Bind prefixes
    out.bind("lack",      LACK)
    out.bind("lack-entity", LACK_ENT)
    out.bind("lack-stmt", LACK_STMT)
    out.bind("lack-prov", LACK_PROV)
    out.bind("lack-type", LACK_TYPE)
    out.bind("prov",      PROV)
    out.bind("dct",       DCT)
    out.bind("rdf",       RDF)
    out.bind("rdfs",      RDFS)
    out.bind("owl",       OWL)
    out.bind("xsd",       XSD)
    out.bind("cs",        CS)

    entities_done = set()

    def add_entity(uri):
        if uri in entities_done:
            return
        entities_done.add(uri)
        rows = fetch_entity_triples(kg, uri)
        for row in rows:
            if row.label:
                out.add((uri, RDFS.label, row.label))
            if row.type:
                out.add((uri, RDF.type, row.type))
            if row.seeAlso:
                out.add((uri, RDFS.seeAlso, row.seeAlso))
            if row.sameAs:
                out.add((uri, OWL.sameAs, row.sameAs))

    for case in cases:
        cs_uri = CS[f"cs-{case['id']}"]
        print(f"\nCase {case['id']}: {case['entity_label']} → {case['proxy_label']} → {case['target_label']}")

        # Add case study metadata to output graph
        out.add((cs_uri, RDF.type, CS.CaseStudy))
        out.add((cs_uri, RDFS.label, Literal(
            f"{case['entity_label']} → {case['proxy_label']} → {case['target_label']}"
        )))
        out.add((cs_uri, CS.entity,   case["entity"]))
        out.add((cs_uri, CS.relation, case["relation"]))
        out.add((cs_uri, CS.proxy,    case["proxy"]))
        out.add((cs_uri, CS.relation1, case["relation1"]))
        out.add((cs_uri, CS.target,   case["target"]))

        # Add entity metadata
        for uri in [case["entity"], case["proxy"], case["target"]]:
            add_entity(uri)

        # Hop 1: entity → relation → proxy
        hop1_stmts = fetch_statements(
            kg, case["entity"], case["relation"], case["proxy"]
        )
        print(f"  Hop 1 ({case['relation_label']}): {len(hop1_stmts)} statement(s)")

        # Assert base triple
        out.add((case["entity"], case["relation"], case["proxy"]))

        for s in hop1_stmts:
            stmt_uri = s["stmt"]
            out.add((stmt_uri, RDF.type,          RDF.Statement))
            out.add((stmt_uri, RDF.subject,        case["entity"]))
            out.add((stmt_uri, RDF.predicate,      case["relation"]))
            out.add((stmt_uri, RDF.object,         case["proxy"]))
            if s["seeAlso"]:
                out.add((stmt_uri, RDFS.seeAlso,   s["seeAlso"]))
            if s["source"]:
                out.add((stmt_uri, DCT.source,     s["source"]))
            if s["derivedFrom"]:
                out.add((stmt_uri, PROV.wasDerivedFrom, s["derivedFrom"]))
            if s["since"]:
                out.add((stmt_uri, LACK.since,     s["since"]))
            if s["until"]:
                out.add((stmt_uri, LACK.until,     s["until"]))
            if s["generatedBy"]:
                out.add((stmt_uri, PROV.wasGeneratedBy, s["generatedBy"]))

        # Hop 2: proxy → relation1 → target
        hop2_stmts = fetch_statements(
            kg, case["proxy"], case["relation1"], case["target"]
        )
        print(f"  Hop 2 ({case['relation1_label']}): {len(hop2_stmts)} statement(s)")

        # Assert base triple
        out.add((case["proxy"], case["relation1"], case["target"]))

        for s in hop2_stmts:
            stmt_uri = s["stmt"]
            out.add((stmt_uri, RDF.type,          RDF.Statement))
            out.add((stmt_uri, RDF.subject,        case["proxy"]))
            out.add((stmt_uri, RDF.predicate,      case["relation1"]))
            out.add((stmt_uri, RDF.object,         case["target"]))
            if s["seeAlso"]:
                out.add((stmt_uri, RDFS.seeAlso,   s["seeAlso"]))
            if s["source"]:
                out.add((stmt_uri, DCT.source,     s["source"]))
            if s["derivedFrom"]:
                out.add((stmt_uri, PROV.wasDerivedFrom, s["derivedFrom"]))
            if s["since"]:
                out.add((stmt_uri, LACK.since,     s["since"]))
            if s["until"]:
                out.add((stmt_uri, LACK.until,     s["until"]))
            if s["generatedBy"]:
                out.add((stmt_uri, PROV.wasGeneratedBy, s["generatedBy"]))

    return out


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("=== generate-case-studies.py ===\n")

    if not os.path.exists(CSV_PATH):
        print(f"ERROR: {CSV_PATH} not found.")
        sys.exit(1)
    if not os.path.exists(KG_PATH):
        print(f"ERROR: {KG_PATH} not found.")
        sys.exit(1)

    cases = load_case_studies(CSV_PATH)
    print(f"Loaded {len(cases)} case studies from CSV.")

    kg = load_kg(KG_PATH)

    out = build_output_graph(kg, cases)

    print(f"\nWriting {len(out):,} triples to {OUTPUT_PATH}...")
    out.serialize(destination=OUTPUT_PATH, format="turtle")
    print("Done.")


if __name__ == "__main__":
    main()
