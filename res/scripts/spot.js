setInterval(increaseProgressBar, 1000);
function increaseProgressBar() {
    const progress = document.getElementById("progress");
    const progress_time_element = document.getElementById("time_start");
    let currentValue = parseFloat(progress.getAttribute("value")) || 0;
    let newValue = currentValue + 1000;
    progress.setAttribute("value", newValue);
    progress.setAttribute("value", newValue);
    let minutes = Math.floor(newValue / 60000);
    let seconds = ((newValue % 60000) / 1000).toFixed(0);
    let finalTime = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    progress_time_element.textContent = finalTime;
}