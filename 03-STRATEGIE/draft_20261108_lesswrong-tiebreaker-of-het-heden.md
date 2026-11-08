# DRAFT — LessWrong post
> Status: draft · Aangemaakt: 2026-11-08  
> Publicatiekanaal: LessWrong (EN)  
> Tags (voorstel): decision theory · ethics · longtermism · uncertainty · population ethics

---

# The Present Gets One Extra Vote: Certainty as a Tiebreaker Between Now and the Future

## The problem

Suppose you must choose between two actions. Both cause harm — one to people alive today, one to people who will exist in the future. The scale of harm seems roughly comparable. How do you decide?

The standard expected-value answer is: multiply probability by magnitude, sum across all affected beings, pick the lower total. Clean, symmetric, timeless.

But there is an asymmetry that this framework tends to obscure: **we are far more certain about present effects than future ones.** The further away in time an outcome is, the more uncertain our models, the longer the causal chain, and the larger the compounding error. Absolute predictive certainty about the future is impossible.

Does that epistemic asymmetry have moral weight? I think it does — at least as a tiebreaker.

---

## The proposal: 50% + 1

My tentative principle:

> **When choosing between actions that cause comparable harm to present versus future sentient beings, and no other decisive factor separates them, the present gets the tie-breaking vote.**

Borrowing language from democratic theory: in a tied vote, someone has to cast the deciding ballot. I'm suggesting that *certainty of effect* earns that ballot — and present effects are always more certain than future ones.

This is not a claim that present people matter more as a matter of intrinsic worth. It is an epistemic claim: **a harm we can observe with high confidence deserves to be weighted more heavily than a harm of equal expected magnitude that we cannot.**

The 50%+1 framing is a metaphor, not a formula. The underlying idea is that epistemic weight tracks temporal proximity — not because distance in time diminishes moral worth, but because it diminishes our ability to verify that the harm will materialise at all, in the form we expect, to the beings we imagine.

---

## Why this matters: the longtermism challenge

The longtermist position — most associated with effective altruism's academic wing — holds that future people matter exactly as much as present people, that there may be astronomically many of them, and that therefore almost any present sacrifice is justified if it reduces existential risk by even a tiny fraction.

I find this internally consistent but practically dangerous for two reasons:

**1. It treats model outputs as morally equivalent to observed facts.**  
The expected number of future people is a model. It rests on assumptions about civilisational stability, population dynamics, and physics that compound uncertainty over centuries or millennia. Using that number at face value in an ethical calculus gives speculative quantities the same moral authority as the suffering of an identifiable person in front of you today.

**2. It creates an asymmetric escape hatch.**  
If future stakes can always be inflated to dwarf present ones — because the future is long and the future population is large — then the framework can justify almost any present harm. This is not a reductio ad absurdum of longtermism itself, but it is a reason to build in a structural safeguard.

The tiebreaker principle is one such safeguard. It says: when the scales are genuinely balanced, do not let the speculative weight of the future tip them automatically.

---

## What this principle does *not* say

It is important to be precise about the limits:

- **It is not a general discount rate.** This is not temporal discounting in the economic sense (future utility is worth less simply because it is future). The claim is specifically about *certainty of effect*, not about *intrinsic value at a distance in time*.
- **It is not a licence to ignore the future.** When the evidence is strong that an action causes catastrophic future harm — climate change, nuclear proliferation, engineered pathogens — the tiebreaker does not apply, because the asymmetry in scale and evidential weight is not a tie.
- **It does not resolve hard cases.** It is a tiebreaker, not a decision procedure. It operates only when other morally relevant factors (magnitude, probability, reversibility, affected population size) leave the balance genuinely unresolved.

---

## The open question I cannot yet resolve

Here is what I am genuinely uncertain about — and what I am writing this post to think through:

**Should epistemic certainty function only as a tiebreaker, or as a continuous weighting factor in all inter-temporal comparisons?**

The tiebreaker version is modest: it only matters at the margins. The weighting-factor version is much stronger: every future harm should be discounted in proportion to our uncertainty about whether it will occur as modelled — and this discount should be applied across all comparisons, not just tied ones.

The weighting-factor version feels intuitively compelling. When I am 95% confident that action A causes X units of suffering today, and 30% confident that action B causes X units of suffering in 2200, it seems strange to treat these as morally equivalent even before we consider scale.

But the weighting-factor version also has a troubling consequence: it seems to license discounting future suffering simply because the future is hard to model. And we have good independent reasons to try to model it better rather than to adjust our ethics to our current epistemic limitations.

So I land, for now, on the tiebreaker. But I hold it lightly.

---

## A sketch toward formalisation

Let \( C(t) \) be a certainty function that maps temporal distance \( t \) to a confidence weight \( C \in (0, 1] \), where \( C(0) = 1 \) (the present is certain) and \( C(t) \to 0 \) as \( t \to \infty \).

The adjusted harm of an action is then:

$$H_{\text{adj}} = H_{\text{expected}} \times C(t)$$

Under the **tiebreaker** interpretation, \( C(t) \) is used only to break ties — it has no effect unless \( H_{\text{adj,present}} \approx H_{\text{adj,future}} \) under some standard calculation.

Under the **weighting-factor** interpretation, \( C(t) \) is applied to all inter-temporal comparisons.

The shape of \( C(t) \) is itself an empirical question. Is our forecasting accuracy roughly exponential in temporal distance? Linear? Stepwise (near future / far future / deep future)? This matters enormously for how much weight the principle carries in practice.

---

## Conclusion

I am proposing a principle that is small by design: when present and future harms are otherwise comparable, give the present the tie-breaking vote, because present effects are more certain. This is not anthropocentrism, not temporal chauvinism, and not a dismissal of longtermist concerns. It is an attempt to build epistemic humility into inter-temporal ethics without abandoning the future altogether.

The bigger question — whether certainty should function as a continuous weighting factor rather than a tiebreaker — I leave open. I suspect the answer depends on how good our models of the far future actually are, and on whether we believe that epistemic limitations should constrain moral weights or only decision procedures.

I would be interested in:
- Arguments that the tiebreaker framing is too weak to do useful ethical work
- Arguments that it is already too strong (i.e., that any certainty discount is a form of illegitimate future-discounting)
- Formal frameworks in decision theory or population ethics that have already engaged with this structure — I am sure I am not the first to think about it this way, and I would rather build on existing work than reinvent it badly

---

*This post is part of an ongoing book project on competence, decision-making, and future-oriented thinking. Cross-posted from that project's working notes.*

