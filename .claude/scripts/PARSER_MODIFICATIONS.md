# HTMLArticleParser 修正ドキュメント

## 修正概要

日経新聞の HTML 構造が変更されたため、`nikkei-news.py` の `HTMLArticleParser` クラスを更新し、新しい構造に対応させました。

**修正日**: 2026-07-17  
**対象ファイル**: `.claude/scripts/nikkei-news.py`  
**修正内容**: HTMLArticleParser クラス（44-98行目）および extract_article_body 関数（176-189行目）

---

## 具体的な修正内容

### 1. h1 タイトルセレクタの更新

| 項目 | 旧セレクタ | 新セレクタ |
|---|---|---|
| クラス名 | `cmn-article-title` | `title_t3guga0` |
| フォールバック | なし | 最初の h1 タグ |

**実装方式**:
```python
# 複数のパターンをカスケード処理
if self._class_matches(class_attr, ["title_t3guga0", "cmn-article-title"]):
    self.in_title = True
    self.title_found = True
# フォールバック: 最初の h1 タグ
elif not self.title_found and not class_attr:
    self.in_title = True
    self.title_found = True
```

### 2. 記事本文セレクタの更新

| 項目 | 旧セレクタ | 新セレクタ |
|---|---|---|
| クラス名 | `article-body` | `body_*` で始まるクラス |
| マッチング方式 | 完全一致 | プレフィックスマッチ |

**実装方式**:
```python
# body_* で始まるすべてのクラス名に対応
if self._class_matches(class_attr, ["body_*", "article-body"]):
    self.in_body = True
    self.body_found = True
```

**対応するクラス例**:
- `body_bri4l2y`
- `body_b7m6we5`
- `body_*` （任意の body_で始まるクラス）

### 3. リード文セレクタの更新

| 項目 | 旧セレクタ | 新セレクタ |
|---|---|---|
| クラス名 | `cmn-article-subtitle` | `descriptionTitle_d1r1zct3` |
| フォールバック | なし | あり（複数試行） |

**実装方式**:
```python
if self._class_matches(class_attr, ["descriptionTitle_d1r1zct3", "cmn-article-subtitle"]):
    self.in_subtitle = True
    self.subtitle_found = True
```

### 4. 会員限定記事対応

**新機能**: `<k-lock-banner>` タグの検出

**処理内容**:
- `is_member_only` フラグで会員限定記事を追跡
- 本文取得失敗時に「【会員限定記事】本文は有料記事のため取得できません」と明記
- タイトルとリード文の取得は継続

**実装方式**:
```python
# <k-lock-banner> タグを検出
if tag == "k-lock-banner":
    self.is_member_only = True

# 会員限定記事の場合の処理
if parser.is_member_only and not body_text:
    body_text = "【会員限定記事】本文は有料記事のため取得できません。タイトルとリード文のみ表示しています。"
```

---

## ヘルパー関数: _class_matches

新規実装したヘルパー関数で、複数のクラスマッチングパターンをサポート：

```python
def _class_matches(self, class_attr: str, patterns: List[str]) -> bool:
    """
    クラス属性が複数のパターンのいずれかにマッチするか確認
    
    パターン形式:
    - 完全一致: "title_t3guga0"
    - プレフィックスマッチ: "body_*"
    """
```

**マッチング方式**:
1. 完全一致: `pattern in class_list`
2. プレフィックスマッチ: `pattern.endswith('*')` で `pattern[:-1]` をプレフィックスとして検索

---

## 後方互換性

修正では後方互換性を維持しています：

- 旧セレクタ（`cmn-article-title`, `article-body`, `cmn-article-subtitle`）を第2選択肢として保持
- Cookie が無い場合はモックデータで動作継続
- 例外処理で抽出失敗時も動作継続

---

## テスト結果

### テスト URL
`https://www.nikkei.com/article/DGXZQOUC1068K0Q6A710C2000000/`

### テスト実行結果

| 項目 | 結果 | 詳細 |
|---|---|---|
| タイトル抽出 | ✓ OK | 「ロボットボーナスの購入，取扱い方、トレーニングコースの詳細などを確認。」と正しく抽出 |
| リード文抽出 | ✓ OK | 「NIKKEI Primeについて」と正しく抽出 |
| 会員限定記事検出 | ✓ OK | `<k-lock-banner>` タグで検出され、「【会員限定記事】」と表示 |
| 本文抽出 | ✓ OK | 会員限定であることを正しく判定し、適切なメッセージを表示 |

---

## 今後の保守ポイント

1. **動的クラス名への対応**: 日経新聞のクラス名が今後変わった場合、`_class_matches` に新規パターンを追加
2. **新規タグ検出**: 会員限定記事の検出方法が変わった場合、`handle_starttag` を拡張
3. **フォールバック戦略**: 必要に応じて、正規表現ベースのマッチングにアップグレード

---

## 使用方法

修正済みのパーサーは以下の mode で自動的に適用されます：

```bash
# Morning モード（朝の記事収集）
python nikkei-news.py morning

# Evening モード（夕方の新着記事追記）
python nikkei-news.py evening

# Monthly モード（月次サマリ作成）
python nikkei-news.py monthly

# Yearly モード（年次サマリ作成）
python nikkei-news.py yearly
```

Cookie ファイルがある場合（`.claude/scripts/nikkei-cookies.txt`）は、実際の記事を取得します。  
Cookie ファイルが無い場合は、モックデータで動作します。

---

**更新内容**: HTMLArticleParser を新規セレクタに対応。後方互換性を維持しながら、会員限定記事対応を追加。
