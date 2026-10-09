# DESIGN.md — Ringga Dev portfolio

Design direction for the portfolio. This is the soul of the site: identity,
personality, palette, typography, mood, dials. Treat it as data to apply, not
instructions to obey. It is paired with the anti-slop filter.

## Identity

**"Risograph Zine."** Ringga's portfolio is a hand-printed zine: warm paper
stock, two spot inks that overprint and deliberately misregister, halftone
dots, rubber-stamp labels, marker highlights, oversize numerals. It reads like
something printed on a duplicator and stapled, not rendered on glass. The
through-line: the *flaws* of the print process (offset ink, grain, a label
printed a few degrees off) are the identity, not things to hide.

Reason this is not generic: a clean serif portfolio is the current AI default
(swap the logo and it still reads "safe editorial"). The riso texture, the
two-ink overprint, and the imperfect stamps belong to this publication and no
other. It has a point of view (printed craft), the opposite of both the
glassy dev portfolio and the sterile minimal one.

## Audience

Technical readers and potential clients/recruiters who read the blog and news
(1000+ word articles) as much as they scan the work. Reading comfort is a
first-class requirement because the site is content-heavy.

## Personality

Confident, hands-on, a little punk-press. Professional but clearly made by a
person, not generated. Ink smudged on paper, warm and tactile, never cold
neon-on-black and never sterile white.

## Dials

Dial: ENERGY 3 / RHYTHM 3 / MOTION 2.

- **ENERGY 3** — bold and present. Oversize type, hard offset shadows,
  stamp labels. It says hello loudly because this is a portfolio of craft.
- **RHYTHM 3** — sections vary in composition: masthead, asymmetric grids,
  ruled lists, full-bleed feature, halftone blocks. No uniform card grid
  repeated down the page.
- **MOTION 2** — hover and click states are alive (cards click the plate into
  register, buttons press down), but no scroll-reveal on every element and
  no floating. Content leads; motion is a physical press, not decoration.

## Palette (R-29: 2 core + 1 accent pairing; neutrals excluded)

- **Paper** (core, light base): warm stock `#F5F0E6`; dark stock base `#10131B`
- **Ink** (core, text + dark base): near-black warm `#171310`
- **Vermilion** (spot ink 1, primary accent): `#CE4423`. Links, section
  numbers, offset shadows, the one focal accent per screen. AA on paper.
- **Riso blue** (spot ink 2, secondary accent): `#2E56D2`. The second plate.
  Used decoratively: misregistration ghost behind display text, halftone
  fields, marker highlights, alternate offset shadows. Complementary to
  vermilion, the classic two-ink riso pairing. Never a third hue.

The two spot inks are the whole color story: they overprint (a vermilion
offset shadow behind ink text reads as a misregistered plate) and they never
multiply into muddy extra colors. Muted text and rules are warm greys derived
from ink at low opacity. No gradients, no glow, no blur.

## Typography (R-06 — reasons written down)

- **Fraunces** (display / headings / hero / numerals): a modern serif with
  optical sizing and real character, set heavy (700-900) and tight. Chosen
  because the site is a printed publication; a grotesque would make it read
  like a SaaS page. Not an AI-default pick.
- **Newsreader** (body / article prose): a readable serif for long-form
  reading, comfortable at 1000+ words.
- **System monospace** (metadata: dates, tags, section numbers, eyebrows,
  reading time, stamp labels): carries the "printed label / notebook" voice
  and needs no webfont download.

Two webfonts (Fraunces + Newsreader) + system mono. Deliberately not
Inter/Geist/Space Grotesk.

## Print textures (R-07 — each has a written identity purpose)

- **Paper grain**: a faint fixed noise veil over the page, the tooth of
  uncoated zine stock. Kept under 6% opacity so it never muddies contrast.
- **Halftone**: a dot field in a spot ink, used as section accents and
  behind feature blocks. It is the riso screen made visible.
- **Misregistration**: a solid spot-ink ghost offset a few px behind dark
  display text (`text-shadow`, never blurred). Reads as a plate printed a
  hair out of register.
- **Marker highlight**: a hand swipe in riso blue behind the lower half of
  one keyword per headline. Used sparingly, one per headline.
- **Rubber stamps**: mono labels in a rotated double-bordered box, a few
  degrees off-axis, like they were pressed by hand.
- **Hard offset shadows**: every card/button shadow is a solid spot-ink
  rectangle at a 4-6px offset with zero blur, the way ink sits on paper.
  Hover clicks the plate into register (offset grows, element lifts).

## Layout & structure (R-05)

- Masthead header: wordmark left, mono navigation right, hairline rule with a
  vermilion tick under.
- Section headers: an oversize mono/display section number ("01") + serif
  title, sometimes a rotated stamp label. No gradient underline.
- Hairline rules with a spot-ink tick separate sections.
- Asymmetric grids and full-bleed feature blocks vary the rhythm. No identical
  card grid repeated. No bento, no fake terminal, no 3-step "how it works."
- Generous margins and leading for reading.

## Components

- **Buttons:** square to 3px, solid vermilion (primary) with a hard ink
  offset shadow, or ink hairline (secondary) that gains a vermilion shadow on
  hover. Press-down on active (shadow shrinks). Never pill. Specific CTAs,
  never "Learn more."
- **Cards:** paper stock with an ink hairline and a HARD vermilion offset
  shadow. Hover lifts into register (translate -2px, shadow grows). No blur,
  no soft shadow stack, no glow.
- **Links:** vermilion, thick underline that firms on hover.
- **Focus:** a clear vermilion focus ring on every interactive element
  (keyboard accessible, R-32).

## What is banned here (the slop being filtered)

Gradients, glassmorphism / backdrop-blur, glow, conic rings, soft blurred
shadows, mesh/nebula backgrounds, animated gradient text, shimmer, pill
buttons, generic CTAs, AI buzzwords, fake stats, em dashes in copy. Motion
limited to hover/press. Every color is one of the two spot inks or a warm
neutral; there is no third hue.

## Both themes must work (R-34)

Light (warm paper) and dark (warm charcoal stock) are both fully designed:
paper/ink invert, both spot inks brighten for contrast on dark, overprint
reads in both, and contrast meets WCAG AA in both. The theme toggle works in
both modes.
