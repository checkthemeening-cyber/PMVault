# 統合コンサルティング支援エージェントシステム - ユーザーガイド

## システム概要

複数のサブエージェントから構成される統合的なコンサルティング支援エージェントシステムです。ユーザーの質問・テーマに対して、Web調査、内部アーカイブ検索、統合分析、プレゼンテーション資料作成を自動で実行します。

**処理フロー:**
```
ユーザーの質問
    ↓
PMエージェント（統括）
    ├→ 外部リサーチエージェント（Web調査）
    └→ 内部リサーチエージェント（アーカイブ検索）
        ↓
    アナリストエージェント（統合分析）
        ↓
    PPTデザイナーエージェント（資料作成）
        ↓
出力ファイル（MD、JSON、PPTX）
```

---

## システム構成

### 1. PMエージェント（統括・質問対応）
**役割**: ユーザーの質問を受け取り、全体を統括

**主な機能**:
- ユーザー入力の受け取り
- 4つのサブエージェントへのタスク分解と指示
- 各エージェント間のデータ受け渡し
- 最終的な出力ファイルの生成

**実装ファイル**: `consulting-team.py` の `PMAgent` クラス

---

### 2. 外部リサーチエージェント（Web調査）
**役割**: Web上の最新情報を検索・収集

**主な機能**:
- テーマに関連する複数の検索クエリを自動生成
- Web上の最新情報、ニュース、トレンド、ベストプラクティスを収集
- 結果を構造化（タイトル、内容、出典、信頼度）して返す

**実装ファイル**: `consulting-team.py` の `ExternalResearchAgent` クラス

**自動生成される検索クエリ例**:
- 「{テーマ} 最新動向」
- 「{テーマ} ベストプラクティス」
- 「{テーマ} トレンド 2024 2025」
- 「{テーマ} 事例」

---

### 3. 内部リサーチエージェント（アーカイブ検索）
**役割**: PMVault の過去プロジェクト情報を検索

**主な機能**:
- `40.archive/` ディレクトリ（2006-2017年プロジェクト）から関連プロジェクトを検索
- テーマのキーワードを自動抽出し、マッチングを実施
- Overview.md、Artifacts、関連情報を抽出
- 過去のアウトプット、クライアント情報、実装事例を検出

**実装ファイル**: `consulting-team.py` の `InternalResearchAgent` クラス

**検索対象**:
- ディレクトリ構造: `40.archive/{年}/{プロジェクトフォルダ}/Overview.md`
- 抽出情報: プロジェクト概要、実施内容、成果物、クライアント情報

---

### 4. アナリストエージェント（統合分析）
**役割**: 外部研究と内部研究の情報を統合分析

**主な機能**:
- 外部研究・内部研究の結果を統合
- 共通のテーマ、ギャップ、示唆を抽出
- 以下の構造化分析結果を生成:
  - **主要な知見** (key_findings): 3-4項目
  - **主要課題** (gaps): 3-4項目
  - **戦略的示唆** (implications): 4項目
  - **推奨事項** (recommendations): 5項目

**実装ファイル**: `consulting-team.py` の `AnalystAgent` クラス

**出力形式** (JSON):
```json
{
  "key_findings": [...],
  "gaps": [...],
  "implications": [...],
  "recommendations": [...]
}
```

---

### 5. PPTデザイナーエージェント（資料作成）
**役割**: 分析結果をPowerPoint資料に変換

**主な機能**:
- アナリストの分析結果をスライドに変換
- ストーリー性を持たせた資料構成:
  1. タイトルスライド
  2. アジェンダ
  3. 現状・市場環境分析
  4. 主要課題
  5. 戦略的示唆
  6. 推奨アクション
  7. 実装ロードマップ（イメージ）
  8. 結論スライド

**実装ファイル**: `consulting-team.py` の `PPTDesignerAgent` クラス

**デザイン要素**:
- カラースキーム: 濃紺(RGB: 0, 51, 102)、ゴールド、ホワイト
- フォントサイズ: タイトル54pt、本文18-24pt
- レイアウト: 箇条書き中心の読みやすい構成

---

## 使用方法

### 基本的な実行方法

```bash
python consulting-team.py "調査テーマ"
```

### 実行例

```bash
cd C:\Users\check\PMVault
python .\.claude\scripts\consulting-team.py "脱炭素経営への戦略構築"
```

### コマンドライン引数

| 引数 | 必須 | 説明 |
|-----|------|------|
| テーマ（第1引数） | 必須 | 調査対象のテーマ（日本語テキスト） |

### 出力ファイル

実行後、`C:\Users\check\PMVault\consulting-output\` に以下のファイルが自動生成されます:

| ファイル | 拡張子 | 説明 |
|---------|--------|------|
| report_{timestamp} | .md | Markdown形式の統合レポート |
| analysis_{timestamp} | .json | 構造化された分析結果 |
| presentation_{timestamp} | .pptx | PowerPointプレゼンテーション |

**タイムスタンプ形式**: `YYYYMMDD_HHMMSS`

#### 出力例
```
report_20260711_135448.md
analysis_20260711_135448.json
presentation_20260711_135448.pptx
```

---

## 出力ファイル仕様

### 1. Markdownレポート (report_*.md)

構成:
- 概要: 調査の背景と目的
- 統合分析サマリー: 全体的な発見
- 主要な知見: 3-4の重要な発見
- 主要課題: 検出されたギャップ
- 戦略的示唆: 分析から導き出された示唆
- 推奨アクション: 5つの具体的アクション
- 調査方法: 実施した調査の詳細
- 提案する推進体制と次ステップ: 4段階のロードマップ

### 2. JSON分析結果 (analysis_*.json)

構造:
```json
{
  "theme": "調査テーマ",
  "timestamp": "2026-07-11T13:54:48.636271",
  "key_findings": [...],
  "gaps": [...],
  "implications": [...],
  "recommendations": [...],
  "integrated_summary": "..."
}
```

### 3. PowerPointプレゼンテーション (presentation_*.pptx)

スライド構成:
1. **タイトルスライド**: テーマとレポート日
2. **アジェンダ**: 5つのセッション
3. **現状分析**: 市場環境と関心事項
4. **主要課題**: 検出されたギャップ
5. **戦略的示唆**: 深い洞察
6. **推奨アクション**: 5つの具体策
7. **実装ロードマップ**: 段階別計画
8. **結論**: まとめメッセージ

---

## 実行例と結果

### 例1: 脱炭素経営

**コマンド**:
```bash
python consulting-team.py "脱炭素経営への戦略構築：東京ガスのケース"
```

**実行ログ**:
```
[2026-07-11 13:54:48] [PMAgent] Starting consulting process for theme: 脱炭素経営への戦略構築：東京ガスのケース
[2026-07-11 13:54:48] [PMAgent] Step 1: Executing external and internal research agents
[2026-07-11 13:54:48] [ExternalResearchAgent] Starting web research on: 脱炭素経営への戦略構築：東京ガスのケース
[2026-07-11 13:54:48] [ExternalResearchAgent] Web research completed. Found 12 results
[2026-07-11 13:54:48] [InternalResearchAgent] Starting internal archive search: 脱炭素経営への戦略構築：東京ガスのケース
[2026-07-11 13:54:48] [InternalResearchAgent] Found 0 relevant projects
[2026-07-11 13:54:48] [PMAgent] Step 2: Analyzing research results
[2026-07-11 13:54:48] [AnalystAgent] Analysis completed with 3 key findings
[2026-07-11 13:54:48] [PMAgent] Step 3: Generating output files
[2026-07-11 13:54:48] [PMAgent] Markdown report created: ...
[2026-07-11 13:54:48] [PMAgent] Analysis JSON created: ...
[2026-07-11 13:54:48] [PMAgent] Step 4: Designing PowerPoint presentation
[2026-07-11 13:54:48] [PPTDesignerAgent] PPT successfully created: ...
```

**生成ファイル**:
- `report_20260711_135448.md` (107行)
- `analysis_20260711_135448.json` (29行)
- `presentation_20260711_135448.pptx` (37KB)

### 例2: スマートメーター関連

**コマンド**:
```bash
python consulting-team.py "スマートメーター関連システムコンサル"
```

**実行結果の特徴**:
- 外部リサーチ: 12件の結果
- 内部アーカイブ: 1件のマッチング（002_スマートメーター関連システムコンサル_東京電力）
- 主要知見: 4項目（内部事例を含む）
- 課題: 3項目（過去データが充実している場合はギャップが減少）

---

## トラブルシューティング

### Q1: スクリプトが実行できない
**A**: 以下を確認してください:
- Python 3.6以上がインストールされている
- 必要なライブラリがインストールされている:
  ```bash
  pip install python-pptx requests beautifulsoup4
  ```

### Q2: 内部アーカイブが検索されない
**A**: 確認項目:
- `40.archive/` ディレクトリが存在する
- 各プロジェクトフォルダに `Overview.md` が存在する
- テーマキーワードが Overview.md に含まれている

### Q3: PPT生成に失敗する
**A**: 対処方法:
- `python-pptx` がインストールされているか確認
- 出力ディレクトリが書き込み可能か確認
- 失敗時は Markdown で代替される

### Q4: Web検索結果が実データでない
**A**: これは正常動作です:
- デモンストレーション用に Sample 結果を生成
- 実運用では、実際の検索API（Google Custom Search、Bing など）と統合可能

---

## カスタマイズ・拡張

### 外部リサーチエージェントのカスタマイズ

`ExternalResearchAgent._create_sample_web_results()` メソッドを編集して、
実際のWeb APIと連携することで本当のWeb検索を実装できます:

```python
def _web_search(self, query: str) -> Optional[List[ResearchResult]]:
    # Google Custom Search API などを使用
    # または、BeautifulSoup でスクレイピング
```

### 内部アーカイブパスの変更

デフォルトパスを変更する場合:

```python
# コマンドラインで指定
pm_agent = PMAgent()
results = pm_agent.execute(
    theme,
    output_dir="C:\\custom\\output\\path"
)
```

### PPTデザインの変更

`PPTDesignerAgent` の各 `_add_*_slide()` メソッドを編集して、
スライドレイアウト、配色、フォント等をカスタマイズできます。

---

## 技術仕様

### システム要件
- Python 3.6 以上
- Windows / macOS / Linux（パスの調整が必要）
- 依存パッケージ:
  - python-pptx 1.0.0以上
  - requests 2.25.0以上
  - beautifulsoup4 4.9.0以上

### ファイル構成
```
.claude/scripts/
├── consulting-team.py              # メインスクリプト
└── CONSULTING_SYSTEM_GUIDE.md      # このドキュメント

consulting-output/
├── report_*.md                     # Markdownレポート
├── analysis_*.json                 # JSON分析結果
└── presentation_*.pptx             # PowerPoint資料

40.archive/
├── 2006/
├── 2007/
├── ...
└── 2017/
    └── {ProjectFolder}/
        └── Overview.md             # 検索対象ファイル
```

### ログ出力
スクリプト実行時、各エージェントのアクティビティが標準出力に表示されます:

```
[YYYY-MM-DD HH:MM:SS] [AgentName] Message
```

---

## ベストプラクティス

### 1. テーマの指定方法
- **良い例**: 「脱炭素経営への戦略構築」、「DX推進とビジネス変革」
- **避けるべき例**: 「こと」、「その他」

### 2. 複数テーマの分析
一度に複数テーマを分析する場合は、各テーマごとに別々に実行:
```bash
python consulting-team.py "テーマ1"
python consulting-team.py "テーマ2"
```

### 3. 出力ファイルの活用
- **Markdown レポート**: ドキュメント作成、Wiki 登録用
- **JSON 分析結果**: API連携、自動化処理の入力
- **PPT 資料**: クライアントプレゼンテーション、内部報告用

### 4. アーカイブの充実
内部検索の精度を高めるため、`40.archive` に新しい事例が追加される際は、
適切な `Overview.md` を作成してください。

---

## その他の情報

### ライセンス
このシステムはクライアントプロジェクト向け内部ツールです。

### バージョン
- Version 1.0 (2026-07-11)
- Author: Claude Consulting Agent System

### フィードバック・改善提案
バグ報告や機能改善の提案は、プロジェクトマネージャーまでお願いします。

---

**最終更新**: 2026年7月11日
