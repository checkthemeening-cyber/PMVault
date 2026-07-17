# 統合コンサルティング支援エージェントシステム - 実装ノート

**作成日**: 2026年7月11日

---

## 実装概要

### システムアーキテクチャ

```
┌─────────────────────────────────────────────────────────┐
│                      PMAgent                            │
│  (統括・質問対応・出力統合)                              │
└────────────┬─────────────────────────┬──────────────────┘
             │                         │
    ┌────────▼──────────┐   ┌─────────▼──────────┐
    │ ExternalResearch  │   │ InternalResearch   │
    │    Agent          │   │    Agent           │
    │ (Web調査)         │   │ (Archive検索)      │
    └────────┬──────────┘   └─────────┬──────────┘
             │                         │
             └────────┬────────────────┘
                      │
            ┌─────────▼──────────┐
            │ AnalystAgent       │
            │ (統合分析)         │
            └─────────┬──────────┘
                      │
            ┌─────────▼──────────┐
            │ PPTDesignerAgent   │
            │ (資料作成)         │
            └─────────┬──────────┘
                      │
         ┌────────────┼────────────┐
         │            │            │
    ┌────▼───┐  ┌────▼────┐  ┌───▼─────┐
    │ Markdown│  │  JSON   │  │   PPT   │
    │ Report  │  │ Analysis│  │ Present │
    └─────────┘  └─────────┘  └─────────┘
```

---

## エージェント実装詳細

### 1. ExternalResearchAgent (外部リサーチエージェント)

**役割**: Web上の情報を検索・収集

**主要メソッド**:
- `execute(theme)`: メイン実行メソッド
  - 複数の検索クエリを自動生成
  - 各クエリについて Web 検索を実施
  - ResearchResult リストを返す

- `_web_search(query)`: Web検索の実装
  - 現在はサンプルデータを生成
  - 実装: requests + BeautifulSoup またはAPI連携

- `_create_sample_web_results(query)`: サンプル結果生成
  - 3種類のサンプルソースを生成
  - タイトル、コンテンツ、信頼度を含む

**データ構造** (ResearchResult):
```python
@dataclass
class ResearchResult:
    topic: str              # 調査テーマ
    source_type: str        # "web" or "archive"
    title: str              # タイトル
    content: str            # コンテンツ（最大1000文字）
    url: Optional[str]      # URL
    confidence: float       # 信頼度 (0.0-1.0)
    timestamp: str          # タイムスタンプ
```

**検索クエリの生成ロジック**:
```
"{テーマ} 最新動向"
"{テーマ} ベストプラクティス"
"{テーマ} トレンド 2024 2025"
"{テーマ} 事例"
```

**エラーハンドリング**:
- Web検索失敗時も処理を継続（ロギングのみ）
- requests ライブラリなし時はスキップ

---

### 2. InternalResearchAgent (内部リサーチエージェント)

**役割**: PMVault の 40.archive から関連プロジェクトを検索

**主要メソッド**:
- `execute(theme)`: メイン実行メソッド
  - Archive 検索と情報抽出を実施
  - ResearchResult リストを返す

- `_find_relevant_projects(theme)`: プロジェクト検索
  - テーマからキーワードを抽出
  - 各プロジェクトの Overview.md を確認
  - キーワードマッチしたプロジェクトを返す

- `_extract_keywords(theme)`: キーワード抽出
  - 日本語テキスト処理
  - 一般的な止め言葉を除外
  - 上位5キーワードを抽出

- `_matches_keywords(file_path, keywords)`: キーワードマッチング
  - ファイル内容とキーワードを比較
  - 1つ以上のキーワード一致で該当と判定

- `_extract_project_info(project_path, theme)`: プロジェクト情報抽出
  - Overview.md を読み込み
  - プロジェクト名と概要をまとめる
  - ResearchResult を生成

**アーカイブディレクトリ構造**:
```
40.archive/
├── 2006/
├── 2007/
│   ├── 001_JNES_JNES/
│   │   ├── Overview.md
│   │   ├── README.md
│   │   └── ...
│   └── ...
└── 2017/
```

**キーワード抽出ロジック**:
1. 止め言葉を除外（「の」「に」「を」など）
2. 文字列を分割
3. 1文字以上2文字以下は除外
4. 小文字に統一
5. 上位5つを選択

**マッチング精度**: 1つ以上のキーワードが一致すれば該当

---

### 3. AnalystAgent (アナリストエージェント)

**役割**: 複数のリサーチ結果を統合分析

**主要メソッド**:
- `execute(external_results, internal_results, theme)`: メイン実行
  - 4つの分析を実施
  - AnalysisOutput を返す

- `_extract_key_findings(results, theme)`: 主要知見の抽出
  - 外部/内部結果の統計情報を分析
  - 4項目の主要知見を生成：
    1. 市場トレンド
    2. 内部事例パターン（内部検索がある場合）
    3. 統合的アプローチの必要性
    4. 業界別アプローチの差異

- `_identify_gaps(results, theme)`: ギャップの特定
  - 不足情報を特定
  - 4項目のギャップを生成

- `_extract_implications(results, theme)`: 示唆の抽出
  - 戦略的な洞察を導き出す
  - 4項目の示唆を生成

- `_generate_recommendations(results, theme, implications)`: 推奨事項の生成
  - 5段階の推奨アクション
  - 実行可能な形で具体化

- `_create_summary(findings, implications, recommendations)`: 統合サマリー作成
  - 全体的なまとめを作成

**出力形式** (AnalysisOutput):
```python
@dataclass
class AnalysisOutput:
    key_findings: List[str]        # 3-4項目
    gaps: List[str]                 # 3-4項目
    implications: List[str]         # 4項目
    recommendations: List[str]      # 5項目
    integrated_summary: str         # テキスト
```

**分析アルゴリズム**:
1. 外部/内部リサーチの結果を統合
2. 結果セットの統計（件数、種類）を分析
3. パターン認識（テンプレートベース）
4. 構造化出力を生成

---

### 4. PPTDesignerAgent (PPTデザイナーエージェント)

**役割**: AnalysisOutput を PowerPoint に変換

**主要メソッド**:
- `execute(analysis, theme, output_path)`: メイン実行
  - Presentation オブジェクトを作成
  - 8つのスライドを追加
  - .pptx ファイルを保存

**スライド構成**:
1. `_add_title_slide()`: タイトルスライド
   - テーマを大きく表示
   - 「統合分析レポート」サブタイトル
   - 実行日を記載
   - 背景色: 濃紺

2. `_add_agenda_slide()`: アジェンダ
   - 5つのセッション
   - 見出し形式

3. `_add_current_state_slide()`: 現状分析
   - 市場環境について
   - 4つのポイント

4. `_add_challenges_slide()`: 主要課題
   - ギャップ情報をそのまま表示
   - 最大4項目

5. `_add_implications_slide()`: 戦略的示唆
   - 示唆情報をそのまま表示
   - 最大4項目

6. `_add_recommendations_slide()`: 推奨アクション
   - 推奨事項を表示
   - 最大5項目

7. `_add_roadmap_slide()`: 実装ロードマップ
   - 4段階のフェーズ
   - 期間とアクティビティを記載

8. `_add_conclusion_slide()`: 結論
   - メインメッセージ
   - 背景色: ライトグレー
   - テキストを中央配置

**デザイン仕様**:
- スライドサイズ: 10" x 7.5"
- カラースキーム:
  - 背景（タイトル）: RGB(0, 51, 102) - 濃紺
  - タイトルテキスト: RGB(255, 255, 255) - 白
  - サブタイトル: RGB(255, 200, 0) - ゴールド
  - 本文: RGB(0, 0, 0) - 黒
- フォント:
  - タイトル: 54pt Bold
  - セクションタイトル: 28pt Bold
  - 本文: 18-24pt

**エラーハンドリング**:
- python-pptx なし時はスキップ
- ファイル書き込み失敗時は None を返す

---

### 5. PMAgent (PM エージェント)

**役割**: 全体を統括し、出力を生成

**主要メソッド**:
- `execute(theme, output_dir)`: メイン実行フロー
  1. ExternalResearchAgent を実行
  2. InternalResearchAgent を実行（並行実行可能）
  3. AnalystAgent を実行
  4. Markdown レポートを生成
  5. JSON 分析結果を保存
  6. PPTDesignerAgent を実行
  7. 結果を返す

- `_create_markdown_report()`: Markdown レポート生成
  - 構造化されたレポートを生成
  - セクション: 概要、知見、課題、示唆、推奨事項、調査方法、次ステップ

- `_create_analysis_json()`: JSON 分析結果保存
  - 構造化データを JSON 形式で保存
  - API 連携用の中間フォーマット

**処理フロー**:
```
ユーザー入力受け取り
    ↓
[並行実行]
├─ 外部リサーチ実行
└─ 内部リサーチ実行
    ↓
リサーチ結果の統合
    ↓
アナリスト実行
    ↓
出力ファイル生成
├─ Markdown
├─ JSON
└─ PPT
    ↓
完了ログ出力
```

**タイムスタンプ形式**: `YYYYMMDD_HHMMSS`

---

## データフロー

### ResearchResult → AnalysisOutput

```
[ResearchResult, ...]  (12-13件)
        ↓
  AnalystAgent._extract_key_findings()
        ↓
[key_findings, gaps, implications, recommendations]
        ↓
   AnalysisOutput
```

### AnalysisOutput → PPT

```
AnalysisOutput
    ├─ key_findings → スライド
    ├─ gaps → スライド
    ├─ implications → スライド
    └─ recommendations → スライド
        ↓
    Presentation object
        ↓
    .pptx file
```

---

## 依存パッケージ

### 必須
- **python-pptx** (1.0.0以上)
  - PowerPoint ファイル生成
  - インストール: `pip install python-pptx`

### オプション（Web検索用）
- **requests** (2.25.0以上)
  - HTTP リクエスト
  - インストール: `pip install requests`

- **beautifulsoup4** (4.9.0以上)
  - HTML パース（Web検索実装時に使用）
  - インストール: `pip install beautifulsoup4`

### システム
- Python 3.6 以上
- pathlib（標準）
- json（標準）
- datetime（標準）
- subprocess（標準）

---

## ロギング機能

各エージェントは `log()` メソッドでアクティビティをログ出力:

```
[YYYY-MM-DD HH:MM:SS] [AgentName] Message
```

**ログレベル実装**:
- 情報ログ（主処理）: `log(message)`
- エラーハンドリング: `log(f"Error: {error}")`

---

## エラーハンドリング戦略

### Web検索の失敗
```python
except Exception as e:
    self.log(f"Error during web search: {str(e)}")
    return []  # 空リストで継続
```

### アーカイブ検索の失敗
```python
except Exception as e:
    self.log(f"Error searching archive: {str(e)}")
    # 空リストで継続
```

### PPT生成の失敗
```python
except Exception as e:
    self.log(f"Error creating PPT: {str(e)}")
    return None  # スキップで継続
```

**フォールバック戦略**:
- Web検索失敗 → Markdown/JSON は生成（PPT のみ失敗）
- Archive検索失敗 → 「該当プロジェクトなし」と記載
- PPT生成失敗 → "PPT generation failed" と記載

---

## パフォーマンス最適化

### 実施した最適化
1. **並行実行**: 外部/内部リサーチを理論上並行可能
2. **早期終了**: エラー時も処理継続で全出力を確保
3. **メモリ効率**: ResearchResult をデータクラスで管理
4. **I/O最適化**: ファイルは1回の write で処理

### 実行時間の目安
- Web検索: < 1秒（サンプルデータの場合）
- Archive検索: 0.1-0.5秒（ディレクトリサイズ依存）
- 分析処理: < 0.1秒
- PPT生成: 0.5-1秒
- **合計**: 2-3秒

---

## 拡張ポイント

### 1. Web検索の実装
`ExternalResearchAgent._web_search()` を以下のように改善:

```python
def _web_search(self, query: str):
    # Google Custom Search API
    # Bing Search API
    # スクレイピング（requests + bs4）
```

### 2. Archive検索の改善
- 全文検索エンジン導入（Elasticsearch 等）
- メタデータベース化
- 全ファイル型対応（Artifacts など）

### 3. 分析ロジックの高度化
- 機械学習によるテーマ分類
- 自然言語処理による要約
- 感情分析

### 4. PPT設計の拡張
- グラフ・チャート の自動生成
- テンプレート選択
- カラーカスタマイズ

### 5. 出力フォーマット追加
- HTML レポート
- Excel 分析シート
- PDF 出力

---

## テストケース

### TC-1: 基本実行
**入力**: 「脱炭素経営」
**期待結果**:
- 外部リサーチ: 12件
- 内部リサーチ: 0件（テーママッチなし）
- 出力: MD, JSON, PPT

### TC-2: Archive マッチ
**入力**: 「スマートメーター」
**期待結果**:
- 外部リサーチ: 12件
- 内部リサーチ: 1件（002_スマートメーター_東京電力）
- 出力: MD, JSON, PPT
- MD内に過去事例の記載

### TC-3: 長いテーマ
**入力**: 「デジタルトランスフォーメーション推進と組織変革」
**期待結果**: 正常処理（キーワード抽出: DX/推進/組織変革）

---

## セキュリティ考慮事項

1. **ファイルパス**: すべて Path 型で正規化
2. **入力検証**: テーマは文字列として使用（インジェクション対策）
3. **ファイルアクセス**: 既存ファイルはチェック → 存在確認後 open
4. **エラーメッセージ**: 内部詳細は非表示

---

## 既知の制限

1. **Web検索**: サンプルデータを使用（実装のプレースホルダー）
2. **言語**: 日本語テーマに最適化
3. **Archive**: 2006-2017年のみ（定期更新で拡張可能）
4. **出力形式**: 固定テンプレート（カスタマイズには コード修正が必要）

---

## 今後の改善案

### 短期（1-2週間）
- [ ] Web検索API の統合（Google Custom Search）
- [ ] エラーハンドリングの強化
- [ ] ログレベルの追加

### 中期（1ヶ月）
- [ ] Archive の定期更新パイプライン
- [ ] PPT テンプレートの複数化
- [ ] HTML レポート出力

### 長期（2-3ヶ月）
- [ ] Machine Learning による分析最適化
- [ ] 自然言語生成（GPT連携）
- [ ] リアルタイム監視ダッシュボード

---

**バージョン**: 1.0  
**作成日**: 2026年7月11日  
**最終更新**: 2026年7月11日
