# 3Dカードジェネレータ

このプロジェクトは、画像をアップロードして3Dカードを生成するWebアプリケーションです。ユーザーは2つの画像をアップロードし、凹み深さやプレート厚みを調整して3Dモデル（STLファイル）を生成できます。

![3Dカードジェネレータのイメージ](images/image.png)

## 機能

- **画像アップロード**: ベース画像とターゲット画像をアップロード可能。
- **リアルタイムプレビュー**: アップロードした画像のプレビューを表示。
- **パラメータ調整**: 凹み深さやプレート厚みを調整可能。
- **3Dモデル生成**: STL形式の3Dモデルを生成してダウンロード。
- **プログレスバー**: 処理進捗を表示。

## 使用技術

- **フロントエンド**:
  - HTML5, CSS3
  - JavaScript (Vanilla JS)
- **バックエンド**:
  - Python (Flask)
  - ライブラリ: Pillow, NumPy, numpy-stl
- **その他**:
  - STLファイル生成ロジック

## セットアップ

### 必要条件

- Python 3.8以上
- Flask
- Pillow
- NumPy
- numpy-stl

### インストール手順

1. リポジトリをクローンします。

   ```bash
   git clone https://github.com/your-repo/3d_card_generator.git
   cd 3d_card_generator
   ```

2. 必要なPythonパッケージをインストールします。

   ```bash
   pip install -r requirements.txt
   ```

3. サーバーを起動します。

   ```bash
   python server.py
   ```

4. ブラウザで以下のURLにアクセスします。

   ```
   http://127.0.0.1:5000
   ```

## ファイル構成

```
3d_card_generator/
├── static/
│   ├── style.css       # スタイルシート
│   ├── script.js       # フロントエンドのJavaScript
├── templates/
│   ├── index.html      # メインHTMLファイル
├── server.py           # Flaskサーバー
├── requirements.txt    # 必要なPythonパッケージ
└── README.md           # このファイル
```

## 使用方法

1. **画像をアップロード**:
   - ベース画像とターゲット画像を選択します。
2. **パラメータを調整**:
   - 凹み深さとプレート厚みを入力します。
3. **生成開始**:
   - 「生成開始」ボタンを押して3Dモデルを生成します。
4. **ダウンロード**:
   - 処理が完了すると、STLファイルが自動的にダウンロードされます。

## 注意事項

- アップロードする画像は同じサイズである必要があります。


