# Adalyze（アドアライズ）
広告文に潜む詐欺的・誇張的表現をAIが評価し、危険スコアを可視化する診断ツール（無料ベータ）。

## 主な機能
- 広告文の危険スコア診断（カテゴリ考慮）
- 診断結果の保存（TinyDB / JSON）
- ログ閲覧（検索・カテゴリ/スコア/期間フィルター、ソート）
- CSV / JSON エクスポート
- 統計ページ（カテゴリ別平均、分布、推移）

## ディレクトリ構成
```txt
adalyze_dev/
├── home.py
├── utils.py
├── pages/
│   ├── fraudcheck.py
│   ├── log.py
│   └── stats.py
├── data/
│   └── result.json
├── img/
│   └── logo.svg
├── .streamlit/
│   └── config.toml
└── .env
```

##1) 依存関係
```
pip install -r requirements.txt
```

##2) 環境変数（.env）

プロジェクト直下に .env を作成し、OpenAI APIキーを設定します。
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

##3) 起動
```
streamlit run home.py
```

##注意
- 広告文に個人情報・機密情報は入力しないでください。
- 診断結果は参考情報であり、法的判断を代替するものではありません。
