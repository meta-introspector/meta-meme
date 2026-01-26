#!/usr/bin/env python3
"""
Generate llm.txt dataset from trusted repos
Uses FOAF for people/orgs, includes solfunmeme
"""
import json
from pathlib import Path

TRUSTED_REPOS = {
    "meta-introspector/meta-meme": {
        "url": "https://github.com/meta-introspector/meta-meme",
        "description": "Formally verified AI-human creative framework",
        "foaf_person": "James Michael DuPont"
    },
    "jmikedupont2/Escaped-RDFa": {
        "url": "https://github.com/Escaped-RDFa/namespace",
        "description": "Cryptographically secure semantic web",
        "foaf_person": "James Michael DuPont"
    },
    "introspector/solfunmeme": {
        "url": "https://github.com/meta-introspector/SOLFUNMEME",
        "description": "Solana meme token framework",
        "foaf_person": "James Michael DuPont"
    }
}

def generate_foaf():
    """Generate FOAF profile"""
    return '''@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<#me> a foaf:Person ;
  foaf:name "James Michael DuPont" ;
  foaf:nick "jmikedupont2" ;
  foaf:homepage <https://github.com/jmikedupont2> ;
  foaf:account <https://github.com/meta-introspector> ;
  foaf:account <https://huggingface.co/introspector> ;
  foaf:workplaceHomepage <https://meta-meme.jmikedupont2.workers.dev> .
'''

def generate_llm_txt():
    """Generate llm.txt for all repos"""
    llm_txt = f"""# Meta-Meme Trust Network - LLM Context

## Overview
Trusted repositories for Meta-Meme RDF queries and semantic web applications.

## Repositories

"""
    for repo, info in TRUSTED_REPOS.items():
        llm_txt += f"""### {repo}
- URL: {info['url']}
- Description: {info['description']}
- Maintainer: {info['foaf_person']}

"""
    
    llm_txt += """## FOAF Profile
See foaf.ttl for machine-readable profile.

## RDF Sources
All repos available as RDF sources for distributed queries.
"""
    return llm_txt

print("📝 Generating llm.txt dataset...")
Path('llm.txt').write_text(generate_llm_txt())
Path('foaf.ttl').write_text(generate_foaf())
print("✅ Generated llm.txt and foaf.ttl")
