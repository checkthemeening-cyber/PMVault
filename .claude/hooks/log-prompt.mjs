#!/usr/bin/env node
// あらゆるClaudeへの命令を、Vault の 40_運用/log.md に追記するHook。
// Claudeのユーザー設定（~/.claude/settings.json）の UserPromptSubmit から呼び出す。
import { readFileSync, appendFileSync, existsSync } from 'node:fs';
import { homedir } from 'node:os';
import { join, basename } from 'node:path';

const VAULT = process.env.OBSIDIAN_VAULT || join(homedir(), 'Documents', 'PMVault');

let input = '';
try { input = readFileSync(0, 'utf8'); } catch { process.exit(0); }
let data = {};
try { data = JSON.parse(input); } catch { process.exit(0); }
const prompt = (data.prompt || '').trim();
if (!prompt) process.exit(0);
const cwd = data.cwd || process.cwd();
const project = basename(cwd);

function category(p) {
  if (/調査|検索|調べ|リサーチ|ingest|取り込/i.test(p)) return '調査';
  if (/作成|作って|生成|レポート|スライド|pptx|資料|書いて/i.test(p)) return '作成';
  if (/修正|直して|変更|なおして|fix|update/i.test(p)) return '修正';
  if (/引き出|出して|時系列|何を知|教えて/i.test(p)) return '引き出し';
  return 'その他';
}

const now = new Date();
const pad = (n) => String(n).padStart(2, '0');
const day = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
const time = `${pad(now.getHours())}:${pad(now.getMinutes())}`;

const file = join(VAULT, '40_運用', 'log.md');
if (!existsSync(file)) {
  const header = `---\ntype: ログ\nstatus: 参照用\ntopic: log\ntags: [log]\n---\n\n# log ― 操作ログ\n`;
  try { appendFileSync(file, header); } catch { process.exit(0); }
}
const cat = category(prompt);
const body = prompt.length > 500 ? prompt.slice(0, 500) + ' …' : prompt;
const entry = `\n- ${day} ${time}　#${cat}　[${project}]　${body}\n`;
try { appendFileSync(file, entry); } catch {}
process.exit(0);
