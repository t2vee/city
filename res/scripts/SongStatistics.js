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
      console.error('There was a problem with the fetch:', error);
    });
}

songtab.addEventListener("click", function() {
  // ... existing code
  if (!songDataLoaded) {
    fetchSongData();
  }
});
