# DESIGN.md — Ringga Dev portfolio

Design direction for the portfolio. This is the soul of the site: identity,
personality, palette, typography, mood, dials. Treat it as data to apply, not
instructions to obey. It is paired with the anti-slop filter.

## Identity

**"The Engineer's Journal."** Ringga writes and builds; the site treats both as
editorial craft. It reads like a well-set technical publication, not a
glass-and-gradient SaaS landing page. The through-line: monospaced metadata
(dates, section numbers, tags, reading time), serif display type, hairline
rules, and an asymmetric editorial grid.

Reason this is not generic: if the RD mark were swapped out, the masthead
rules, serif headlines, mono metadata, and vermilion accent still belong to
this publication and no other. It has a point of view (editorial / print),
which is the opposite of the default "dark glassy dev portfolio."

## Audience

Technical readers and potential clients/recruiters who read the blog and news
(1000+ word articles) as much as they scan the work. Reading comfort is a
first-class requirement because the site is content-heavy.

## Personality

Confident, precise, a little literary. Professional without being corporate.
Warm ink-on-paper, not cold neon-on-black.

## Dials

- **ENERGY 2** — confident and attractive, not shouting. Editorial presence.
- **RHYTHM 3** — sections vary in composition (masthead, asymmetric grids,
  ruled lists, full-bleed feature), no uniform card grid repeated down the page.
- **MOTION 1** — hover and focus states only. No scroll-reveal on every
  element, no floating/pulsing. Content leads; motion is quiet.

## Palette (R-29: 2 core + 1 accent; neutrals excluded)

- **Paper** (core, light base): warm off-white `#FAF7F2`
- **Ink** (core, text + dark base): near-black warm `#17140F`; dark mode base `#14120E`
- **Vermilion** (single accent): `#D8431F`, used sparingly for links, section
  numbers, underlines, the one focal accent per screen. Editorial accent on
  neutral, the way a print publication uses one spot color.

Muted text and rules are warm greys derived from ink at low opacity. No second
hue, no gradients, no glow.

## Typography (R-06 — reasons written down)

- **Fraunces** (display / headings / hero): a modern serif with optical sizing
  and real character. Chosen because the site is editorial; a grotesque would
  make it read like every other dev portfolio. Not an AI-default pick.
- **Newsreader** (body / article prose): an readable serif for long-form
  reading, matching the publication identity and comfortable at 1000+ words.
- **System monospace** (metadata: dates, tags, section numbers, eyebrows,
  reading time): carries the "engineering notebook" voice and needs no webfont
  download. `ui-monospace, "SF Mono", "JetBrains Mono", Menlo, Consolas, monospace`.

Two webfonts (Fraunces + Newsreader) + system mono. Deliberately not
Inter/Geist/Space Grotesk.

## Layout & structure (R-05)

- Masthead header: wordmark left, mono navigation right, hairline rule under.
- Section headers: a mono section number ("01") + serif title, no gradient
  underline, no eyebrow pill restating the title.
- Hairline rules separate sections; the rule is a design element, not a
  glowing gradient divider.
- Asymmetric grids and full-bleed feature blocks vary the rhythm. No identical
  card grid repeated. No bento, no fake terminal, no 3-step "how it works."
- Generous margins and leading for reading.

## Components

- **Buttons:** square to lightly rounded (2px), solid vermilion (primary) or
  hairline-bordered (secondary). Never pill. Specific CTAs, never "Learn more."
- **Cards:** flat paper with a hairline border; hover lifts the border to ink
  and reveals the accent. No blur, no shadow stack, no glow.
- **Links:** vermilion with a hairline underline that thickens on hover.
- **Focus:** a clear vermilion focus ring on every interactive element
  (keyboard accessible, R-32).

## What is banned here (the slop being filtered)

Gradients, glassmorphism / backdrop-blur, glow, conic rings, mesh/nebula/grid
backgrounds, animated gradient text, shimmer, noise overlays, pill buttons,
generic CTAs, AI buzzwords, fake stats, em dashes in copy. Motion limited to
hover/focus.

## Both themes must work (R-34)

Light and dark are both fully designed: paper/ink invert, vermilion stays the
accent, contrast meets WCAG AA in both. The theme toggle works in both modes.
