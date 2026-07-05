
# Overview

Dictionaries are stored in .sqlite files containing enough information to resolve dictionary definitions.
This was done so
- Massive dictionaries don't have to be distributed with the package
- Users are able to modify the dictionary, or create their own for a new language

# Tables

`info`
> Contains basic information about this dictionary

| Column          | Description                                                         | e.g.         |
|-----------------|:-------------------------------------------------------------------:|:-------------|
| name            | A name for the dictionary used for identifying in logs              | Custom       |
| language        | Language code for definitions in this dictionary (see LANGUAGES.md) | zh           |
| date            | Date used for identification                                        | 2026-03-24   |
| version         | Version used for identification                                     | 1.0.0        |
| format_version  | Version of the AutoAnki dictionary format specification             | 1.0.0        |

`fields`
> Defines the semantic meaning of each column in the definitions table.

| Column       | Description                             | e.g.                         |
|--------------|:---------------------------------------:|:-----------------------------|
| field_name   | Name of the colum in the definitions table             | pinyin        |
| role         | Standardized semantic role used by AutoAnki            | PRONUNCIATION |
| required     | Whether this field is required by the specification    | false         |
| display_name |  Human-readable name for displaying in UIs (optional)  | Pinyin        |

`roles`

| Role           | Description                                         |
|----------------|:----------------------------------------------------|
| HEADWORD       | Primary word or phrase being defined                |
| DEFINITION     | Definition, translation, or meaning                 |
| PRONUNCIATION  | Pronunication (e.g. Pinyin, IPA, Romaji)            |
| ALTERNATE      | Alternate spelling or writing system                |
| POS            | Part of speech                                      |
| FREQUENCY      | Frequency ranking or score                          |
| TAG            | Category or proficiency tag (e.g. HSK, JLPT)        |
| EXAMPLE        | Example sentence or phrase                          |
| FILTER         | Field intended for filtering during deck generation |


`definitions`
> Table containing the actual definitions

| Column      | Description                                      | e.g.                                |
|-------------|:------------------------------------------------:|:------------------------------------|
| id          | Unique identifier for the dictionary entry       | 12345                               |
| field_name  | One or more columns defined in the fields table. | pinyin, definition, frequency, etc. |
| ...         | Additional user-defined fields are permitted     | stroke_count, radicals, audio_url   |















