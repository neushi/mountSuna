# macが勝手にボリュームをマウントしないようにする

## 1. fstabで設定
不要なボリュームをマウントさせないようにするにはfstabに設定を記述します。

## 2. 安全な編集方法
fstabを編集する際は以下のコマンドを使用します：
    sudo vifs

## 3. ボリューム情報取得スクリプト
### スクリプト全文
diskutil info -all|grep -e 'Volume UUID' -e 'Volume Name:' -e 'APFS Snapshot UUID:' -e 'Mounted:' | sed 's/^/#/' | sed '/Mounted: *Yes/s/^# */### /' | sed '/Volume Name:/s/^# */#-------- /' | sed '/Volume UUID:/s/^# */# /' | sed 's/Volume UUID: *\(.*\)/#UUID=\1 none auto noauto/'

### スクリプトの機能
1. システム上の全ボリューム情報を取得
2. 必要な情報（UUID、ボリューム名、マウント状態）のみを抽出
3. fstabで使用できる形式に整形
4. マウント済みのボリュームを見やすく表示
5. 結果をコメント形式で出力し、そのまま参考にできるように

### コマンドの詳細説明
スクリプトを分解すると以下のようになります：

1. ボリューム情報の取得：
    diskutil info -all|grep -e 'Volume UUID' -e 'Volume Name:' -e 'APFS Snapshot UUID:' -e 'Mounted:'

2. 行頭に#を追加：
    sed 's/^/#/'

3. マウント済みの項目を###でマーク：
    sed '/Mounted: *Yes/s/^# */### /'

4. ボリューム名の行を#--------でマーク：
    sed '/Volume Name:/s/^# */#-------- /'

5. UUID行の整形：
    sed '/Volume UUID:/s/^# */# /'

6. fstab形式へ変換：
    sed 's/Volume UUID: *\(.*\)/#UUID=\1 none auto noauto/'
