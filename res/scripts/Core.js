document.addEventListener('DOMContentLoaded', (event) => {
  setTimeout(function() {
    document.getElementById('cacheStatus').textContent = ' Page Cached';
    document.getElementById('cacheStatus').style.color = 'green';
    var spinner = document.getElementById('cacheSpinner');
    if (spinner) {
      spinner.style.display = 'none';
      document.getElementById('cacheTick').style.display = 'block';
    }
  }, 3000);
});
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

    document.getElementById("loadtime").innerHTML += ` Page Load Time:&#32;<span style="margin-left: 5px;color: ${colour(pageLoadTime)}"> ${pageLoadTime}ms</span>`;
  } else {
    document.getElementById("loadtime").innerHTML += 'Page: Timing data not available';
  }
});

document.addEventListener("DOMContentLoaded", function() {
  const songtab = document.getElementById("songtab");
  const albumtab = document.getElementById("albumtab");
  const slideout = document.getElementById("slideout");
  const songcontent = document.getElementById("songcontent");
  const albumcontent = document.getElementById("albumcontent");
  const wrap = document.getElementById("wrap");

  let activeTab = '';

  function toggleContent(tab) {
    songcontent.style.display = "none";
    albumcontent.style.display = "none";
    if (tab === 'song') {
      songcontent.style.display = "block";
    } else {
      albumcontent.style.display = "block";
    }
  }

  songtab.addEventListener("click", function() {
    if (activeTab === 'song') {
      wrap.classList.remove("slideout-active");
      activeTab = '';
    } else {
      wrap.classList.add("slideout-active");
      activeTab = 'song';
      toggleContent('song');
    }
  });

  albumtab.addEventListener("click", function() {
    if (activeTab === 'album') {
      wrap.classList.remove("slideout-active");
      activeTab = '';
    } else {
      wrap.classList.add("slideout-active");
      activeTab = 'album';
      toggleContent('album');
    }
  });
});

function formatDateString(dateString) {
  const date = new Date(dateString);
  const options = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  };
  return date.toLocaleDateString('en-AU', options);
}

function lol(num) {
  if (num < 100) {
    return '😴';
  } else if (num < 400) {
    return '😁';
  } else if (num < 800) {
    return '🤪';
  } else {
    const emojis = ['💀', '🤡'];
    const randomIndex = Math.floor(Math.random() * emojis.length);
    return emojis[randomIndex];
  }
}

function lol2(dateString) {
  const date = new Date(dateString);
  const hour = date.getHours();

  if (hour >= 6 && hour < 18) {
    return '🌞';
  } else {
    return '🌑';
  }
}

let songDataLoaded = false;

function fetchSongData() {
  // Show the spinner
  document.getElementById("spinner").style.display = "block";
  const tempElement = document.getElementById("songtab");
  let trackUrl = tempElement.dataset.url;
  let sanitisedTrackUrl = trackUrl.split("/").pop()
  fetch(`/gateway/SpotifyStatsRelay/Track?track_id=${sanitisedTrackUrl}`)
    .then(response => response.json())
    .then(data => {
      json_data = JSON.parse(data);
      document.getElementById("spinner").style.display = "none";
      let songContent = document.getElementById("songcontent");
      songContent.innerHTML = `<h1>Song Statistics</h1>`;
      songContent.innerHTML += `<hr class="sl">`
      songContent.innerHTML += `<h4>I've listened to this track:</h4>`;
      songContent.innerHTML += `<h3>${json_data.total_count} times ${lol(json_data.total_count)}</h3>`;
      songContent.innerHTML += `<hr class="sl">`
      const firstPlayedFormatted = formatDateString(json_data.first_played);
      songContent.innerHTML += `<h4>I've first listened to this track on the: </h4>`;
      songContent.innerHTML += `<h3>${firstPlayedFormatted} ${lol2(firstPlayedFormatted)}</h3>`;
      songContent.innerHTML += `<hr class="sl">`
      let bestPeriods = json_data.best_period;
        bestPeriods.sort((a, b) => b.count - a.count);

        songContent.innerHTML += '<h3>Top two months I listened to ' + json_data.track_name + '</h3>';
        for (let i = 0; i < Math.min(2, bestPeriods.length); i++) {
          let period = bestPeriods[i];
          let year = period._id.year;
          let month = new Date(Date.UTC(year, period._id.month - 1)).toLocaleString('default', { month: 'long' });
          let count = period.count;
          let total = period.total;

          let percentage = ((count / total) * 100).toFixed(2);

          songContent.innerHTML += `
            <p>${month} ${year}<br>
            ${count} times (${percentage}% of total time)</p>
          `;
        }
      songContent.innerHTML += `<hr class="sl">`
      songDataLoaded = true;
    })
    .catch(error => {
      document.getElementById("spinner").style.display = "none";
      let songContent = document.getElementById("songcontent");
      songContent.innerHTML = `<h1>Oops!</h1>`;
      songContent.innerHTML += `<hr class="sl">`
      songContent.innerHTML += `<h3>Sorry! Stats for this song are currently unavailable 😞</h3>`;
    });
}
function convertTimeToMilliseconds(time) {
    const [minutes, seconds] = time.split(":").map(Number);
    return (minutes * 60000) + (seconds * 1000);
}
songtab.addEventListener("click", function() {
  if (!songDataLoaded) {
    fetchSongData();
  }
});
setInterval(increaseProgressBar, 1000);
function increaseProgressBar() {
    const songDuration = document.getElementById("songDuration");
    let totalDuration = convertTimeToMilliseconds(songDuration.getAttribute("data-duration"));
    const progress = document.getElementById("progress");
    const progress_time_element = document.getElementById("time_start");

    let currentValue = parseFloat(progress.getAttribute("value")) || 0;
    let newValue = currentValue + 1000;
        if (newValue >= totalDuration && totalDuration > 0) {
        console.log("song finished reloading page...");
        window.location.reload();
    }
    progress.setAttribute("value", newValue);
    progress.setAttribute("value", newValue);
    let minutes = Math.floor(newValue / 60000);
    let seconds = ((newValue % 60000) / 1000).toFixed(0);
    let finalTime = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    progress_time_element.textContent = finalTime;
}