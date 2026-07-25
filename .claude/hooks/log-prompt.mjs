#!/usr/bin/env node
// Claudeへの依頼と、その実行結果を Vault の 40_運用/log.md に追記するHook。
// 同じスクリプトを2つのイベントに登録し、hook_event_name で分岐する:
//   UserPromptSubmit → 「日時」と「依頼」を追記
//   Stop             → 直前の依頼に対する「結果」を追記（トランスクリプトの最終応答から取得）
// どちらも追記のみ。既存行は書き換えない。
// Vaultのパスは第1引数で渡す（cmd/bash/PowerShellのどれで実行されても効く）。環境変数 OBSIDIAN_VAULT でも可。
import { readFileSync, appendFileSync, existsSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { homedir, tmpdir } from 'node:os';
import { join, basename, dirname } from 'node:path';

// Git Bash 形式の /c/Users/... を Windows が解釈できる C:/Users/... に直す。
const toNative = (p) =>
  process.platform === 'win32' && typeof p === 'string' ? p.replace(/^\/([a-zA-Z])\//, '$1:/') : p;

const VAULT = toNative(process.argv[2] || process.env.OBSIDIAN_VAULT || join(homedir(), 'Documents', 'PMVault'));

let input = '';
try { input = readFileSync(0, 'utf8'); } catch { process.exit(0); }
let data = {};
try { data = JSON.parse(input); } catch { process.exit(0); }

const file = join(VAULT, '40_運用', 'log.md');
const session = String(data.session_id || data.sessionId || 'nosess');
// 依頼と結果の対応付け用。並行セッションがログを交互に書いても追える。
const tag = `${basename(data.cwd || process.cwd())}#${session.slice(0, 4)}`;
// 依頼と結果を繋ぐ受け渡し。Vaultは汚さずOSの一時領域に置く。
const stateFile = join(tmpdir(), 'claude-log-prompt', session.replace(/[^\w.-]/g, '_') + '.json');

const pad = (n) => String(n).padStart(2, '0');
const now = new Date();
const day = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
const time = `${pad(now.getHours())}:${pad(now.getMinutes())}`;

// 箇条書き1行に収める。改行と連続空白は潰す。
function oneLine(s, max) {
  const t = String(s).replace(/\s+/g, ' ').trim();
  return t.length > max ? t.slice(0, max) + ' …' : t;
}

function append(text) {
  try { mkdirSync(dirname(file), { recursive: true }); } catch { return false; }
  if (!existsSync(file)) {
    const header = `---\ntype: ログ\nstatus: 参照用\ntopic: log\ntags: [log]\n---\n\n# log ― 操作ログ\n`;
    try { appendFileSync(file, header); } catch { return false; }
  }
  try { appendFileSync(file, text); return true; } catch { return false; }
}

// トランスクリプトを末尾から辿り、最後のアシスタント応答テキストを1つ返す。
// thinking と tool_use は対象外。サブエージェント（isSidechain）も除外。
function lastAssistantText(rawPath) {
  const path = toNative(rawPath);
  if (!path || !existsSync(path)) return null;
  let lines;
  try { lines = readFileSync(path, 'utf8').split('\n'); } catch { return null; }
  for (let i = lines.length - 1; i >= 0; i--) {
    if (!lines[i].trim()) continue;
    let o;
    try { o = JSON.parse(lines[i]); } catch { continue; }
    if (o.type !== 'assistant' || o.isSidechain) continue;
    const blocks = o.message && o.message.content;
    if (!Array.isArray(blocks)) continue;
    const text = blocks.filter((b) => b && b.type === 'text').map((b) => b.text).join(' ').trim();
    if (text) return { uuid: o.uuid || '', text };
  }
  return null;
}

const event = data.hook_event_name || (data.prompt ? 'UserPromptSubmit' : 'Stop');

if (event === 'UserPromptSubmit') {
  const prompt = (data.prompt || '').trim();
  if (!prompt) process.exit(0);
  if (!append(`\n- ${day} ${time}　[${tag}]\n    - 依頼: ${oneLine(prompt, 500)}\n`)) process.exit(0);
  // この時点での最終応答を控えておく。Stop時にこれと同じなら新しい応答が未書き込みと判断する。
  const before = lastAssistantText(data.transcript_path);
  try {
    mkdirSync(dirname(stateFile), { recursive: true });
    writeFileSync(stateFile, JSON.stringify({ tag, beforeUuid: before ? before.uuid : '' }));
  } catch {}
  process.exit(0);
}

if (event === 'Stop') {
  if (data.stop_hook_active) process.exit(0);
  // 対応する依頼が無ければ結果だけを孤立して書かない。
  if (!existsSync(stateFile)) process.exit(0);
  let state = {};
  try { state = JSON.parse(readFileSync(stateFile, 'utf8')); } catch {}
  try { rmSync(stateFile); } catch {}
  const last = lastAssistantText(data.transcript_path);
  const fresh = last && last.uuid !== state.beforeUuid;
  append(`    - 結果: (${time}) ${fresh ? oneLine(last.text, 400) : '（応答テキストを取得できませんでした）'}\n`);
  process.exit(0);
}

process.exit(0);
