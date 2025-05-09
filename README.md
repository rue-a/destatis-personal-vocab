# Destatis Fächersystematiken -- Come2Data Version

In diesem Repositorium werden die Come2Data Versionen der Destatis Fächersystematiken verwaltet. Dei Systematiken werden mit [SkoHub-Pages](https://github.com/skohub-io/skohub-pages) als interaktive Webseiten zur Erkundung unter https://rue-a.github.io/destatis-personal-vocab/ bereitgestellt.

## Systematik der Fächergruppen, Lehr- und Forschungsbereiche und Fachgebiete (`personal_23`)

Referenz: https://www.destatis.de/DE/Methoden/Klassifikationen/Bildung/personal-stellenstatistik

Die Fächersystematik hat 3 Hierarchielevel:
1) Fächergruppe (FG), 2-stellige Id
2) Lehr- und Forschungsbereiche (LuF), 3-stellige Id
3) Fachgebiet (FGB), 4-stellige Id

Eine maschinenlesbare Version der Fächersystematik wurde von Destatis auf Anfrage in Form von Excel Workbooks bereitgestellt.

### Erstellung des SKOS Dokuments `destatis_personal_skos.ttl`

Das SKOS Dokument wurde mithile der Python Scripts `tablest2skos.py`, `enrich_skos.py` und `get_mappings.py` erstellt. 

#### 1) Konvertierung der Originaldaten zu SKOS

Konvertiert die tabellarischen Daten in Graphdaten gemäß des SKOS Datenmodells.

Als __Eingangsdaten__ für `pers_tables2skos.py` wurden CSV-Versionen der Originaldaten (Excel Workbooks) verwendent, bei denen einige händische Änderung vorgenommen wurden:
1) Etwaige Header mit Metainformationen wurden entfernt
2) Die zweite Spalte jeder Datei wurde gelöscht (da etwas unklar ist was sie bedeutet oder leer ist)
3) die verbleibenden Spalten wurden umbenannt in `id`, `label` und `parent_id` (`parent_id` kommt nur bei LuF und FGB vor)

Als __Ausgangsdaten__ entsteht die Datei `destatis_personal_skos.ttl` (1). Die Datei wird in den Folgeschritten überschrieben.


## Systematik der Fächergruppen, Studienbereiche und Studienfächer (`studierende_23`)

Referenz: https://www.destatis.de/DE/Methoden/Klassifikationen/Bildung/studenten-pruefungsstatistik

Die Fächersystematik hat 3 Hierarchielevel:
1) Fächergruppe (FG), 2-stellige Id
2) Lehr- und Forschungsbereiche (LuF), 2-stellige Id
3) Fachgebiet (FGB), 3-stellige Id

Eine maschinenlesbare Version der Fächersystematik wurde von Destatis auf Anfrage in Form von Excel Workbooks bereitgestellt.

### Erstellung des Dokuments `destatis_studierende_skos.ttl`


#### Anreicherung

Eine SKOS-Version der *Systematik der Fächergruppen, Studienbereiche und Studienfächer* wird von der [DINI (Deutsche Initiative für Netzwerkinformation)](https://dini.de/) Arbeitsgruppe [KIM (Das Kompetenzzentrum Interoperable Metadaten)](https://dini.de/standards) unter https://github.com/dini-ag-kim/hochschulfaechersystematik gepflegt. Diese Version beinhaltet auch Übersetzungen der Konzeptlabels ins Englische und Ukrainische. Die Version wurde diesem Repositorium in der Version `v2025-02-03` als `hochschulfaechersystematik.ttl` hinzugefügt.