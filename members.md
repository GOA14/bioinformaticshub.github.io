---
layout: page
title: Members
subtitle: People building the bioinformatics community in Nigeria. Add yourself through GitHub.
permalink: /members/
---

Everyone listed here added themselves by opening a
[membership issue](https://github.com/{{ site.repository }}/issues/new?template=membership.yml)
or by sending a pull request against `_data/members.yml`.
See [Join]({{ '/join/' | relative_url }}) for the two-minute version.

<div class="member-tools">
  <input type="search" id="member-search" placeholder="Filter by name, institution or interest&hellip;" aria-label="Filter members">
  <span class="small"><span id="member-count">{{ site.data.members | size }}</span> shown</span>
</div>

{% assign steering = site.data.members | where: "team", "steering" | sort: "name" %}
{% assign everyone = site.data.members | sort: "name" %}

{% if steering.size > 0 %}
## Steering committee

<ul class="member-grid">
  {% for m in steering %}{% include member-card.html member=m %}{% endfor %}
</ul>
{% endif %}

## All members

<ul class="member-grid" id="all-members">
  {% for m in everyone %}{% include member-card.html member=m %}{% endfor %}
</ul>

<script>
(function () {
  var box = document.getElementById('member-search');
  var cards = Array.prototype.slice.call(document.querySelectorAll('#all-members .member-card'));
  var counter = document.getElementById('member-count');
  if (!box) return;
  box.addEventListener('input', function () {
    var q = box.value.trim().toLowerCase();
    var shown = 0;
    cards.forEach(function (c) {
      var hay = c.dataset.name + ' ' + c.dataset.institution + ' ' + c.dataset.interests;
      var hit = q === '' || hay.indexOf(q) !== -1;
      c.style.display = hit ? '' : 'none';
      if (hit) shown++;
    });
    counter.textContent = shown;
  });
})();
</script>
