// code-comments — opencode plugin
//
// opencode has no SessionStart equivalent, so the ruleset rides on the system
// prompt instead: 'experimental.chat.system.transform' runs before every LLM
// request and mutates output.system (a string[]) in place; its return value is
// discarded. See https://opencode.ai/docs/plugins.
//
// Installed as a symlink at ~/.config/opencode/plugins/code-comments.js. Node
// resolves the link before setting import.meta.url, so SKILL.md resolves inside
// the repo clone and edits there take effect on the next opencode start.

import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HEADER = 'CODE-COMMENT RULES ACTIVE — apply when writing or editing comments in source files.';

function ruleset() {
  const skill = join(dirname(dirname(fileURLToPath(import.meta.url))), 'SKILL.md');
  const body = readFileSync(skill, 'utf8').replace(/^---[\s\S]*?\n---\n/, '');
  return HEADER + '\n\n' + body.trim();
}

export const CodeCommentsPlugin = async () => {
  // Read once at load: a file read per LLM request buys nothing when the file
  // only changes between opencode restarts.
  let rules;
  try {
    rules = ruleset();
  } catch (e) {
    // A missing SKILL.md means the clone moved. Degrade to no injection rather
    // than break every request in the session.
    return {};
  }

  return {
    'experimental.chat.system.transform': async (_input, output) => {
      if (!output || !Array.isArray(output.system)) return;
      // Idempotent: opencode is expected to rebuild output.system per request,
      // but an unguarded append against a reused array grows the system prompt
      // every turn until it eats the context window.
      if (output.system.some((s) => typeof s === 'string' && s.includes(HEADER))) return;
      output.system.push(rules);
    },
  };
};

export default CodeCommentsPlugin;
