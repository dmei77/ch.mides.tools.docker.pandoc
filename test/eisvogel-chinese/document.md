---
title: "Multilingual Example"
author: [Author]
date: "2020-01-01"
subject: "Markdown"
keywords: [Markdown, Example]
lang: "de"
toc: true
toc-own-page: true
titlepage: true
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "360049"
titlepage-rule-height: 0
titlepage-background: "background.pdf"
colorlinks: true
mainfont: "Noto Sans"
header-includes:
  - \newfontfamily\hebrewfont[Script=Hebrew]{Noto Sans Hebrew}
  - \newfontfamily\cjkfont{Noto Sans CJK SC}
  - \newfontfamily\arabicfont[Script=Arabic]{Noto Sans Arabic}
pandoc-latex-environment:
  noteblock: [note]
  tipblock: [tip]
  warningblock: [warning]
  cautionblock: [caution]
  importantblock: [important]
...

# Deutsch
Dies ist ein deutsches Beispiel.

# Hebräisch

\hebrewfont  שלום עולם 

# Chinese Textexample

\cjkfont 这是一个中文测试，数字七：七。

# Arabisch:

\arabicfont السلام عليكم 
\fontspec{Noto Sans}

# Zusammenfassung

| Sprache      | Empfohlene Schriftart                      |
| ------------ | ------------------------------------------ |
| Chinesisch   | `Noto Sans CJK SC`                         |
| Hebräisch    | `Noto Sans Hebrew`                         |
| Multilingual | `Noto Sans` (wenn vollständig installiert) |


