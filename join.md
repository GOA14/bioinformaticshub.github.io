---
layout: page
title: Join the hub
subtitle: Two things to do -- join the Slack workspace, and add yourself to the members page.
permalink: /join/
---

## 1. Join the Slack workspace

Day-to-day conversation happens on Slack. Sign up at
[{{ site.slack }}]({{ site.slack_invite }}) with an **institutional email address**
on one of the domains listed below.

Slack works in a browser, on the desktop and on your phone. Once you are in, join
whichever channels suit you &mdash; `#first-steps`, `#unix-bash`, `#r`, `#python`,
`#transcriptomics`, `#single-cell`, `#metagenomics`, `#workflow`, `#galaxy`,
`#quality-control`, `#introductions` and others. Say hello in `#introductions`,
add a profile picture, and please read the
[Code of Conduct]({{ '/code-of-conduct/' | relative_url }}).

> If your Nigerian university or research institute is not on the list, that is not a
> refusal. Open an issue or a pull request against `_data/institutions.yml` and we will
> add your domain.

## 2. Put yourself on the members page

Membership of the website is held in one plain-text file,
[`_data/members.yml`](https://github.com/{{ site.repository }}/blob/main/_data/members.yml).
Pick whichever route you prefer.

### Route A &mdash; the issue form (no Git knowledge needed)

1. Open the [membership form](https://github.com/{{ site.repository }}/issues/new?template=membership.yml) while signed in to GitHub.
2. Fill in your name, institution and interests. Everything else is optional.
3. Submit. A workflow reads your answers, writes an entry into `_data/members.yml` and opens a pull request for you.
4. A maintainer merges it, GitHub Pages rebuilds, and your card appears on the [members page]({{ '/members/' | relative_url }}).

Your GitHub username is taken from the account that opened the issue, so nobody can add
an entry in your name. Your profile photo is pulled straight from your GitHub account.

### Route B &mdash; edit the file yourself

1. Fork [{{ site.repository }}](https://github.com/{{ site.repository }}).
2. Add an entry to `_data/members.yml`:

```yaml
- name: Your Name
  github: your-github-username
  institution: Your University or Institute
  interests: RNA-Seq, metagenomics, R
  role: PhD student
  location: Kano, Nigeria
  website: https://example.org
  orcid: 0000-0002-1825-0097
```

3. Open a pull request. A check validates the file; once it is green a maintainer merges it.

### Updating or removing your entry

Run the issue form again with your new details &mdash; entries are matched on your GitHub
username, so the bot updates your existing card rather than adding a second one. To be
removed, open an issue or delete your own block in a pull request. No reason needed.

## Who is welcome?

Anyone interested in bioinformatics in Nigeria. You do not need to be a bioinformatician,
and you do not need to be working in Nigeria today. Next-generation sequencing, microarrays,
pathways and networks, structural biology, scientific programming, systems biology,
computational genomics &mdash; all of it counts. Biologists, biomedical and medical
scientists who are new to the field are especially welcome.

## Eligible institutional email domains

<ul class="domains">
{% for i in site.data.institutions %}
  <li><code>@{{ i.domain }}</code><br><span class="small">{{ i.name }}</span></li>
{% endfor %}
</ul>
