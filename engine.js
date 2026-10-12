(function (root) {
  "use strict";
  function plural(n, word, form) { return n + " " + (n === 1 ? word : (form || word + "s")); }
  function round1(x) { return Math.round(x * 10) / 10; }

  function runoffPlan(roofSqM, stormMmHr, perSpoutLMin) {
    if (!(roofSqM > 0) || !(stormMmHr > 0) || !(perSpoutLMin > 0)) return { error: "the roof, the storm and the labeled capacity must be positive" };
    var flow = round1(roofSqM * stormMmHr / 60);
    var spouts = Math.ceil(flow / perSpoutLMin);
    var headroom = round1(spouts * perSpoutLMin - flow);
    var verdict;
    if (spouts === 1) verdict = "a single quiet drop";
    else if (spouts <= 3) verdict = "a working gutter line";
    else verdict = "a serious storm system";
    return { flow: flow, spouts: spouts, headroom: headroom, verdict: verdict };
  }

  function dropPlan(wallCm, bracketCm) {
    if (!(wallCm > 0) || !(bracketCm > 0)) return { error: "the wall and the labeled bracket spacing must be positive" };
    if (wallCm < bracketCm) return { error: "the wall is shorter than one labeled bracket spacing" };
    var brackets = Math.floor(wallCm / bracketCm) + 1;
    var spare = round1(wallCm - (brackets - 1) * bracketCm);
    var verdict;
    if (wallCm < 300) verdict = "a bungalow drop";
    else if (wallCm <= 600) verdict = "a two-storey drop";
    else verdict = "a tall-wall drop";
    return { brackets: brackets, spare: spare, verdict: verdict };
  }

  function spreadPlan(distanceCm, sectionCm) {
    if (!(distanceCm > 0) || !(sectionCm > 0)) return { error: "the target distance and the labeled section must be positive" };
    var sections = Math.ceil(distanceCm / sectionCm);
    var reach = round1(sections * sectionCm);
    var overshoot = round1(reach - distanceCm);
    var verdict;
    if (distanceCm <= 120) verdict = "a doorstep splash";
    else if (distanceCm <= 300) verdict = "a garden-edge discharge";
    else verdict = "a far-fence discharge";
    return { sections: sections, reach: reach, overshoot: overshoot, verdict: verdict };
  }

  function renderRunoff(r, roofSqM, stormMmHr, perSpoutLMin) {
    return "A roof " + roofSqM + " sq m in a labeled " + stormMmHr + " mm/hr storm sheds " + plural(r.flow, "liter") + " a minute - " + plural(r.spouts, "downspout") + " at a labeled " + perSpoutLMin + " L/min" + (r.spouts === 1 ? "" : " each") + ", with " + r.headroom + " L/min of headroom - " + r.verdict + ".";
  }

  function renderDrop(r, wallCm, bracketCm) {
    return "A drop " + wallCm + " cm is one straight pipe; at a labeled " + bracketCm + " cm bracket spacing it takes " + plural(r.brackets, "bracket") + ", both ends included, with " + r.spare + " cm of extra spacing - " + r.verdict + ".";
  }

  function renderSpread(r, distanceCm, sectionCm) {
    return "A target " + distanceCm + " cm from the foundation at a labeled " + sectionCm + " cm section takes " + plural(r.sections, "extension section") + ", reaching " + r.reach + " cm with " + r.overshoot + " cm to spare - " + r.verdict + ".";
  }

  var api = { runoffPlan: runoffPlan, dropPlan: dropPlan, spreadPlan: spreadPlan, renderRunoff: renderRunoff, renderDrop: renderDrop, renderSpread: renderSpread };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.DownspoutMath = api;
})(this);
