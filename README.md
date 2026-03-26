# mountSuna　マウントすな!
Mac, quit auto-mounting my volumes!

# macが勝手にボリュームをマウントしないようにする

## 1. fstabで設定
不要なボリュームをマウントさせないようにするにはfstabに設定を記述します。

## 2. 安全な編集方法
fstabを編集する際は以下のコマンドを使用します：
    sudo vifs

## 3. ボリューム情報取得コマンド（Pythonスクリプト）

以下の `mount_suna.py` スクリプトを使用することで、`fstab` にそのまま貼り付けられる形式でボリューム一覧を取得できます。メンテナンスしやすく、出力も見やすく整形されます。

### 実行準備

リポジトリ内の `mount_suna.py` に実行権限を付与します（初回のみ）：
```bash
chmod +x mount_suna.py
```

### 実行例

スクリプトを実行すると、以下のように設定用のテキストが出力されます。

```bash
./mount_suna.py
```

**出力イメージ:**
```text
# **********
# Volume Name: Macintosh HD
#### Mounted: Yes
# UUID=12345678-ABCD-EFGH-IJKL-1234567890AB none auto noauto
# **********
```

### 使い方

1. スクリプトを実行し、自動マウントを防ぎたいボリュームを探します。
2. 対象ボリュームの出力にある `UUID=...` から始まる行をコピーします。
3. `sudo vifs` を用いて fstab を開き、末尾に貼り付けます。
4. コピーした行の先頭にある `# ` を削除して保存します。