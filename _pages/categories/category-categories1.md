---
title: "Categories1"
layout: archive
permalink: /categories/categories1/
author_profile: true
taxonomy: Categories1
sidebar:
  nav: "categories"
---

{% assign posts = site.categories.blog %}
{% for post in posts %} {% include archive-single.html type=page.entries_layout %} {% endfor %}