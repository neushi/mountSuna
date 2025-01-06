# mountSuna　マウントすな!
Mac, quit auto-mounting my volumes!

# macが勝手にボリュームをマウントしないようにする

## 1. fstabで設定
不要なボリュームをマウントさせないようにするにはfstabに設定を記述します。

## 2. 安全な編集方法
fstabを編集する際は以下のコマンドを使用します：
    sudo vifs

## 3. ボリューム情報取得コマンド
### コマンド
```bash
diskutil info -all | grep -e 'Volume UUID' -e 'Volume Name:' -e 'APFS Snapshot UUID:' -e 'Mounted:' -e '\*\*\*\*\*\*'| sed 's/^/#/' | sed '/Mounted: *Yes/s/^# */####/' | sed '/Volume UUID:/s/^# */# /' | sed 's/Volume UUID: *\(.*\)/UUID=\1 none auto noauto/'
```

### コマンドの詳細説明
分解すると以下のようになります：

1. ボリューム情報の取得：
```bash
diskutil info -all | grep -e 'Volume UUID' -e 'Volume Name:' -e 'APFS Snapshot UUID:' -e 'Mounted:' -e '\*\*\*\*\*\*'
```

2. 行頭に#を追加：
```bash
sed 's/^/#/'
```

3. マウント済みの項目を####でマーク：
```bash
sed '/Mounted: *Yes/s/^# */####/'
```

4. UUID行の整形：
```bash
sed '/Volume UUID:/s/^# */# /'
```

5. fstab形式へ変換：例えば、
   Volume UUID: 12345678-1234-1234-1234-123456789012 を 
   UUID=12345678-1234-1234-1234-123456789012 none auto noauto に変換します。

```bash
sed 's/Volume UUID: *\(.*\)/UUID=\1 none auto noauto/'
```

