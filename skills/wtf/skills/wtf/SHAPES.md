# Drawing vocabulary

The worked example of every shape in `/wtf`'s match table, plus the rules that
belong to one shape rather than all of them. Copy the geometry, not the content.

Every drawing goes in an `ini` fence. The Split is the one exception.

**Flow** — a sequence, a pipeline, a request's life:

```ini
request --> auth --> handler --> database
              |
              +--> 401, done      # most traffic stops here
```

**Boxed flow** — same thing when the stages are components rather than steps:

```ini
╭─────────╮      ╭─────────╮      ╭─────────╮
│ request │ -->  │  auth   │ -->  │ handler │
╰─────────╯      ╰─────────╯      ╰─────────╯
```

**Sequence** — who talks to whom, in order. The best shape there is for a protocol or a round trip:

```ini
browser          server           database
   |                |                 |
   |--- GET /x ---->|                 |
   |                |--- SELECT ----->|
   |                |<--- 3 rows -----|
   |<-- 200 --------|                 |
```

**Branch** — a decision and what each outcome costs:

```ini
          request
             |
          [ auth ]
          /     \
      fail       pass
        |          |
       401      handler
```

**Mapping** — old name becomes new name. One pair per line, arrows in a column:

```ini
state.Record    -->  pact.WorktreeRecord   # shared, stored
Status          -->  Lifecycle             # how far setup got
Status          -->  Provenance            # who made it
LastActivity    -->  TouchedAt
```

**Tree** — precedence, containment, override order:

```ini
config
├── defaults      # loaded first
├── user file     # overrides defaults
└── env vars      # wins over both
```

**State machine** — the transitions, including the one back:

```ini
  idle  --start-->  running  --done-->  done
    ^                  |
    +------stop--------+
```

**Nesting** — what lives inside what, what can reach what:

```ini
┌─ your server ──────────────┐
│  app code                  │
│  ┌─ connection pool ────┐  │   # new
│  │  10 open sockets     │  │
│  └──────────────────────┘  │
└────────────────────────────┘
```

**Split** — before and after, this way and that way. The one shape that uses a `diff` fence, because red and green already mean before and after:

```diff
- today:  3 round trips, ~120ms, any one failure kills it
+ after:  1 round trip,   ~40ms, one failure point
```

One fact per line and nothing trailing it. A caption column on the right gets coloured as though it were part of the comparison, which turns the fence into a two-column table that lies. Box-drawing and block characters stay out of a `diff` fence — the gutter eats the walls and the rows fuse into one slab.

**Bars** — proportion, cost, where the time goes. Half-blocks, number on the right:

```ini
database    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄     81%
rendering   ▄▄▄                  14%
everything  ▄                     5%
```

`▄` only. Never `░ ▒ ▓`, which render as solid slabs rather than texture, and never full-height `█` — stacked rows touch and fuse into one staircase shape instead of reading as separate quantities.

**Timeline** — sequence *and* duration, which bars can't carry:

```ini
build   ▄▄▄
test       ▄▄▄▄▄▄
deploy           ▄▄
        0s    30s    60s
```

**Sparkline** — the shape of a series in one line, drawn from `▁▂▃▄▅▆▇█`:

```ini
requests/min  ▁▂▃▅▇█▇▅▃▂▁▂▄▆█▇▅▃▁    # spike at 14:20
```

**Number line** — two values on a real scale, rather than two numbers side by side:

```ini
0ms         40ms                120ms
|------------|--------------------|
             ^ after              ^ today
```

**Table** — only for a real grid: several things compared on several axes. Write it as a markdown table and let the terminal draw it; never hand-draw a grid. Two things on one axis is a Split, not a table.
