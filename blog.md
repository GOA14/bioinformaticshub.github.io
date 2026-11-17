---
layout: page
title: Blog
subtitle: Notes, write-ups and announcements from the community.
permalink: /blog/
---

Anyone in the hub can post. Add a Markdown file to `_posts/` named
`YYYY-MM-DD-your-title.md` and open a pull request &mdash; tutorials, meeting
write-ups, tool reviews and opportunity round-ups are all welcome.

{% if site.posts.size > 0 %}
<ul class="post-list">
  {% for post in site.posts %}
    <li>
      <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
      <p class="meta">{{ post.date | date: "%-d %B %Y" }}{% if post.author %} &middot; {{ post.author }}{% endif %}</p>
      <p>{{ post.excerpt | strip_html | truncate: 220 }}</p>
    </li>
  {% endfor %}
</ul>
{% else %}
No posts yet.
{% endif %}
