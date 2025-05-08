import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal, XSD
from rdflib.namespace import RDF, SKOS, DCTERMS

# Basis-URL
BASE_URL = "https://www.destatis.de/DE/Methoden/Klassifikationen/Bildung/personal-stellenstatistik"
# BASE_URL = "http://test.org"

# CSV-Dateien laden
fg_df = pd.read_csv("personal_23/fg.csv", dtype=str)
fg_df["id"] = fg_df["id"].str.zfill(2)
luf_df = pd.read_csv("personal_23/luf.csv", dtype=str)
luf_df["id"] = luf_df["id"].str.zfill(3)
luf_df["parent_id"] = luf_df["parent_id"].str.zfill(2)
fgb_df = pd.read_csv("personal_23/fgb.csv", dtype=str)
fgb_df["id"] = fgb_df["id"].str.zfill(4)
fgb_df["parent_id"] = fgb_df["parent_id"].str.zfill(3)


# RDF Graph vorbereiten
g = Graph()
DESTATIS = Namespace(BASE_URL + "/")
g.bind("skos", SKOS)
g.bind("dcterms", DCTERMS)
g.bind("destatis", DESTATIS)


# ConceptScheme erzeugen
g.add((DESTATIS.scheme, RDF.type, SKOS.ConceptScheme))
g.add(
    (
        DESTATIS.scheme,
        DCTERMS.title,
        Literal(
            "Systematik der Fächergruppen, Lehr- und Forschungsbereiche und Fachgebiete",
            lang="de",
        ),
    )
)
g.add((DESTATIS.scheme, DCTERMS.creator, Literal("Statistisches Bundesamt", lang="de")))
g.add((DESTATIS.scheme, DCTERMS.created, Literal("2024-01-11", datatype=XSD.date)))
g.add((DESTATIS.scheme, DCTERMS.license, Literal("Unbekannt", lang="de")))

# Fächergruppen (FG)
for _, row in fg_df.iterrows():
    fg_id = row["id"]
    fg_label = row["label"]
    fg_uri = URIRef(f"{DESTATIS}{fg_id}")

    g.add((fg_uri, RDF.type, SKOS.Concept))
    g.add((fg_uri, SKOS.prefLabel, Literal(fg_label, lang="de")))
    g.add((fg_uri, SKOS.notation, Literal(fg_id)))
    g.add((fg_uri, SKOS.topConceptOf, DESTATIS.scheme))
    g.add((DESTATIS.scheme, SKOS.hasTopConcept, fg_uri))
    g.add((fg_uri, SKOS.inScheme, DESTATIS.scheme))


# Lehr- und Forschungsbereiche (LuF)
for _, row in luf_df.iterrows():
    luf_id = row["id"]
    luf_label = row["label"]
    fg_id = row["parent_id"]
    luf_uri = URIRef(f"{DESTATIS}{fg_id}.{luf_id}")
    fg_uri = URIRef(f"{DESTATIS}{fg_id}")

    g.add((luf_uri, RDF.type, SKOS.Concept))
    g.add((luf_uri, SKOS.prefLabel, Literal(luf_label, lang="de")))
    g.add((luf_uri, SKOS.notation, Literal(f"{luf_id}")))
    g.add((luf_uri, SKOS.broader, fg_uri))
    g.add((fg_uri, SKOS.narrower, luf_uri))
    g.add((luf_uri, SKOS.inScheme, DESTATIS.scheme))


# Fachgebiete (FGB)
for _, row in fgb_df.iterrows():
    fgb_id = row["id"]
    fgb_label = row["label"]
    luf_id = row["parent_id"]
    fg_id = luf_df.query(f"id == '{luf_id}'")["parent_id"].values[0]

    fgb_uri = URIRef(f"{DESTATIS}{fg_id}.{luf_id}.{fgb_id}")
    luf_uri = URIRef(f"{DESTATIS}{fg_id}.{luf_id}")

    g.add((fgb_uri, RDF.type, SKOS.Concept))
    g.add((fgb_uri, SKOS.prefLabel, Literal(fgb_label, lang="de")))
    g.add((fgb_uri, SKOS.notation, Literal(f"{fgb_id}")))
    g.add((fgb_uri, SKOS.broader, luf_uri))
    g.add((luf_uri, SKOS.narrower, fgb_uri))
    g.add((fgb_uri, SKOS.inScheme, DESTATIS.scheme))


# Als Turtle speichern
g.serialize("destatis_personal_skos.ttl", format="turtle")
print("SKOS-Hierarchie wurde erfolgreich erstellt.")
