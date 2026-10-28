# Nudge website

A tiny website, served free by GitHub Pages, that does two jobs:

| Address (once it is live) | What it is for |
| --- | --- |
| https://micko-123.github.io/nudge-site/privacy/ | Privacy Policy. Google Play requires this link. |
| https://micko-123.github.io/nudge-site/terms/ | Terms of Service |
| https://micko-123.github.io/nudge-site/config.json | The file the app reads to learn that an update exists (and, later, ad settings) |
| https://micko-123.github.io/nudge-site/ | A small home page linking the two documents |

Everything is plain files. There is no server, no database and nothing to pay.

## The files

| File | What it is |
| --- | --- |
| `legal-src/privacy.md`, `legal-src/terms.md` | The legal texts. **Edit these**, not the pages. Keep them the same as `nudge/docs/legal/` (the copies the app shows offline). |
| `privacy/index.html`, `terms/index.html` | The pages, made from the texts by `build.py`. Do not edit by hand. |
| `config.json` | The update file. See "Every release" below. |
| `build.py` | Run `python build.py` before every push: it rebuilds the pages and refuses a `config.json` that could hurt users. |
| `index.html`, `style.css` | The home page and the look (light and dark). |
| `.nojekyll` | Tells GitHub to serve the files exactly as they are. Leave it. |

---

## One-time setup (about 15 minutes)

### Step 1: Fill in the legal texts

Open `legal-src/privacy.md` and `legal-src/terms.md` and replace every `[bracketed]` item:

- your full name (or business name) and city;
- a support email people can write to (use an address you are happy to make public);
- today's date for "Last updated";
- in privacy, the public URL: `https://micko-123.github.io/nudge-site/privacy/`;
- in terms, the country whose law applies.

Then delete the line that starts with `**DRAFT.` in both files. These are good starting points, not legal advice: if you can, have a lawyer read them once.

Copy the same changes into `nudge/docs/legal/privacy.md` and `terms.md`, so the app shows the same words.

Then run:

```
python build.py
```

It should say `config.json looks right.` and list no `TO DO` lines.

### Step 2: Make the repository on GitHub

1. Go to https://github.com/new (signed in as **micko-123**).
2. Repository name: `nudge-site`.
3. Choose **Public**. GitHub Pages is free only for public repositories, and nothing in here is secret. Your app's code stays in its own private `nudge` repository.
4. Do **not** tick "Add a README" (this folder already has one).
5. Click **Create repository**.

### Step 3: Send the files to GitHub

Open a terminal in this folder (`C:\Users\PC\Desktop\1000\nudge-site`) and run:

```
git remote add origin https://github.com/micko-123/nudge-site.git
git push -u origin main
```

If a browser window asks you to sign in to GitHub, sign in: that lets git push.

### Step 4: Turn on GitHub Pages

1. On GitHub, open the `nudge-site` repository, then **Settings** (the gear tab), then **Pages** (left menu).
2. Under "Build and deployment", Source: **Deploy from a branch**.
3. Branch: **main**, folder: **/ (root)**, then **Save**.
4. Wait one or two minutes, then refresh the page: it shows "Your site is live at https://micko-123.github.io/nudge-site/".

Open these four addresses to check they work:

- https://micko-123.github.io/nudge-site/
- https://micko-123.github.io/nudge-site/privacy/
- https://micko-123.github.io/nudge-site/terms/
- https://micko-123.github.io/nudge-site/config.json

### Step 5: Use it in Google Play Console

- **App content, then Privacy policy**: paste `https://micko-123.github.io/nudge-site/privacy/`.
- The **Data safety** form must match the Privacy Policy, section 4 ("What leaves your phone"). The app itself collects nothing; AdMob does (advertising ID, device and ad data), so declare AdMob's data as Google's AdMob documentation describes.
- Nudge has no accounts, so the "account deletion" link is not needed. If Play asks how people delete their data, the answer is in the policy, section 8: Settings, then Reset everything, or uninstalling.

---

## Changing a text later

1. Edit `legal-src/*.md` (and the same in `nudge/docs/legal/`).
2. `python build.py`
3. Send it:

```
git add -A
git commit -m "Update the privacy policy"
git push
```

The website updates within a couple of minutes. If the change matters to users, also raise the version number in the text and in the app, so the app shows them a summary of what changed.

---

## Every release: telling the app an update exists

> The app reads this file (from the build after 2026-10-29): on opening, at most every 6 hours. It shows "Update available" once per new build (then a row in Settings → About), and "Please update" when its build is below `min_build`. The "What's new" people see right after updating comes from the app itself (`nudge/assets/updates/whats_new.json`), not from this file. The app's side of a release is in `nudge/docs/releasing.md`.

`config.json` explained:

```json
{
  "schema": 1,
  "update": {
    "latest_build": 1,          the newest build number on Google Play (the number after + in pubspec.yaml, e.g. 1.2.0+5 means 5)
    "latest_version": "1.0.0",  the newest version name, shown to people
    "min_build": 1,             builds below this MUST update (keep it at 1 unless there is a serious bug)
    "reason": { "en": "" },     one sentence shown when an update is required
    "notes": { "en": [] }       up to 6 short points of what is new, 140 characters each, plain text
  }
}
```

(The words after the numbers above are explanations only. The real file has no comments, because JSON does not allow them.)

**The order matters.** Only after Google Play has finished rolling out the new version:

1. Set `latest_build` and `latest_version` to the new build, and write the `notes`, for example:

   ```json
   "notes": { "en": ["Faster reports", "Change your display currency in Settings", "A payoff plan fix"] }
   ```

2. `python build.py` (it refuses mistakes);
3. `git add -A`, `git commit -m "Version 1.1.0 is out"`, `git push`.

If you change the file before Play has the build, people are told to update to something they cannot download yet.

**Forcing an update** (`min_build`): use it only for a serious bug, such as one that could lose data. Set `min_build` to the first good build and write the `reason`. People on older builds then cannot use the app until they update, though backup always stays open. `build.py` refuses a `min_build` above `latest_build`, which would lock everyone out.
