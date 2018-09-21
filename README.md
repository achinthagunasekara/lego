# Lego Configuration Management Tool

![Lego Logo](images/logo.png "Lego Logo")

Lego configuration management tool.

## Builder Files Structure

```
.
├── brick_sets
│   └── php_web_server
│       └── bricks.yaml
└── server.yaml
```

### Builder File Format

*server.yaml*

```
---

brick_sets:
  - php_web_server
```

### Bricks File Format

*php_web_server/bricks.yml*

```
---

"Install Packages":
  type: package
  provider: apt
  state: present
  packages:
    - apache2
    - php5

"Create Sample PHP Page":
  type: file
  state: present
  owner: root
  group: root
  mode: 0755
  files:
    - source: index.php
      destination: /var/www/html/index.php

"Restart Apache Service":
  type: command
  commands:
    - /etc/init.d/apache2 restart
```

## Documentation

### Currently Supported Types

#### package

| Attribute  | Explanation |
| ------------- | ------------- |
| provider  | Package manager to use on the system. Currently only `apt` is supported |
| state  | `present` or `absent` |
| packages | List of packages to manage |

#### file

| Attribute  | Explanation |
| ------------- | ------------- |
| state  | `present` or `absent` |
| owner | Owner of the file |
| group | Owner group of the file |
| mode | Permission to set on the file. E.G 0755 |
| files | Yaml dictionary of `source` and `destination` of the files to be created. `owner`, `group`, and `mode` can be set on a existing file by skipping `source` |


### command

| Attribute  | Explanation |
| ------------- | ------------- |
| commands  | Yaml list of commands to run |

## [TODO]

* Test cases need to be written for modules using `pytest`.
* Perhaps make modules dropable to a directory...?
