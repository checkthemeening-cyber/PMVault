---
type: 概念
status: 参照用
date: 2026-07-01
topic: MOC
tags: [MOC, 運用ルール]
source: 本文に各URL併記
last_verified: 2026-07-01
certainty: 有力
---

# コンテンツ地図（MOC）

要約：index.md が全ノートの目次なら、MOC は1テーマだけを手で選んで束ねた地図。AI が MOC を1枚読むだけで、その領域の主要ノートと相互リンクを一度に参照できる。

## MOC とは
- 手でキュレーションしたリンク集のノート。Wikipedia のポータルに近い
- 1つのノートは複数の MOC に同時に属してよい（フォルダと違い排他でない）
- ボトムアップに増えるリンク網へ、トップダウンの俯瞰を1枚重ねる役割

## index.md との違い
- index.md … Vault 全ノートのカタログ。増えると ingest / lint が更新する
- MOC … 案件・クライアント・テーマ1つに絞った地図。手で並べ、文脈を添える
- 使い分け：何があるかは index、この領域をどう読むかは MOC

## AI にとっての効き目
- 領域全体を1ファイルで提示できるので、PARA のアーカイブを掘る・Zettel のカードを1枚ずつ巡回するより速い … Nick Milo の LYT が示した利点 https://yu-wenhao.com/en/blog/lyt-framework-guide/ （LYTは2020提唱）
- 「Xについて時系列で」の問いに、AI は 40_運用/hot.md → index.md → 該当 MOC の順で必要分だけ読める

## いつ切るか
- 同じ topic のノートが10件を超えたら、そのテーマの MOC を1枚作る
- 案件単位・クライアント単位・手法単位など、後から何度も引く粒度で切る
- 作ったら index.md の『## 概念（00_ナレッジ/concepts/）』に [[コンテンツ地図（MOC）]] を1行足す

## 4つの手がかりとの接続
- MOC 自身も type: 概念 / status: 参照用 / topic: <テーマ> / tags: [MOC] を持つ
- 子ノートは frontmatter の topic を MOC と揃え、本文末尾で [[親MOC]] を指す

## 関連
- [[命名と4手がかり]]
- [[PKM手法カタログ]]
- [[ノートの粒度（atomic・evergreen）]]
- [[MOC_テンプレ]]

> 出典: LYT / MOC は Nick Milo が2020年に提唱（Linking Your Thinking）。実践ガイド https://yu-wenhao.com/en/blog/lyt-framework-guide/ ／ 常緑ノートの3原則 Andy Matuschak https://notes.andymatuschak.org/Evergreen_notes 。研修用に整理。
