#!/usr/bin/env python3
"""
build.py — LACK Knowledge Graph static site builder.

Usage:
    python build.py

Reads:  config.yaml, content/*.md, templates/base.html, static/, *.ttl, *.omn, KG.ttl
Writes: _site/
"""

import os
import re
import shutil
import json
import yaml
import markdown as md_lib
from collections import defaultdict

# ── Paths ──────────────────────────────────────────────────────────────────────

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(ROOT, "content")
STATIC_DIR = os.path.join(ROOT, "static")
TEMPLATE_FILE = os.path.join(ROOT, "templates", "base.html")
CONFIG_FILE = os.path.join(ROOT, "config.yaml")
OUTPUT_DIR = os.path.join(ROOT, "_site")
KG_FILE = os.path.join(ROOT, "KG.ttl")

# Extra files to copy verbatim into _site root
VERBATIM_FILES = ["lack-ontology.ttl", "lack-ontology.omn", "KG.ttl"]

# Relation predicates in the lack: namespace to count
LACK_RELATIONS = [
    "memberOf", "hasMember",
    "employedBy", "hasEmployee",
    "leadsAt", "hasLeader",
    "fundedBy", "hasFunder",
    "founded", "wasFoundedBy",
    "contributedTo", "hasContributor",
    "hasPartner",
    "sponsored", "wasSponsoredBy",
    "associatedWith",
    "acquired", "wasAcquiredBy",
    "derivedFrom", "hasDerivation",
    "organised", "wasOrganisedBy",
]

# ── KG parsing ─────────────────────────────────────────────────────────────────

def parse_kg_stats(kg_path):
    """
    Parse KG.ttl with simple regex (no rdflib dependency).
    Returns a dict of stats for use in templates.
    """
    if not os.path.exists(kg_path):
        print(f"  WARNING: {kg_path} not found — skipping stats generation.")
        return None

    print("  Parsing KG.ttl for stats...")

    type_counts = defaultdict(int)
    relation_counts = defaultdict(int)
    source_counts = defaultdict(int)
    year_counts = defaultdict(int)
    wikidata_linked = 0

    re_type = re.compile(r'rdf:type\s+lack-type:(\w+)')
    re_person = re.compile(r'rdf:type\s+lack:Person|rdf:type\s+<https://purl\.net/climatesense/lack/ns#Person>')
    re_relation = re.compile(r'\b(?:lack:)(' + '|'.join(LACK_RELATIONS) + r')\b')
    re_see_also = re.compile(r'rdfs:seeAlso\s+"(https?://[^"]+)"')
    re_year = re.compile(r'lack:(?:since|until|activeSince|activeUntil)\s+"(\d{4})"|<https://purl\.net/climatesense/lack/ns#(?:since|until|activeSince|activeUntil)>\s+"(\d{4})"|"(\d{4})"\^\^xsd:gYear')
    re_wikidata = re.compile(r'owl:sameAs\s+<https://www\.wikidata\.org/entity/')
    entity_iris = set()

    with open(kg_path, encoding="utf-8", errors="replace") as f:
        content = f.read()

    for m in re.finditer(r'^(lack-entity:[a-f0-9]+)\s*\n', content, re.MULTILINE):
        entity_iris.add(m.group(1))
    total_entities = len(entity_iris)

    wikidata_linked = len(re_wikidata.findall(content))

    for m in re_type.finditer(content):
        t = m.group(1)
        type_counts[t] += 1

    type_counts["person"] = len(re_person.findall(content))

    for m in re_relation.finditer(content):
        relation_counts[m.group(1)] += 1

    for m in re_see_also.finditer(content):
        url = m.group(1)
        if "desmog.com" in url:
            source_counts["Desmog"] += 1
        elif "lobbymap.org" in url or "influencemap.org" in url:
            source_counts["LobbyMap / InfluenceMap"] += 1
        else:
            source_counts["Other"] += 1

    for m in re_year.finditer(content):
        raw = m.group(1) or m.group(2) or m.group(3)
        if raw:
            y = int(raw)
            if 1900 <= y <= 2030:
                year_counts[y] += 1

    total_relations = sum(relation_counts.values())

    GROUP_MAP = {
        "person": "Persons",
        "company": "Companies",
        "think_tank": "Think tanks",
        "foundation": "Foundations",
        "government_agency": "Government agencies",
        "university": "Universities",
        "coalition": "Coalitions",
        "publication": "Publications",
        "industry_association": "Industry associations",
        "trade_association": "Trade associations",
        "professional_association": "Professional associations",
        "consulting_firm": "Consulting firms",
        "political_party": "Political parties",
        "research_institute": "Research institutes",
        "program": "Programs",
        "law_firm": "Law firms",
        "journal": "Journals",
        "country": "Countries",
        "ngo": "NGOs",
    }

    grouped = defaultdict(int)
    other_count = 0
    for k, v in type_counts.items():
        label = GROUP_MAP.get(k)
        if label:
            grouped[label] += v
        else:
            other_count += v
    if other_count:
        grouped["Other"] += other_count

    entity_chart = sorted(grouped.items(), key=lambda x: -x[1])
    relation_chart = sorted(relation_counts.items(), key=lambda x: -x[1])

    years_sorted = sorted(year_counts.keys())
    year_range = (years_sorted[0], years_sorted[-1]) if years_sorted else (None, None)

    stats = {
        "total_entities": total_entities,
        "total_relations": total_relations,
        "wikidata_linked": wikidata_linked,
        "entity_chart": entity_chart,
        "relation_chart": relation_chart,
        "source_counts": dict(source_counts),
        "year_range": year_range,
    }

    print(f"    Entities: {total_entities}, Relations: {total_relations}, Wikidata links: {wikidata_linked}")
    return stats


def render_stats_html(stats):
    """Produce an HTML block with bar charts for entity types and relation counts."""
    if stats is None:
        return ""

    def bar_chart(items, max_val):
        rows = []
        for label, count in items:
            pct = int(count / max_val * 100) if max_val else 0
            rows.append(
                f'<div class="bar-row">'
                f'<span class="bar-label">{label}</span>'
                f'<span class="bar-wrap"><span class="bar-fill" style="width:{pct}%"></span></span>'
                f'<span class="bar-count">{count:,}</span>'
                f'</div>'
            )
        return "\n".join(rows)

    TOP_TYPES = 12
    TOP_RELS = 10

    entity_items = stats["entity_chart"][:TOP_TYPES]
    rel_items = stats["relation_chart"][:TOP_RELS]

    max_entity = entity_items[0][1] if entity_items else 1
    max_rel = rel_items[0][1] if rel_items else 1

    yr = stats["year_range"]
    year_str = f"{yr[0]}–{yr[1]}" if yr[0] else "n/a"

    src = stats["source_counts"]
    src_items = sorted(src.items(), key=lambda x: -x[1])
    max_src = src_items[0][1] if src_items else 1

    html = f"""
<div class="stats-dashboard">

  <div class="stat-cards">
    <div class="stat-card">
      <span class="stat-number">{stats['total_entities']:,}</span>
      <span class="stat-label">entities</span>
    </div>
    <div class="stat-card">
      <span class="stat-number">{stats['total_relations']:,}</span>
      <span class="stat-label">relations</span>
    </div>
    <div class="stat-card">
      <span class="stat-number">{stats['wikidata_linked']:,}</span>
      <span class="stat-label">Wikidata links</span>
    </div>
    <div class="stat-card">
      <span class="stat-number">{year_str}</span>
      <span class="stat-label">temporal coverage</span>
    </div>
  </div>

  <div class="chart-grid">
    <div class="chart-block">
      <h3>Entities by type</h3>
      <div class="bar-chart">
        {bar_chart(entity_items, max_entity)}
      </div>
    </div>
    <div class="chart-block">
      <h3>Relations by predicate</h3>
      <div class="bar-chart">
        {bar_chart(rel_items, max_rel)}
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
    """Render nav <li> items. Supports both file-based and url-based items."""
    items = []
    for item in nav_items:
        if "file" in item:
            slug = slug_from_filename(item["file"])
            href = f"{base_url}/{html_filename(item['file'])}"
            active = ' class="active"' if slug == current_slug else ""
        else:
            # url-based item (e.g. Explore)
            href = f"{base_url}/{item['url']}"
            active = ' class="active"' if item.get("label", "") == current_slug else ""
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
    config = load_config()
    site_title = config["site_title"]
    base_url = config.get("base_url", "").rstrip("/")
    nav_items = config["nav"]

    template = load_template()

    # Parse KG stats
    kg_stats = parse_kg_stats(KG_FILE)
    stats_html = render_stats_html(kg_stats)

    # Clean and recreate output directory
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # Copy static assets (includes explore.html)
    out_static = os.path.join(OUTPUT_DIR, "static")
    shutil.copytree(STATIC_DIR, out_static)
    print(f"  Copied static/ → _site/static/")

    # Copy verbatim files (ontology + data)
    for fname in VERBATIM_FILES:
        src = os.path.join(ROOT, fname)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(OUTPUT_DIR, fname))
            print(f"  Copied {fname} → _site/{fname}")
        else:
            print(f"  WARNING: {fname} not found, skipping.")

    # Markdown extensions
    md_extensions = ["tables", "fenced_code", "attr_list", "def_list"]

    # Build each markdown page (skip url-based nav items)
    for item in nav_items:
        if "url" in item:
            print(f"  Skipped nav item '{item['label']}' (static URL: {item['url']})")
            continue

        md_file = item["file"]
        md_path = os.path.join(CONTENT_DIR, md_file)

        if not os.path.exists(md_path):
            print(f"  WARNING: {md_path} not found, skipping.")
            continue

        with open(md_path, encoding="utf-8") as f:
            raw = f.read()

        meta, body = parse_frontmatter(raw)
        page_title = meta.get("title", item["label"])

        content_html = md_lib.markdown(body, extensions=md_extensions)
        content_html = content_html.replace("{{ stats_dashboard }}", stats_html)

        current_slug = slug_from_filename(md_file)
        nav_html = build_nav(nav_items, base_url, current_slug)

        page_html = render_page(
            template, content_html, page_title, nav_html, site_title, base_url
        )

        out_filename = html_filename(md_file)
        out_path = os.path.join(OUTPUT_DIR, out_filename)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_html)

        print(f"  Built {md_file} → _site/{out_filename}")

    print(f"\nDone. Site written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
