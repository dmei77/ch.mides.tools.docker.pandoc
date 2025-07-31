---
title: "Boxes with pandoc-latex-environment and awesomebox"
author: [Author]
date: "2020-01-01"
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
mainfont: Noto Sans CJK SC
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

# Chinese Textexample

这是一个中文测试，数字七：七。

