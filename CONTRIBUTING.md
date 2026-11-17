# Contributing

Everything on <https://bioinformaticshub.github.io> is community-maintained. You do not
need permission to contribute, and you do not need to be an experienced Git user.

## Add yourself to the members page

The easy way: open the
[membership form](https://github.com/bioinformaticshub/bioinformaticshub.github.io/issues/new?template=membership.yml).
A workflow reads your answers, writes an entry into `_data/members.yml` and opens a pull
request for you. Edit the issue later to update your details; the same pull request is
refreshed.

The manual way: fork the repository, add a block to `_data/members.yml`, open a pull
request. Required fields are `name`, `github`, `institution` and `interests`. Run
`python scripts/validate_members.py` first if you can.

## Write a blog post

Add `_posts/YYYY-MM-DD-short-title.md`:

```markdown
---
title: "Calling variants on a laptop"
date: 2026-04-02
author: Your Name
tags: [tutorial, variant-calling]
---

Your post, in Markdown.
```

## List an event

Add a file to `_events/`, using `_events/2026-01-example-relaunch-meetup.md` as a
template, and set `published: true`. Or use the
[event proposal form](https://github.com/bioinformaticshub/bioinformaticshub.github.io/issues/new?template=event.yml).

## Fix anything else

Every page has an "Improve this page" link in the footer that opens the GitHub editor on
that file. Typos, dead links, a missing institutional email domain in
`_data/institutions.yml` &mdash; send the pull request, no issue needed first.

## Run the site locally

```bash
git clone https://github.com/bioinformaticshub/bioinformaticshub.github.io.git
cd bioinformaticshub.github.io
bundle install
bundle exec jekyll serve --livereload   # http://127.0.0.1:4000
```

## Review standards

Pull requests are merged when the checks pass and the content follows the
[Code of Conduct](CODE_OF_CONDUCT.md). Maintainers aim to review within a week. If yours
is sitting there, say so on Slack.
