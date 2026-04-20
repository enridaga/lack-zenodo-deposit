#!/usr/bin/env python3
"""
build.py — LACK Knowledge Graph static site builder.

Usage:
    python build.py

Reads:  config.yaml, content/*.md, templates/base.html, static/, *.ttl, *.omn, KGSTATS.md
Writes: _site/
"""

import os
import re
import shutil
import yaml
import argparse
import markdown as md_lib
from collections import defaultdict

# ── Paths ──────────────────────────────────────────────────────────────────────

ROOT         = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR  = os.path.join(ROOT, "content")
STATIC_DIR   = os.path.join(ROOT, "static")
TEMPLATE_FILE= os.path.join(ROOT, "templates", "base.html")
CONFIG_FILE  = os.path.join(ROOT, "config.yaml")
OUTPUT_DIR   = os.path.join(ROOT, "_site")
KG_FILE      = os.path.join(ROOT, "KG.ttl")
KGSTATS_FILE = os.path.join(ROOT, "KGSTATS.md")

# Extra files to copy verbatim into _site root
VERBATIM_FILES = ["lack-ontology.ttl", "lack-ontology.omn", "KG.ttl"]

# ── KGSTATS.md parsing ─────────────────────────────────────────────────────────

def parse_kgstats(path):
    """
    Parse KGSTATS.md and return a flat dict of kg_* placeholder values
    for use in content/knowledge-graph.md substitution.
    """
    if not os.path.exists(path):
        print(f"  WARNING: {path} not found — KG placeholders will not be substituted.")
        return {}

    print("  Parsing KGSTATS.md...")

    with open(path, encoding="utf-8") as f:
        text = f.read()

    before   = _extract_section(text, "BEFORE INFERENCING")
    inferred = _extract_section(text, "INFERRED")
    after    = _extract_section(text, "AFTER INFERENCING")

    # Entity counts
    total_entities  = _first_int(before, r"^(\d+)$")
    entity_links    = _parse_csv_block(before, "type,count,wikidata,dbpedia")
    persons_row     = _row_by_key(entity_links, "lack/ns#Person")
    collectives_row = _row_by_key(entity_links, "lack/ns#Collective")

    total_persons      = int(persons_row["count"])      if persons_row     else 0
    total_collectives  = int(collectives_row["count"])  if collectives_row else 0
    wikidata_persons   = int(persons_row["wikidata"])   if persons_row     else 0
    wikidata_collectives = int(collectives_row["wikidata"]) if collectives_row else 0
    dbpedia_persons    = int(persons_row["dbpedia"])    if persons_row     else 0
    dbpedia_collectives= int(collectives_row["dbpedia"])if collectives_row else 0

    wikidata_total = wikidata_persons + wikidata_collectives
    dbpedia_total  = dbpedia_persons  + dbpedia_collectives
    unlinked       = total_entities   - wikidata_total

    # Relation counts
    asserted_total = _first_int(before,   r"^(\d+)$", skip=1)
    inferred_total = _first_int(inferred, r"^(\d+)$", skip=1)
    after_total    = _first_int(after,    r"^(\d+)$", skip=1)

    # Asserted relation breakdown
    rel_rows = _parse_csv_block(before, "relation,count")
    rel_map  = {r["relation"].split("#")[-1]: int(r["count"]) for r in rel_rows}

    def pct(n, total):
        return f"{round(n / total * 100)}%" if total else "n/a"

    placeholders = {
        "kg_total_entities":    f"{total_entities:,}",
        "kg_total_persons":     f"{total_persons:,}",
        "kg_total_collectives": f"{total_collectives:,}",
        "kg_wikidata_links":    f"{wikidata_total:,}",
        "kg_dbpedia_links":     f"{dbpedia_total:,}",
        "kg_asserted":          f"{asserted_total:,}",
        "kg_inferred":          f"{inferred_total:,}",
        "kg_total":             f"{after_total:,}",
        "kg_wikidata_pct":      pct(wikidata_total, total_entities),
        "kg_dbpedia_pct":       pct(dbpedia_total,  total_entities),
        "kg_unlinked":          f"{unlinked:,}",
        "kg_unlinked_pct":      pct(unlinked, total_entities),
        "kg_asserted_inf":      f"{asserted_total:,}",
        "kg_inferred_inf":      f"{inferred_total:,}",
        "kg_total_inf":         f"{after_total:,}",
        **{f"kg_rel_{k}": f"{v:,}" for k, v in rel_map.items()},
    }

    # Store raw numbers for dashboard rendering
    placeholders["_total_entities"]  = total_entities
    placeholders["_total_persons"]   = total_persons
    placeholders["_total_collectives"]= total_collectives
    placeholders["_asserted_total"]  = asserted_total
    placeholders["_after_total"]     = after_total
    placeholders["_wikidata_total"]  = wikidata_total
    placeholders["_rel_map"]         = rel_map

    print(f"    Entities: {total_entities:,}  Asserted: {asserted_total:,}  "
          f"Inferred: {inferred_total:,}  Total: {after_total:,}")
    return placeholders


def _extract_section(text, heading):
    pattern = re.compile(
        r"###\s+" + re.escape(heading) + r".*?\n(.*?)(?=\n###|\Z)",
        re.DOTALL | re.IGNORECASE
    )
    m = pattern.search(text)
    return m.group(1) if m else ""


def _first_int(text, pattern, skip=0):
    matches = re.findall(pattern, text, re.MULTILINE)
    try:
        return int(matches[skip])
    except (IndexError, ValueError):
        return 0


def _parse_csv_block(text, header):
    lines = text.splitlines()
    rows, in_block, keys = [], False, []
    for line in lines:
        line = line.strip()
        if line == header:
            keys, in_block = header.split(","), True
            continue
        if in_block:
            if not line or line.startswith("#"):
                break
            parts = line.split(",")
            if len(parts) == len(keys):
                rows.append(dict(zip(keys, parts)))
    return rows


def _row_by_key(rows, key_fragment):
    for row in rows:
        if key_fragment in list(row.values())[0]:
            return row
    return None


def apply_kg_placeholders(text, placeholders):
    """Replace all {{ kg_* }} tokens in text with values from placeholders dict."""
    def replacer(m):
        key = m.group(1).strip()
        return placeholders.get(key, m.group(0))
    return re.sub(r"\{\{\s*(kg_\w+)\s*\}\}", replacer, text)


# ── SPARQL queries (rdflib) ────────────────────────────────────────────────────

def query_kg_sparql(kg_path):
    """
    Run three targeted SPARQL queries against KG.ttl using rdflib.
    Returns a dict with: source_counts, year_range, subtype_counts.
    """
    if not os.path.exists(kg_path):
        print(f"  WARNING: {kg_path} not found — SPARQL stats unavailable.")
        return {"source_counts": {}, "year_range": (None, None), "subtype_counts": []}

    print("  Loading KG.ttl for SPARQL queries (this may take a moment)...")
    try:
        from rdflib import Graph, Namespace
        from rdflib.namespace import RDF, RDFS, OWL, XSD
    except ImportError:
        print("  WARNING: rdflib not installed — SPARQL stats unavailable.")
        return {"source_counts": {}, "year_range": (None, None), "subtype_counts": []}

    g = Graph()
    g.parse(kg_path, format="turtle")
    print(f"  Loaded {len(g):,} triples.")

    # ── Query 1: Evidence source counts ───────────────────────────────────────
    source_q = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?source (COUNT(*) AS ?count) WHERE {
      ?e rdfs:seeAlso ?url .
      BIND(
        IF(CONTAINS(STR(?url), "desmog.com"),      "Desmog",
        IF(CONTAINS(STR(?url), "lobbymap.org"),    "LobbyMap",
        IF(CONTAINS(STR(?url), "influencemap.org"),"InfluenceMap",
        "Other"))) AS ?source)
    }
    GROUP BY ?source
    ORDER BY DESC(?count)
    """
    source_counts = {}
    for row in g.query(source_q):
        source_counts[str(row.source)] = int(row["count"])

    # ── Query 2: Year range ────────────────────────────────────────────────────
    year_q = """
    PREFIX lack: <https://purl.net/climatesense/lack/ns#>
    PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
    SELECT ?y WHERE {
      ?s ?p ?y .
      FILTER(?p IN (lack:since, lack:until, lack:activeSince, lack:activeUntil))
      FILTER(DATATYPE(?y) = xsd:gYear)
    }
    """
    years = []
    for row in g.query(year_q):
        try:
            years.append(int(str(row.y)[:4]))
        except ValueError:
            pass
    year_range = (str(min(years)), str(max(years))) if years else (None, None)
    # ── Query 3: Entity counts per lack-type subtype ───────────────────────────
    subtype_q = """
    PREFIX lack-type: <https://purl.net/climatesense/lack/type/>
    PREFIX rdf:       <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?subtype (COUNT(DISTINCT ?e) AS ?count) WHERE {
      ?e rdf:type ?subtype .
      FILTER(STRSTARTS(STR(?subtype), STR(lack-type:)))
    }
    GROUP BY ?subtype
    ORDER BY DESC(?count)
    """
    subtype_counts = []
    for row in g.query(subtype_q):
        label = str(row.subtype).split("/")[-1].replace("_", " ")
        subtype_counts.append((label, int(row["count"])))

    print(f"    Sources: {source_counts}  Year range: {year_range}  "
          f"Subtypes: {len(subtype_counts)}")
    return {
        "source_counts":  source_counts,
        "year_range":     year_range,
        "subtype_counts": subtype_counts,
    }


# ── Stats dashboard HTML ───────────────────────────────────────────────────────

def render_stats_html(kg_placeholders, sparql_stats):
    """
    Build the static stats dashboard HTML from KGSTATS.md data
    and the three SPARQL query results.
    """
    if not kg_placeholders:
        return ""

    def bar_chart(items, max_val, css_class=""):
        rows = []
        for label, count in items:
            pct = int(count / max_val * 100) if max_val else 0
            rows.append(
                f'<div class="bar-row">'
                f'<span class="bar-label">{label}</span>'
                f'<span class="bar-wrap"><span class="bar-fill{" " + css_class if css_class else ""}"'
                f' style="width:{pct}%"></span></span>'
                f'<span class="bar-count">{count:,}</span>'
                f'</div>'
            )
        return "\n".join(rows)

    # Summary cards
    total_entities   = kg_placeholders["_total_entities"]
    total_persons    = kg_placeholders["_total_persons"]
    total_collectives= kg_placeholders["_total_collectives"]
    after_total      = kg_placeholders["_after_total"]
    wikidata_total   = kg_placeholders["_wikidata_total"]
    yr               = sparql_stats["year_range"]
    year_str         = f"{yr[0]}–{yr[1]}" if yr[0] else "n/a"

    # Entity subtype bar chart (from SPARQL)
    subtype_items = sparql_stats["subtype_counts"][:12]
    max_subtype   = subtype_items[0][1] if subtype_items else 1

    # Relation breakdown bar chart (from KGSTATS.md)
    rel_map   = kg_placeholders["_rel_map"]
    rel_items = sorted(rel_map.items(), key=lambda x: -x[1])[:10]
    max_rel   = rel_items[0][1] if rel_items else 1

    # Source bar chart (from SPARQL)
    src_items = sorted(sparql_stats["source_counts"].items(), key=lambda x: -x[1])
    max_src   = src_items[0][1] if src_items else 1

    html = f"""
<div class="stats-dashboard">

  <div class="stat-cards">
    <div class="stat-card">
      <span class="stat-number">{total_entities:,}</span>
      <span class="stat-label">entities</span>
    </div>
    <div class="stat-card">
      <span class="stat-number">{total_persons:,}</span>
      <span class="stat-label">persons</span>
    </div>
    <div class="stat-card">
      <span class="stat-number">{total_collectives:,}</span>
      <span class="stat-label">collectives</span>
    </div>
    <div class="stat-card">
      <span class="stat-number">{after_total:,}</span>
      <span class="stat-label">total triples</span>
    </div>
    <div class="stat-card">
      <span class="stat-number">{wikidata_total:,}</span>
      <span class="stat-label">Wikidata links</span>
    </div>
    <div class="stat-card">
      <span class="stat-number">{year_str}</span>
      <span class="stat-label">temporal coverage</span>
    </div>
  </div>

  <div class="chart-grid">
    <div class="chart-block">
      <h3>Entities by subtype</h3>
      <div class="bar-chart">
        {bar_chart(subtype_items, max_subtype)}
      </div>
    </div>
    <div class="chart-block">
      <h3>Relations by predicate (asserted)</h3>
      <div class="bar-chart">
        {bar_chart(rel_items, max_rel, css_class="yellow")}
      </div>
    </div>
  </div>

  <div class="chart-block" style="margin-top:1.5rem">
    <h3>Evidence sources</h3>
    <div class="bar-chart">
      {bar_chart(src_items, max_src)}
    </div>
  </div>

</div>
"""
    return html


# ── Helpers ────────────────────────────────────────────────────────────────────

def load_config():
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_template():
    with open(TEMPLATE_FILE, encoding="utf-8") as f:
        return f.read()


def parse_frontmatter(text):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if match:
        meta = yaml.safe_load(match.group(1)) or {}
        body = text[match.end():]
    else:
        meta = {}
        body = text
    return meta, body


def slug_from_filename(filename):
    return os.path.splitext(filename)[0]


def html_filename(md_filename):
    return slug_from_filename(md_filename) + ".html"


def build_nav(nav_items, base_url, current_slug):
    items = []
    for item in nav_items:
        if "file" in item:
            slug  = slug_from_filename(item["file"])
            href  = f"{base_url}/{html_filename(item['file'])}"
            active= ' class="active"' if slug == current_slug else ""
        else:
            href  = f"{base_url}/{item['url']}"
            active= ' class="active"' if item.get("label", "") == current_slug else ""
        items.append(f'      <li><a href="{href}"{active}>{item["label"]}</a></li>')
    return "\n".join(items)


def render_page(template, content_html, page_title, nav_html, site_title, base_url):
    content_html = content_html.replace("{{ base_url }}", base_url)
    out = template
    out = out.replace("{{ page_title }}", page_title)
    out = out.replace("{{ site_title }}", site_title)
    out = out.replace("{{ base_url }}", base_url)
    out = out.replace("{{ nav }}", nav_html)
    out = out.replace("{{ content }}", content_html)
    return out


# ── Build ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Build the LACK static site.")
    parser.add_argument("--local", action="store_true",
                        help="Override base_url to '' for local serving from _site/")
    args = parser.parse_args()

    config     = load_config()
    site_title = config["site_title"]
    base_url   = "" if args.local else config.get("base_url", "").rstrip("/")
    nav_items  = config["nav"]
    template   = load_template()

    # Parse stats sources
    kg_placeholders = parse_kgstats(KGSTATS_FILE)
    sparql_stats    = query_kg_sparql(KG_FILE)
    stats_html      = render_stats_html(kg_placeholders, sparql_stats)

    # Clean and recreate output directory
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # Copy static assets
    out_static = os.path.join(OUTPUT_DIR, "static")
    shutil.copytree(STATIC_DIR, out_static)
    print(f"  Copied static/ → _site/static/")

    # Copy verbatim files
    for fname in VERBATIM_FILES:
        src = os.path.join(ROOT, fname)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(OUTPUT_DIR, fname))
            print(f"  Copied {fname} → _site/{fname}")
        else:
            print(f"  WARNING: {fname} not found, skipping.")

    md_extensions = ["tables", "fenced_code", "attr_list", "def_list"]

    for item in nav_items:
        if "url" in item:
            print(f"  Skipped nav item '{item['label']}' (static URL: {item['url']})")
            continue

        md_file  = item["file"]
        md_path  = os.path.join(CONTENT_DIR, md_file)

        if not os.path.exists(md_path):
            print(f"  WARNING: {md_path} not found, skipping.")
            continue

        with open(md_path, encoding="utf-8") as f:
            raw = f.read()

        meta, body = parse_frontmatter(raw)

        # Apply KG placeholders before markdown rendering
        if md_file == "knowledge-graph.md":
            body = apply_kg_placeholders(body, kg_placeholders)

        page_title   = meta.get("title", item["label"])
        content_html = md_lib.markdown(body, extensions=md_extensions)
        content_html = content_html.replace("{{ stats_dashboard }}", stats_html)

        current_slug = slug_from_filename(md_file)
        nav_html     = build_nav(nav_items, base_url, current_slug)
        page_html    = render_page(
            template, content_html, page_title, nav_html, site_title, base_url
        )

        out_filename = html_filename(md_file)
        out_path     = os.path.join(OUTPUT_DIR, out_filename)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_html)

        print(f"  Built {md_file} → _site/{out_filename}")

    print(f"\nDone. Site written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()