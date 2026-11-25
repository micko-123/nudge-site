# Nudge website

A tiny website, served free by GitHub Pages, that does two jobs:

| Address (once it is live) | What it is for |
| --- | --- |
| https://micko-123.github.io/nudge-site/privacy/ | Privacy Policy. Google Play requires this link. |
| https://micko-123.github.io/nudge-site/terms/ | Terms of Service |
| https://micko-123.github.io/nudge-site/config.json | The file the app reads to learn that an update exists, and its ad settings |
| https://micko-123.github.io/nudge-site/ | A small home page linking the two documents |

Everything is plain files. There is no server, no database and nothing to pay.

## The files

| File | What it is |
| --- | --- |
| `legal-src/privacy.md`, `legal-src/terms.md` | The legal texts. **Edit these**, not the pages. Keep them the same as `nudge/docs/legal/` (the copies the app shows offline). |
| `privacy/index.html`, `terms/index.html` | The pages, made from the texts by `build.py`. Do not edit by hand. |
| `config.json` | Update news and ad settings. See "Every release" and "Switching ads" below. |
| `build.py` | Run `python build.py` before every push: it rebuilds the pages and refuses a `config.json` that could hurt users. |
| `index.html`, `style.css` | The home page and the look (light and dark), in the app's Ocean colours. |
| `favicon.svg` | The app's logo, used as the tab icon and on the home page. A copy of `nudge/docs/brand/nudge_logo.svg`; replace it there first. |
| `og.png`, `apple-touch-icon.png` | The preview picture LinkedIn and other sites show for a shared link (from the app's feature graphic), and the icon a phone uses when the site is added to its home screen. |
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

## Switching ads: the "ads" section

> The app reads this from build 2 on, with the update check: on opening, at most every 6 hours. A change reaches most phones within a day, with no app update. Offline, a phone keeps the last file it got.

Each kind of build has its own part: `prod` is the app on Google Play, `closed` is the closed test, `dev` is the developer's own build. A build with no part of its own uses the app's built-in settings.

```json
"ads": {
  "closed": { "enabled": true },
  "prod": {
    "enabled": true,              false switches every ad off (see below)
    "off": ["homeNative"],        placements to switch off one by one (names below)
    "max_per_session": 6,         banners and native ads per session, 0 to 6
    "quiet_days": 3,              days after setting up with no Home ad and no full-screen ad, 3 to 60
    "full_screen_gap_hours": 24,  hours between full-screen ads, 24 to 720
    "history_first": 6,           rows before the first ad in Activity, 6 to 200
    "history_every": 15           rows between ads in Activity, 15 to 200
  }
}
```

(Again, the words after the values are explanations only.) Leave out anything you do not want to change.

**Every setting can only make ads calmer** than the app's built-in rules. A value outside its range is refused by `build.py`, and ignored by the app if one slips through.

**`"enabled": false`** stops ads completely for that build: no ads, and no consent form. While ads are off, colour themes, PDF reports and the advanced insights become free, so nobody loses anything. The streak freeze, streak repair, double XP and ad-free mode wait until ads are back. Setting it to `true` again starts ads on phones without a restart.

**Placement names** for `off`:

| Name | Where |
| --- | --- |
| `historyNative` | Between rows in Activity |
| `homeNative` | Bottom of Home |
| `investNative` | Bottom of Invest |
| `reportsNative` | Bottom of Reports |
| `insightsNative` | Bottom of Insights |
| `achievementsBanner`, `progressBanner`, `standBanner`, `yearBanner` | Achievements, Progress, Where you stand, Investment year summary |
| `calculatorsBanner` | Calculators list, every calculator, Saved calculations |
| `breakInterstitial`, `calculatorInterstitial` | The day's one full-screen ad |
| `rewardedAdFree`, `rewardedStreakFreeze`, `rewardedTheme`, `rewardedStreakRepair`, `rewardedQuestXp`, `rewardedReportPdf`, `rewardedCalculatorPdf`, `rewardedInsights` | A "Watch ad" offer; off hides that offer |

**When to use it:** AdMob warns about a placement (switch that one off until it is fixed); reviews complain about an ad (switch it off or lower `max_per_session`); anything goes wrong with ads (`"enabled": false`).

Then, as always: `python build.py`, `git add -A`, `git commit -m "Ads: ..."`, `git push`.
