// 現在の時刻を表示する関数
function updateClock() {
    const now = new Date(); // 現在の日付と時刻を取得
    const hours = String(now.getHours()).padStart(2, '0'); // 時
    const minutes = String(now.getMinutes()).padStart(2, '0'); // 分
    const seconds = String(now.getSeconds()).padStart(2, '0'); // 秒

    // 時計を更新する
    document.getElementById('clock').textContent = `${hours}:${minutes}:${seconds}`;
}

// 時計を1秒ごとに更新
setInterval(updateClock, 1000);

// 最初の表示
updateClock();
