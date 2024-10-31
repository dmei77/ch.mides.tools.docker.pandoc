---
title: "Crossref example"
author: [Author]
date: "2024-10-31"
subject: "Markdown"
keywords: [Markdown, Example]
lang: "en"
toc: true
toc-own-page: true
titlepage: true,
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "360049"
titlepage-rule-height: 0
titlepage-background: "background.pdf"
colorlinks: true
tblPrefix: 
- "Table"
- "Tabellen"
header-includes:
- |
  ```{=latex}
  \usepackage{awesomebox}
  ```
pandoc-latex-environment:
  noteblock: [note]
  tipblock: [tip]
  warningblock: [warning]
  cautionblock: [caution]
  importantblock: [important]
...

# pandoc-crossref test

## Section with table

a   b
--- ---
1   2
3   4

: Caption {#tbl:label1}


a   c
--- ---
1   3
3   3

: Caption 2 {#tbl:label2}


\newpage

## Section with text

See table @tbl:label1. or [Tabelchen @tbl:label1] [@tbl:label1; @tbl:label2]