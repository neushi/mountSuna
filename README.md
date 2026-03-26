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

### 実行例

スクリプトを実行すると、以下のように設定用のテキストが出力されます。

```bash
python mount_suna.py
```

**出力イメージ:**
```text
# Volume Name:                 Macintosh HD
UUID=12345678-ABCD-EFGH-IJKL-1234567890AB none auto noauto
# Volume Name:                 Data
UUID=12345678-ABCD-EFGH-IJKL-1234567890AB none auto noauto
	、、、、マウントされていないボリュームがあるだけ繰り返す、、、、
# Volume Name:                 mounted Volume - Data
#### UUID=12345678-ABCD-EFGH-IJKL-1234567890AB none auto noauto
# Volume Name:                 mounted Volume
#### UUID=12345678-ABCD-EFGH-IJKL-1234567890AB none auto noauto
	、、、、マウントされているボリュームがあるだけ繰り返す、、、、
```

### 使い方

1. スクリプトを実行し、自動マウントを防ぎたいボリュームを探します。
2. 対象ボリュームの `UUID=...` （または `#### UUID=...`）の行をコピーします。
3. `sudo vifs` を用いて fstab を開き、適当な位置に貼り付けます。
   ※ `fstab` 内に同一UUIDの行が複数ある場合は、一番上にある行が優先されます。
4. コピーした行の先頭に `#### ` がある場合はこれを削除し、必ず `UUID=...` から始まる形式にして保存します。
   ※ 先頭に `#` がついたままだとコメント行とみなされ、マウント抑止が機能しません。