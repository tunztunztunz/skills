---
name: dry-prose
description: >-
  Short, flat, plain-English prose for anything read while working: READMEs, API
  docs, guides, runbooks, procedures, agent output. Writes new text, or sweeps an
  existing draft.
disable-model-invocation: true
---

# Dry Prose

Someone is reading this while trying to do something else. They scan for one
thing and leave once they find it. Every word they read that is not the fact
costs them time.

Write the shortest version that carries the fact, in words anyone can read at
a glance. Rhythm, contrast, and a well-placed dash make a sentence worth
noticing. A reader in a hurry does not want to notice the sentence. Leave them
out.

Some of these readers are reading in a second language, and some of this text
will be machine translated. They want the same prose the scanning reader wants,
with the grammar left intact.

## Shape first

Sort the facts before writing a sentence. List everything the document has to
carry, one line each, then name the form that holds each cluster. A cluster
whose form is "a paragraph" is one you have not sorted yet: split it, or fold
it into its neighbour.

| What the cluster is | Form |
|---|---|
| One action after another | Numbered steps |
| Several things compared on several axes | Table |
| A value and what it means | Definition list or table |
| One case per condition | A heading per case |
| A single fact | A single sentence |

Prose captions a form, it does not replace one. Reach for a paragraph when
nothing above fits, and hold it to the two or three sentences the form needs
around it.

## Rules

**Write it short.** One idea per sentence. A sentence telling the reader to do
something gets 20 words; a sentence explaining what something is gets 25. Count
them. If a paragraph says one thing, make it one sentence. If a sentence works
with half its words, use half. Say it once: a fact stated twice in different
words is one fact and one wasted sentence.

**Shorten the sentence, keep the grammar.** Cut clauses, modifiers, and
repetition. Keep the small words that carry the relationship between the parts:
articles, "that", and connectives (and, but, or, because, if, when, so, then).
"Remove bolt" reads as a telegram; "Remove the bolt" reads as English. "Retry
fails, the token expired" leaves the reader to guess the link; "Retry fails
because the token expired" states it.

**Use words the reader can point at.** Keep a term only when it names
something the reader will meet: a function, a config key, a flag, an error
string, a noun the project publishes. Everything else is fog. "Surfaces the
primitives", "handles the lifecycle", "orchestrates the flow" name nothing the
reader can find, and they read as technical, so they survive every other rule
here. Replace each with the concrete thing, or cut the sentence. A term the
reader has to learn, because no plain word replaces it, gets four words of
definition at first use and then gets used freely, and an abbreviation gets its
full term the same way. Use one term for one thing across the whole document,
so "the worker", "the runner", and "the job process" all become whichever one
you picked. Common words everywhere else: "use" not "utilize", "start" not
"initiate", "about" not "regarding", "so" not "in order to".
[`WORDS.md`](WORDS.md) holds the rest of that list; read it when a word feels
formal and you want its plain replacement. Write quantities as numerals,
because a reader scanning for a number finds "3" and skims past "three".

**Address the reader.** Second person and the imperative. "Edit `config.yaml`
and set `endpoint`", not "the configuration file may then be edited to set the
endpoint". Passive voice and nominalization are the documentation equivalent of
flourish: they put a narrator between the reader and the action, and they hide
who does what. "Check the config", not "do a check of the config". Keep verbs
in simple tenses: "the file was written", not "the file has been written". An
"-ing" word is a verb, not a noun or an adjective: "before you start the
server", not "before starting the server"; "run the migration first", not
"running the migration is required".

**Keep noun clusters to three.** "background task queue retry policy config"
makes the reader parse six nouns to reach the one that matters. Break the run
with a preposition: "the retry policy for the background task queue".

**Put the condition before the action.** A reader who meets the action first
performs it, then finds out it did not apply. "If the install fails, delete the
lockfile", not "delete the lockfile if the install fails". The same order holds
for anything the reader needs before acting: the caveat on a destructive
command goes above the command, never below it.

**No em dashes in prose. Punctuate by relationship instead:** colon for a label
and its elaboration, period for two independent statements, semicolon when those
two belong together, comma for genuine subordination, parentheses for a real
aside worth keeping. Deciding mechanically is the point, because it removes the
moment where a writer reaches for a dash. Two exceptions, because they are not
prose: a standalone em dash (U+2014) in a table cell as an n/a marker, and en
dashes (U+2013) in ranges (5–23 December, 2025–26).

**Cut what isn't the fact.** Four tells:

- *Trailing reframe*: a clause restating what was just said. "Set `timeout` to
  0 to disable it, which means no timeout is applied." Delete it, or promote it
  to its own sentence if it carries new information.
- *Narrator frame*: "In this section we will", "It is worth noting that",
  "Importantly,". Delete the frame and keep the fact. The fact was always the
  sentence.
- *Intensifier*: a modifier the claim survives without. In documentation the
  recurring ones are "simply", "just", "easy", and "obviously", and they cost
  more than tokens: when the step does not work, they tell the reader the
  failure is theirs.
- *Smoothing transition*: "Moreover,", "That said,", "Ultimately,". If a
  paragraph falls apart without them, the ordering is wrong and they were
  hiding it.

**Describe what the system does, not what it is meant to do.** "Returns a
non-zero exit code and writes the reason to stderr", not "handles errors
gracefully". Intent is what the author holds; behavior is what the reader
needs. Where you have not checked, say so rather than describing the design.

**Keep "X, not Y" only when Y is a reading someone would actually make.** This
one takes judgment. "Returns null, not undefined, when the key is absent" rules
out the reading a reader would otherwise default to, so it carries information.
"Runs in the background, not the foreground" says one thing twice for emphasis,
so it carries only voice. Ask whether a reasonable reader would have made the
mistake Y describes. If not, cut Y.

**Lead with the conclusion.** The first sentence under a heading is the answer.
Context, caveats, and how it works come after it, or not at all. A reader who
stops after that one sentence still leaves with the fact.

**Headings say what is under them.** A reader scanning for one thing meets the
headings first and reads nothing else until one matches. "Advanced usage" tells
them nothing about whether their answer is there; "Streaming responses and
backpressure" does. Name the subject, not the section's rank.

## Mechanical pass

Run [`CHECK.md`](CHECK.md) over the finished text before the blind reader sees
it. Every line in it is countable: a word count, a search for a string, a scan
for one part of speech. Fix what fails and run it again. This pass catches what
a grep catches, which is why it goes first and why the blind reader is still
needed after it.

## Blind reader

You cannot judge whether your own prose landed. Every rule above works inside
one sentence, and a document of clean sentences still fails to carry an idea.
The check is a reader who has not seen what you meant.

Dispatch a subagent on Sonnet. Give it the text and nothing else: no draft, no
request, no rules, no hint of what you were going for. Ask it two questions:
what is this about, and what does it tell you to do?

Compare its answer to what you meant. Every gap is a failure in the prose, not
in the reader. Fix the gaps, dispatch again, and keep going until the answer
matches. Send the whole document when writing new. When sweeping, send the
passages you changed, together, in document order.

When two rounds of fixes leave the same gap, the sentences are not the problem.
Go back to Shape first: a fact the reader keeps missing is usually a fact buried
in a paragraph that should be a table or a numbered step.

A new document is done when every cluster sits in a form, every rule has been
applied, `CHECK.md` passes, the blind reader answered with what you meant, and
you have reported the word count before and after.

## Revising an existing draft

A sweep works sentence by sentence and leaves the document's existing forms
standing. When a paragraph is carrying a table's worth of facts, name it in your
report and let the user decide, rather than restructuring the document under
them.

Inventory before editing. Read every em dash in context before changing any of
them: some are load-bearing, a blind find-and-replace damages ranges and table
markers, and reading them all first surfaces the flourishes that contain no dash
at all, which are usually the more important edits.

Read each target string verbatim before replacing it, never from memory. When
the edit is programmatic, assert an expected match count for every pair and
refuse to write the file if any pair fails. A silently missed replacement is
invisible in the output; a loud failure list is not.

Re-read the output, not the diff. Tone problems live in flow and are invisible
line by line.

Leave verbatim material alone. Quoted text, code samples, command output, and
passages the user wrote and handed over are outside the sweep unless they ask
otherwise.

The sweep is done when every rule has been applied to the whole document,
every em dash has been replaced or deliberately kept, `CHECK.md` passes, the
blind reader answered with what you meant, and you have reported the word count
before and after.

## Over-correction

The failure mode is cutting facts along with the words. Shorten the sentence,
keep the fact. A sentence cut into ambiguity costs the reader more than the
flourish did. The second failure mode is cutting the grammar: a sentence
stripped to a telegram makes the reader rebuild the links between its parts,
so the articles, the connectives, and "that" stay. Do not flatten a heading
until it stops distinguishing its section from the next. Structure is not
voice: tables, headings, code blocks, parameter lists, and numbered steps are
how a scanning reader finds anything, so the forms from Shape first survive the
cut intact. Replace an em dash with real punctuation, never a comma splice.
