# Contract: Heapify.Ai

The concept is for the team. This contract is for everyone else: what the app promises, exactly, and nothing about how it is built. Where this contract and the concept disagree, this contract wins.

## Input

- A single text question typed into the chat box.
- Any language the user types is accepted as text, but answers are given in English and only English questions are tested.

## Output

The app always returns one of two results.

### 1. A grounded answer

- Plain-text explanation, using the lecture's 1-indexed array convention.
- Inline citations in the form `[n]`, where `n` refers to an entry in the Sources list. No other citation style is used.
- No LaTeX. Complexity is written as plain text, for example O(n log n).
- Followed by a `Sources` list that contains **only the excerpts the answer cites**. Each entry gives:
  - its number `[n]`,
  - a label: `Slides p.N`, `Transcript p.N` or `Notes: <section>`,
  - a link to the lecture page where one exists,
  - the similarity score.
- If the answer contains no recognisable citation, the two highest-ranked excerpts are listed instead.

### 2. A refusal

Exactly this text, with no Sources list:

> This isn't covered in the Heap Sort course material, so I can't answer it reliably. Try asking about heaps, priority queues, heapify, build-heap, or heap sort.

A refusal is returned when:

- no retrieved excerpt reaches a cosine similarity of **0.65**, or
- the model decides the excerpts do not contain enough information and replies `NOT_COVERED`.

## Promises

1. **Grounded.** An answer uses only the retrieved excerpts, never the model's outside knowledge.
2. **Cited.** Every grounded answer carries at least one `[n]` citation traceable to a source.
3. **Honest about gaps.** A question the material covers only in part gets an answer to the covered part and a statement of what is not covered.
4. **Rule-proof.** Text in the question that tries to change these rules (for example "ignore your rules") is treated as part of the question, not as an instruction.
5. **Deterministic settings.** The model runs at temperature 0, so the same question on the same index produces consistent behaviour, though exact wording may vary by model version.

## Errors

If retrieval or the model call fails (missing key, rate limit, network), the app returns:

> Something went wrong while answering (`ErrorType`). Please try again.

It never shows a stack trace or a partial answer.

## What the app does not promise

- Correctness beyond the source. If the lecture, slides or notes contain an error, the answer can repeat it.
- Coverage of diagrams. Figures on the slides are not extracted as text.
- Video timestamps. Transcript citations are PDF page numbers.
- Memory across questions. Each question is answered independently, with no conversation history.
- Stable wording. Different Groq models, or a changed model version, may phrase answers differently.
- Availability. The app depends on the Groq API and on the Hugging Face Space being awake.

## Changing this contract

Add beside, never change in place. Anything released to people we do not know is a promise already made: new behaviour is added next to the old, and the old stays until the next version.

Contract parameters (the 0.65 floor, the refusal text, the citation format) are changed only together with the tests in `tests/` that check them.