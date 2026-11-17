---
layout: page
title: Events
subtitle: Meetups, journal clubs and training sessions run by and for the community.
permalink: /events/
---

{% assign today = 'now' | date: "%Y-%m-%d" %}
{% assign upcoming = site.events | where_exp: "e", "e.date >= today" | sort: "date" %}
{% assign past = site.events | where_exp: "e", "e.date < today" | sort: "date" | reverse %}

## Upcoming

{% if upcoming.size > 0 %}
<ul class="event-list">
  {% for e in upcoming %}{% include event-card.html event=e %}{% endfor %}
</ul>
{% else %}
Nothing scheduled yet.
{% endif %}

Want to host a meetup, a hands-on workshop or a journal club? Add a file to the
`_events` folder and open a pull request, or
[open an issue](https://github.com/{{ site.repository }}/issues/new) describing what you
have in mind. An event page needs only a title, a date, a location and a paragraph.

## Past events

{% if past.size > 0 %}
<ul class="event-list">
  {% for e in past %}{% include event-card.html event=e %}{% endfor %}
</ul>
{% else %}
None recorded yet.
{% endif %}
