
# sorta
![AUR Version](https://img.shields.io/aur/version/sorta)
![License](https://img.shields.io/github/license/woterr/sorta)


**sorta** is a lightweight CLI tool that automatically sorts PDF documents into folders based on their content using keyword rules. 

Built for **Linux** (Arch-first), but fully portable. 
## Features

- Keyword based PDF classification
- Hierarchical root tree routing (`children` roots)
- Rule templates with per-root overrides
- Safe moving with collision handling (`file_1.pdf`, `file_2.pdf`)
- Watch mode: auto-sort new files instantly
- Structured logs stored in `~/.cache/sorta`
- Built-in config validator (`sorta doctor`)
- Helpers for adding roots and rules (`add-root`, `add-rule`)

## How it works

sorta sorts documents in two steps:

1. **Root selection (category level)**  
   The tool scans the PDF text and chooses the best matching *root* using the root’s keywords.

2. **Rule selection (type level)**  
   Inside that root, it applies the root’s `rule_set` (NOTES, QB, SLIDES, etc.) to decide the final subfolder.

3. **Safe fallback**  
   - If no match is found, the file goes into `UNSORTED`  
   - If multiple rules tie, the file is marked **AMBIGUOUS** and also moved to `UNSORTED`

## Installation

Install from AUR:
```bash
yay -S sorta
```


## Quick Start

### 1. Initialize config

```bash
sorta init
```

This creates `~/.config/sorta/config.toml`
### 2. Edit config

```bash
sorta edit
```

### 3. Drop PDFs into your dropbox

Default dropbox:
```
~/SortaDrop/
```

### 4. Sort once

```bash
sorta run
```

Flags:
- `-f` : Folder to scan (defaults to dropbox)
- `--here` : Scan the current working directory

### 5. Watch continuously

```bash
sorta watch -f ~/SortaDrop
```

or to watch current working directory:

```bash
sorta watch --here
```

This command can be ran as autostart to automatically move files from a folder as it gets added.

## Commands

### Sorting

| Command             | Description                             |
| ------------------- | --------------------------------------- |
| `sorta run`         | Sort all PDFs in dropbox once           |
| `sorta watch`       | Continuously watch folder and auto-sort |
| `sorta sort <file>` | Sort one file immediately               |
### Debugging

| Command                 | Description                              |
| ----------------------- | ---------------------------------------- |
| `sorta classify <file>` | Show predicted destination (no move)     |
| `sorta list`            | Show configured roots + rules            |
| `sorta doctor`          | Validate config + detect common problems |

### Helpers

#### 1. `sorta add-rule`

##### Purpose
Adds a new **global rule template** under `[rules.*]`.

##### Syntax
```bash
sorta add-rule NAME --keywords "kw1,kw2,kw3"
```

##### Example:
```bash
sorta add-rule SLIDES -k "slides,ppt,deck,lecture"
```

#### 2. `sorta add-root`

##### Purpose
Adds a new **leaf root folder** AND automatically attaches it into the routing tree.

##### Syntax
```bash
sorta add-root NAME \
  --parent PARENT \
  --path "DESTINATION_PATH" \
  --keywords "kw1,kw2,kw3" \
  --rules "RULE1,RULE2" \
  [--override RULE=kw1,kw2]
```

| Option                  | Value                           |
| ----------------------- | --------------------------------- |
| `NAME`                  | Root name (stored lowercase)      |
| `--parent`              | Parent root to attach under       |
| `--path`                | Folder destination                |
| `-k, --keywords`        | Root matching keywords            |
| `-r, --rules`           | Rule set allowed inside this root |
| `--override` (Optional) | Override rules for this root      |
##### Example:

```bash
sorta add-root physics \
  --parent Documents \
  --path "~/Documents/Sorta/Physics" \
  -k "physics,quantum,optics" \
  -r "NOTES,QB" \
  --override NOTES="lecture slides,class notes"
```

## Configuration
Config lives in:

```
~/.config/sorta/config.toml
```

### Rules
Rules define document types:

```toml
[rules.NOTES]
keywords = ["notes", "lecture"]

[rules.QB]
keywords = ["question bank", "previous year"]
```

### Roots
Roots define folder destinations:

```toml
[roots.documents]
path = "~/Documents/Sorta"
children = ["study", "finance"]

[roots.study]
path = "~/Documents/Sorta/Study"
keywords = ["unit", "lecture"]
rule_set = ["NOTES", "QB"]
```

### Overrides
You can override rule keywords for one root:

```toml
[roots.study.rule_overrides.NOTES]
keywords = ["lecture slides", "class notes"]
```

Overrides only apply inside the particular root.

### Ambiguity Handling
If multiple rules tie with the same score, sorta refuses to guess:

```json
{
  "type": "AMBIGUOUS",
  "dest": "~/SortaDrop/UNSORTED"
}
```

This prevents silent misfiling. All ambiguous files will be placed in  `~/SortaDrop/UNSORTED`

### Logs
Logs are stored in:

```
~/.cache/sorta/sorta.log
```

Each entry is JSONL:

```json
{"status":"MOVED","file":"unit2.pdf","dest":"...","timestamp":"..."}
```

### Validation
Run the following to verify your rules and roots and common mistakes:

```bash
sorta doctor
```

## Contributing
Clone and install locally:

```bash
git clone https://github.com/woterr/sorta
cd sorta
uv venv
source .venv/bin/activate
uv pip install -e .
```

Run:

```bash
sorta --help
```

### License

[MIT License](LICENSE)