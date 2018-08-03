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

"Install Apache":
  type: package
  provider: apt
  state: present
  packages:
    - apache
    - php

"Create Sample PHP Page":
  type: file
  state: present
  files:
    - source: files/index.php
      destination: /var/www/html/index.php

"Restart Apache Service":
  type: service
  action: restart
  services:
    - apache2
```
