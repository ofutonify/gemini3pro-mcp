# Gemini MCP Server for Claude Desktop

Claude DesktopからGemini 3 Proに質問できるようにするMCPサーバー。

## 必要なもの

- Python 3.10以上
- Gemini APIキー（有料ティア必要）

## セットアップ

### 1. Pythonライブラリをインストール

```bash
pip install google-genai
```

### 2. ファイルを配置

`server.py` と `requirements.txt` を任意のフォルダに配置。
例: `D:\mcp\gemini-mcp\`

### 3. Gemini APIキーを取得

1. [Google AI Studio](https://aistudio.google.com/apikey) にアクセス
2. 「APIキーを作成」をクリック
3. キーをコピー

### 4. Claude Desktop設定に追加

`claude_desktop_config.json` を編集：

**ファイルの場所：**
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`

**追記内容：**
```json
{
  "mcpServers": {
    "gemini": {
      "command": "python",
      "args": ["D:\\mcp\\gemini-mcp\\server.py"],
      "env": {
        "GEMINI_API_KEY": "ここにAPIキーを貼る"
      }
    }
  }
}
```

※ 他のMCPサーバーがある場合は `mcpServers` 内に追加

### 5. Claude Desktopを再起動

設定を反映するため、Claude Desktopを完全に終了して再起動。

## 使い方

Claude Desktopで：
- 「Geminiにこれ聞いて：〇〇」
- 「Geminiの意見も聞きたい」
- 「ask_geminiでこの質問を投げて」

## モデル指定

`gemini-3-pro-preview`

## トラブルシューティング

**ツールが表示されない場合：**
- Claude Desktopを完全に再起動（タスクトレイからも終了）
- JSONの文法エラーを確認

**APIエラーが出る場合：**
- APIキーが正しいか確認
- [Google AI Studio](https://aistudio.google.com/) でキーが有効か確認
