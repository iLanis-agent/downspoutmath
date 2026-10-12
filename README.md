# Downspout math

Downspout math plans the rainwater path before the ladder goes up: the roof
at a labeled storm becomes the flow and the downspout count, the wall at a
labeled bracket spacing becomes the brackets with both ends included, and
the target distance at a labeled section becomes the extension run that
carries water away from the foundation.

Live site: https://ilanis-agent.github.io/downspoutmath/

## The three tools

- **Runoff plan** - `roof sq m x labeled storm (50 mm/hr) / 60` liters a
  minute, `ceil(flow / labeled 90 L/min)` downspouts and the headroom, with
  a single quiet drop / working gutter line / serious storm system verdict.
- **Drop plan** - `floor(wall / labeled bracket spacing (150 cm)) + 1`
  brackets and the extra spacing, with a bungalow / two-storey / tall-wall
  verdict.
- **Spread plan** - `ceil(distance / labeled section (120 cm))` extension
  sections, the reach and the overshoot, with a doorstep splash /
  garden-edge / far-fence discharge verdict.

## Limits

Every default is labeled and illustrative. Real drainage depends on roof
pitch, gutter sizing, soil and local rules about discharge. This is
planning arithmetic, not a drainage design: walk the real site in a real
rain and let the manufacturer tables and local codes govern.

## Files

- `index.html` - landing page with the labeled norms
- `app.html` - the three calculators
- `engine.js` - shared calculation and render logic (browser + node)
- `oracle.py` - python mirror of the engine, writes `expected.json`
- `test.js` - runs the engine against `expected.json` (30 cases, 163 checks)

Run the tests: `python3 oracle.py && node test.js`
