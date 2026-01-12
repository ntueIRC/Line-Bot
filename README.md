 如果你是第一次下載專案或是在新電腦上開發，請依序執行：
git clone [https://github.com/ntueIRC/Line-Bot.git](https://github.com/ntueIRC/Line-Bot.git)
cd Line-Bot

初始化 (第一次要跑而已)
git init

建立並切換到新分支
git checkout -b <你的名字>

檢查狀態
git status

格式化後暫存變動
black .
isort .
git add .

提交commit
git commit -m "feat: 描述你的更新內容"

推送到遠端 如果是該分支第一次 Push，請使用 -u (之後打git push origin <你的名字>即可)
git push -u origin <你的名字>

建議使用 .env 管理 機密資料（記得將 .env 加入 .gitignore）
