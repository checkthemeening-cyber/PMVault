# 統合コンサルティング支援エージェントシステム

複数のサブエージェントから構成される統合的なコンサルティング支援エージェントシステムです。

## クイックスタート

### インストール

```bash
cd C:\Users\check\PMVault
pip install python-pptx requests beautifulsoup4
```

### 実行方法

```bash
python .\.claude\scripts\consulting-team.py "調査テーマ"
```

### 実行例

```bash
python .\.claude\scripts\consulting-team.py "脱炭素経営への戦略構築"
```

## 出力ファイル

実行後、`consulting-output/` に以下が生成されます:

1. **Markdown レポート** (`report_*.md`)
   - 統合分析結果の詳細レポート
   - 知見、課題、推奨事項を記載

2. **JSON 分析結果** (`analysis_*.json`)
   - 構造化された分析データ
   - API連携用

3. **PowerPoint プレゼンテーション** (`presentation_*.pptx`)
   - 8スライドの視覚的なプレゼンテーション
   - クライアント提示用

## システム構成

### 5つのエージェント

```
┌─────────────────────────────────────────┐
│   PMAgent（統括・質問対応）              │
├──────────────┬──────────────────────────┤
│              │                          │
│  ExternalResearchAgent     InternalResearchAgent
│  (Web調査)                 (Archive検索)
│              │                          │
├──────────────┴──────────────────────────┤
│  AnalystAgent（統合分析）                │
├─────────────────────────────────────────┤
│  PPTDesignerAgent（資料作成）            │
└─────────────────────────────────────────┘
```

### 各エージェントの役割

1. **PMAgent** - 統括・質問対応
   - ユーザーの質問を受け取り、全体を統括
   - 各エージェントの成果を統合
   - 最終的な回答を作成

2. **ExternalResearchAgent** - Web調査
   - Web上の最新情報、ニュース、トレンド、ベストプラクティスを収集
   - 複数の検索クエリを自動生成

3. **InternalResearchAgent** - Archive検索
   - PMVault の 40.archive（2006-2017年プロジェクト）から関連情報を検索
   - キーワードマッチングで関連プロジェクトを検出

4. **AnalystAgent** - 統合分析
   - 外部/内部リサーチ結果を統合
   - 共通テーマ、ギャップ、示唆を抽出
   - 推奨事項を生成

5. **PPTDesignerAgent** - 資料作成
   - 分析結果をPowerPointに変換
   - 8スライド（導入→現状→課題→示唆→推奨→ロードマップ→結論）

## ドキュメント

- **[CONSULTING_SYSTEM_GUIDE.md](CONSULTING_SYSTEM_GUIDE.md)** - 詳細な使用方法ガイド
- **[IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md)** - 技術仕様・実装詳細

## 実装ファイル

- `consulting-team.py` - メインプログラム（約900行）
- `CONSULTING_SYSTEM_GUIDE.md` - ユーザーガイド
- `IMPLEMENTATION_NOTES.md` - 実装ノート
- `README.md` - このファイル

## 処理フロー

```
ユーザー入力（調査テーマ）
    ↓
[Step 1] 並行リサーチ実行
  ├─ 外部リサーチ：Web検索（12件）
  └─ 内部リサーチ：Archive検索
    ↓
[Step 2] 分析処理
  └─ 統合分析：知見/課題/示唆/推奨を抽出
    ↓
[Step 3] 出力ファイル生成
  ├─ Markdown レポート
  └─ JSON 分析結果
    ↓
[Step 4] PPT資料作成
  └─ PowerPoint プレゼンテーション
    ↓
完了
```

## 使用例

### 例1: 脱炭素経営

```bash
python consulting-team.py "脱炭素経営への戦略構築"
```

**出力**:
- `report_20260711_135448.md` - 統合レポート（107行）
- `analysis_20260711_135448.json` - JSON分析結果
- `presentation_20260711_135448.pptx` - 8スライド資料

### 例2: スマートメーター

```bash
python consulting-team.py "スマートメーター関連システムコンサル"
```

**出力の特徴**:
- 内部リサーチで関連プロジェクト を検出
- 過去事例を分析結果に反映

## 出力ファイル仕様

### Markdown レポート構成

1. タイトル・作成日
2. 概要
3. 統合分析サマリー
4. 主要な知見（3-4項目）
5. 主要課題（3-4項目）
6. 戦略的示唆（4項目）
7. 推奨アクション（5項目）
8. 調査方法
9. 提案する推進体制と次ステップ

### JSON構造

```json
{
  "theme": "調査テーマ",
  "timestamp": "ISO 8601形式",
  "key_findings": [...],
  "gaps": [...],
  "implications": [...],
  "recommendations": [...],
  "integrated_summary": "..."
}
```

### PowerPoint スライド構成

1. **タイトルスライド** - テーマ・日時
2. **アジェンダ** - 5つのセッション
3. **現状分析** - 市場環境
4. **主要課題** - ギャップ情報
5. **戦略的示唆** - 深い洞察
6. **推奨アクション** - 5つの具体策
7. **実装ロードマップ** - 4段階フェーズ
8. **結論** - まとめメッセージ

## システム要件

- **Python**: 3.6 以上
- **依存パッケージ**:
  - python-pptx >= 1.0.0
  - requests >= 2.25.0
  - beautifulsoup4 >= 4.9.0
- **OS**: Windows / macOS / Linux

## インストール手順

```bash
# 1. 必要なパッケージをインストール
pip install python-pptx requests beautifulsoup4

# 2. スクリプトを実行
cd C:\Users\check\PMVault
python .\.claude\scripts\consulting-team.py "テーマ"
```

## トラブルシューティング

### Q: スクリプトが実行できない
**A**: Python と必要なパッケージをインストール：
```bash
pip install python-pptx requests beautifulsoup4
```

### Q: 内部アーカイブが検索されない
**A**: 以下を確認：
- `40.archive/` ディレクトリが存在するか
- 各プロジェクトに `Overview.md` があるか
- テーマキーワードが Overview.md に含まれているか

### Q: PPT生成に失敗した
**A**: `python-pptx` がインストールされているか確認：
```bash
pip install python-pptx
```
失敗時は Markdown レポートで代替されます。

## カスタマイズ

### Web検索APIの統合
`ExternalResearchAgent._web_search()` メソッドを編集して、
Google Custom Search や Bing Search API と連携できます。

### アーカイブパスの変更
`InternalResearchAgent` のコンストラクタで `archive_path` を指定：
```python
agent = InternalResearchAgent(archive_path="C:\\custom\\path")
```

### PPTデザインの変更
`PPTDesignerAgent` の各スライド生成メソッドで、
配色、フォント、レイアウトをカスタマイズできます。

## 機能

### 主な機能

- **自動リサーチ**: Web調査 + 内部Archive検索を並行実行
- **統合分析**: 複数情報源から洞察を抽出
- **多形式出力**: Markdown + JSON + PowerPoint
- **エラー耐性**: 片方の処理失敗時も他は継続
- **日本語対応**: 日本語テーマのキーワード抽出と分析

### 出力の品質

- **主要知見**: 4項目（市場トレンド、実装パターン、統合的アプローチ、業界別差異）
- **主要課題**: 3-4項目（不足情報、実装ガイド、定量化）
- **戦略的示唆**: 4項目（戦略統合、経営層、継続投資、カスタマイズ）
- **推奨事項**: 5項目（ワークショップ、診断、ロードマップ、体制、内製化）

## 今後の改善

- [ ] 実際のWeb検索API統合
- [ ] 詳細な統計分析
- [ ] チャート・グラフ自動生成
- [ ] 複数テンプレートサポート
- [ ] HTML/PDF出力対応

## ライセンス

内部ツール・クライアントプロジェクト向け

## 作成日

2026年7月11日

## サポート

バグ報告・機能改善提案はプロジェクトマネージャーまで。

---

**バージョン**: 1.0  
**最終更新**: 2026年7月11日
