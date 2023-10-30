window.addEventListener('load', (event) => {
  const navigationTiming = performance.getEntriesByType('navigation')[0];
  const pageLoadTime = Math.round(navigationTiming.domComplete - navigationTiming.startTime);
  if (pageLoadTime >= 0) {

    document.getElementById("loadtime").innerText += ` Page Load Time: ${pageLoadTime} ms`;
  } else {
    document.getElementById("loadtime").innerHTML += 'Page: Timing data not available';
  }
});