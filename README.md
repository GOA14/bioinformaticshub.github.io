# bioinformaticshub.github.io

The website of **Bioinformatics Hub**, the bioinformatics community for scientists and
researchers in Nigeria. A plain Jekyll site on GitHub Pages, with membership held in a
single YAML file that people add themselves to through GitHub.

Live site: <https://bioinformaticshub.github.io>

Everything here is community-maintained. You do not need permission to contribute, and
you do not need to be an experienced Git user -- see [CONTRIBUTING.md](CONTRIBUTING.md).

## Join the hub

1. Join the Slack workspace with your institutional email address: <https://bioinformaticshub.slack.com>
2. Add yourself to the members page by opening the
   [membership form](https://github.com/bioinformaticshub/bioinformaticshub.github.io/issues/new?template=membership.yml).
   A bot turns your answers into a pull request; once a maintainer merges it, your card
   is live on the [members page](https://bioinformaticshub.github.io/members/).

Prefer to do it by hand? Edit
[`_data/members.yml`](_data/members.yml) and open a pull request. Required fields are
`name`, `github`, `institution` and `interests`.

## How membership works

```
member opens issue form  ->  .github/workflows/membership.yml
                         ->  scripts/add_member.py   (parse, sanitise, upsert)
                         ->  scripts/validate_members.py
                         ->  branch membership/<login> + pull request
                         ->  maintainer merges -> Pages rebuilds -> card appears
```

- The `github:` field is taken from the account that opened the issue, so nobody can be
  added in someone else's name. Avatars come from `https://github.com/<login>.png`.
- Re-submitting or editing the issue **updates** your existing entry and refreshes the
  same pull request; entries are matched on GitHub username.
- Every field is sanitised and length-capped, URLs and ORCID iDs are format-checked, and
  anything unreadable is dropped rather than written to the file.
- To be removed, open an issue or delete your own block in a pull request. No reason needed.

## Brand

The logo is the outline of Nigeria carrying the community network, with Abuja as the hub
node. All variants -- colour, dark, one-colour, app tile, favicon, horizontal and stacked
lockups, and a 1280x640 social card -- are in
[`assets/brand/`](assets/brand/README.md) and are regenerated with
`python scripts/make_logo.py --png`. The site palette uses the flag green `#008751`.

## Repository layout

| Path | What it is |
| --- | --- |
| `_config.yml` | Site title, URLs, Slack link, plugins. |
| `_data/members.yml` | The members directory. One block per person. |
| `_data/institutions.yml` | Institutional email domains accepted by Slack, shown on `/join/`. |
| `_data/navigation.yml` | Top navigation bar. |
| `_layouts/`, `_includes/` | Page templates and the member/event card partials. |
| `assets/css/main.css` | All styling, hand-written, no Sass build step. |
| `_posts/`, `_events/` | Blog posts and events, one Markdown file each. |
| `scripts/` | Membership parser, data validator, and the logo generator. |
| `assets/brand/` | Logo kit (SVG + PNG) and the brand guide. |
| `.github/workflows/` | Pages deployment, membership bot, validation. |
| `.github/ISSUE_TEMPLATE/` | The membership and event forms. |

## Running it locally

```bash
git clone https://github.com/bioinformaticshub/bioinformaticshub.github.io.git
cd bioinformaticshub.github.io
bundle install
bundle exec jekyll serve --livereload     # http://127.0.0.1:4000
python scripts/validate_members.py        # check the members file
```

Testing the membership parser without GitHub:

```bash
ISSUE_BODY="$(cat test-issue.md)" ISSUE_AUTHOR=yourhandle python scripts/add_member.py
```

## Licence

Code MIT, content CC BY 4.0. See [LICENSE](LICENSE).
