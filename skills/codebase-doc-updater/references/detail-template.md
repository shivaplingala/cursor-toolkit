# CODE_DETAILS.md template

Every package folder (one that directly contains a `src/`) gets a
`CODE_DETAILS.md` next to its `src/`. Write it so a **small model with no
reasoning budget** can grep for a symbol and immediately know what it does and
how to call it. Lookup-first, terse, concrete.

## Required structure

````markdown
# Code Details: <package name or folder>
> Path: <folder>  ·  Source: <folder>/src  ·  Files: <N>

One or two sentences: what this package is responsible for and when code in the
rest of the repo would reach for it.

## Quick lookup
| Symbol | Kind | File | One-line purpose |
| --- | --- | --- | --- |
| `bootstrap` | function | src/index.ts | Start the app on a port |
| `AppConfig` | interface | src/index.ts | Shape of the app config object |
| `Button` | component | src/components/Button.tsx | Themed button |
| `Variant` | type | src/components/Button.tsx | Allowed button styles |

## src/index.ts

### function `bootstrap(port: number): void`
- **Does:** Boots the HTTP server and begins listening.
- **Use when:** You need to start the app; call once at process start.
- **Params:** `port` — TCP port to bind.
- **Returns:** nothing.
- **Notes / calls:** logs the port; throws if the port is taken.

### interface `AppConfig`
- **Does:** Describes runtime configuration.
- **Fields:** `port: number` (bind port) · `debug: boolean` (verbose logging).
- **Use when:** Typing config you pass into `bootstrap`.

## src/components/Button.tsx

### type `Variant = 'primary' | 'ghost'`
- **Does:** Enumerates allowed button styles.

### component `Button(props: { variant: Variant })`
- **Does:** Renders a styled button.
- **Props:** `variant` — which visual style to use.
- **Returns:** JSX element.
````

## Rules for the content

- **Cover every exported symbol** — functions, classes (and notable methods),
  interfaces, types, enums (list members), constants, React components, hooks.
  Internal/non-exported helpers only if they're load-bearing.
- **One block per symbol.** Lead each with its real signature in backticks.
- **Plain language.** "Use when" is the most valuable line — it tells a tiny
  model whether this is the symbol it's looking for. Always include it.
- **No invented behaviour.** Describe only what the source actually does. If a
  function's purpose is unclear from the code, say so briefly rather than guess.
- **Group by file**, files in the same order as the Quick lookup table.
- **Keep it scannable** — short bullets, not prose paragraphs. A reader should
  resolve "where is X and what does it do" from the lookup table plus one block.