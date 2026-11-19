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

{% assign established = "MSc holder,PhD student,PhD holder,Postdoctoral researcher,Faculty / Principal investigator,Research scientist (institute or industry)" | split: "," %}
{% assign steering  = site.data.members | where: "team", "steering" | sort: "name" %}
{% assign rest      = site.data.members | where_exp: "m", "m.team != 'steering'" | sort: "name" %}
{% assign scientists = rest | where_exp: "m", "established contains m.stage" %}
{% assign early      = "Undergraduate student,MSc student,Other" | split: "," %}
{% assign earlier    = rest | where_exp: "m", "early contains m.stage" %}
{% assign unstated   = rest | where_exp: "m", "m.stage == nil" %}

{% if steering.size > 0 %}
## Steering committee

<ul class="member-grid">
  {% for m in steering %}{% include member-card.html member=m %}{% endfor %}
</ul>
{% endif %}

{% if scientists.size > 0 %}
## Researchers

<ul class="member-grid">
  {% for m in scientists %}{% include member-card.html member=m %}{% endfor %}
</ul>
{% endif %}

{% if earlier.size > 0 %}
## Students and early career

Undergraduates, MSc students and anyone starting out. If that is you, you are in the right
place &mdash; ask in `#first-steps` on Slack.

<ul class="member-grid">
  {% for m in earlier %}{% include member-card.html member=m %}{% endfor %}
</ul>
{% endif %}

{% if unstated.size > 0 %}
## Members

Entries added before the career-stage field existed. Re-submit the membership form to move
your card into the right group.

<ul class="member-grid">
  {% for m in unstated %}{% include member-card.html member=m %}{% endfor %}
</ul>
{% endif %}

<script>
(function () {
  var box = document.getElementById('member-search');
  var cards = Array.prototype.slice.call(document.querySelectorAll('.member-card'));
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
