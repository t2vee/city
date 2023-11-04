function colour(num) {
  if (num < 500) {
    return 'limegreen';
  } else if (num < 1000) {
    return 'orange';
  } else {
    return 'red';
  }
}

window.addEventListener('load', (event) => {
  const navigationTiming = performance.getEntriesByType('navigation')[0];
  const pageLoadTime = Math.round(navigationTiming.domComplete - navigationTiming.startTime);
  if (pageLoadTime >= 0) {

    document.getElementById("loadtime").innerHTML += ` Page Load Time: <span style="color: ${colour(pageLoadTime)}">${pageLoadTime}ms</span>`;
  } else {
    document.getElementById("loadtime").innerHTML += 'Page: Timing data not available';
  }
});