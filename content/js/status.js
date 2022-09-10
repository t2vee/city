window.onload = (getStatus);
document.getElementById("status").style.backgroundColor = "rgb(105, 105, 105)";
  function getStatus() {
    const requests = new XMLHttpRequest();
    if (!requests) {
      console.log('Failed to create XMLHttpRequest');
      return false;
    }
    requests.open('GET', `https://status.t2v.city/api/status-page/heartbeat/t2v`);
    requests.send();
    requests.onreadystatechange = function() {
      if (requests.readyState === XMLHttpRequest.DONE) {
        if (requests.status === 200) {
            document.getElementById("status").style.backgroundColor = "rgb(64, 192, 87)";
        } else {
            document.getElementById("status").style.backgroundColor = "rgb(255, 0, 0)";
        } 
      } else {
          document.getElementById("status").style.backgroundColor = "rgb(105, 105, 105)";
      }
    }
  }