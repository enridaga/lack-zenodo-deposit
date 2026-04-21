#!/usr/bin/env python3
"""
annotate_paths.py — Read paths-added.csv and produce a structured output
with human-readable labels for all entities and relations, sourced from KG.ttl.

Usage:
    python annotate_paths.py

Output: paths-annotated.csv
"""

import csv
from rdflib import Graph, URIRef
from rdflib.namespace import RDFS

KG_FILE     = "KG.ttl"
INPUT_FILE  = "paths-added.csv"
OUTPUT_FILE = "paths-annotated.csv"

COLUMNS = ["entity", "relation", "proxy", "relation1", "target"]


def load_labels(kg_path):
    """Load all rdfs:label triples from the KG into a URI -> label dict."""
    g = Graph()
    g.parse(kg_path, format="turtle")
    labels = {}
    for s, _, o in g.triples((None, RDFS.label, None)):
        labels[str(s)] = str(o)
    return labels


def get_label(uri, labels):
    """Return the rdfs:label for a URI, falling back to the URI itself."""
    return labels.get(uri, uri)


def main():
    labels = load_labels(KG_FILE)

    with open(INPUT_FILE, newline="", encoding="utf-8") as f_in, \
         open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f_out:

        reader = csv.DictReader(f_in)

        out_columns = [
            "entity",       "entity_label",
            "relation",     "relation_label",
            "proxy",        "proxy_label",
            "relation1",    "relation1_label",
            "target",       "target_label",
        ]
        writer = csv.DictWriter(f_out, fieldnames=out_columns)
        writer.writeheader()

        for row in reader:
            writer.writerow({
                "entity":        row["entity"],
                "entity_label":  get_label(row["entity"],   labels),
                "relation":      row["relation"],
                "relation_label":get_label(row["relation"],  labels),
                "proxy":         row["proxy"],
                "proxy_label":   get_label(row["proxy"],     labels),
                "relation1":     row["relation1"],
                "relation1_label":get_label(row["relation1"],labels),
                "target":        row["target"],
                "target_label":  get_label(row["target"],    labels),
            })

    print(f"Done. Annotated output written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()