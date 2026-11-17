# bioinformaticshub.github.io

The website of **Bioinformatics Hub**, the bioinformatics community for scientists and
researchers in Nigeria. A plain Jekyll site on GitHub Pages, with membership held in a
single YAML file that people add themselves to through GitHub.

Live site: <https://bioinformaticshub.github.io>

---

## One-time setup

1. **Create the organisation.** On GitHub: *+ &rarr; New organization &rarr; Free*, named
   `bioinformaticshub`. Add co-maintainers as owners so the hub does not depend on one
   account.
2. **Create the repository** `bioinformaticshub.github.io` inside that organisation,
   public, with no README (the files here replace it).
3. **Push this site:**

   ```bash
   cd bioinformaticshub.github.io
   git init -b main
   git add .
   git commit -m "Bioinformatics Hub website"
   git remote add origin https://github.com/bioinformaticshub/bioinformaticshub.github.io.git
   git push -u origin main
   ```

4. **Turn on Pages.** *Settings &rarr; Pages &rarr; Build and deployment &rarr; Source:
   **GitHub Actions***. The `Deploy to GitHub Pages` workflow does the rest; the site is
   live a minute or two after the first push.
5. **Let Actions open pull requests.** *Settings &rarr; Actions &rarr; General &rarr;
   Workflow permissions*: select **Read and write permissions** and tick **Allow GitHub
   Actions to create and approve pull requests**. Without this the membership bot cannot
   open its pull request.
6. **Create two labels** (*Issues &rarr; Labels*): `membership` and `event`. The issue
   forms apply them.
7. **Replace the Slack link.** `slack_invite:` in `_config.yml` currently points at the
   workspace URL. Generate a real invite link in Slack
   (*Admin &rarr; Manage members &rarr; Invite people*, or an email-domain-based join link)
   and paste it there.
8. **Check your own entry** in `_data/members.yml` &mdash; the institution field was filled
   in from your old README and may need correcting &mdash; and check the expanded
   institution names in `_data/institutions.yml`.

### Keeping the old repository

`babasaraki/bioinformaticshub` has the project history and its stars. Either keep it as
the archive and add a line to its README pointing at the new site, or transfer it into the
organisation (*Settings &rarr; Transfer ownership*) and rename it, so the stars and issues
follow. The site itself must live in a repository named exactly
`bioinformaticshub.github.io` for the root URL to work.

### Custom domain (optional)

Add a file named `CNAME` containing e.g. `bioinformaticshub.org`, point a `CNAME` DNS
record at `bioinformaticshub.github.io`, then set the domain under *Settings &rarr; Pages*
and tick *Enforce HTTPS*.

---

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
- Re-submitting or editing the issue **updates** the existing entry and refreshes the same
  pull request; entries are matched on GitHub username.
- Every field is sanitised and length-capped, URLs and ORCID iDs are format-checked, and
  anything unreadable is dropped rather than written to the file.
- To merge membership pull requests automatically, create a repository **variable**
  `AUTO_MERGE_MEMBERSHIP` = `true` (*Settings &rarr; Secrets and variables &rarr; Actions
  &rarr; Variables*) and enable auto-merge for the repository. Leave it unset to keep a
  human in the loop, which is the safer default while the hub is small.
- Pull requests opened by the bot do not trigger the `Validate` workflow (a GitHub
  restriction on `GITHUB_TOKEN`); the same two checks already run inside the membership
  workflow before the branch is pushed.

---

## Brand

The logo is the outline of Nigeria carrying the community network, with Abuja as the hub
node. All variants -- colour, dark, one-colour, app tile, favicon, horizontal and stacked
lockups, and a 1280x640 social card -- are in
[`assets/brand/`](assets/brand/README.md) and are regenerated with
`python scripts/make_logo.py --png`. The site header, favicons and link-preview image are
already wired to them, and the site palette uses the flag green `#008751`.

## Repository layout

| Path | What it is |
| --- | --- |
| `_config.yml` | Site title, URLs, Slack link, plugins. Edit this first. |
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
