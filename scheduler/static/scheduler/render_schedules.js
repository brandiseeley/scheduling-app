/*

We want a single page application.
As such, everything will be rendered, right now, with JS.
I set up Django templates, but that's not really what we want. Send a basic
skeleton of a schedule with some ids to grab onto, use JS and
get info from server to render the schedules.

1. Create a basic skeleton to be sent as the original HTML file we get.

2. Write JS that renders the main schedule (for now just use one)
  - Fetch schedule data asynchronously from server
  - Render it into the table with proper dates and times

2. Write JS that renders each users availability
  - Fetch data asynchronously (Should already have it)
  - Iterate through each existing user and add their names
    to the appropriate schedule

Problem: This all happens on the front end. The server would be very basic.
Just for storing dates/times, and schedules. All rendering would happen with
JS on the front end.

*/

async function getScheduleData() {
  let response = await fetch('data/24');
  let data = await response.json();
  console.log(data);
  return data;
}

function renderDays(days) {
  let daysHeader = document.querySelector('#days');
  days.forEach(day => {
    let head = document.createElement('TH');
    head.textContent = day;
    daysHeader.appendChild(head);
  });
}

function renderTimes(hourSamples, days) {
  let tableBody = document.querySelector('tbody');
  hourSamples.forEach(time => {
    let row = document.createElement('TR');
    for (let _ = 0; _ < days.length; _++) {
      let jsTime = new Date(time);

      let tableData = document.createElement('TD');
      let hours = jsTime.getHours();
      let minutes = jsTime.getMinutes();
      let suffix = hours >= 12 ? 'pm' : 'am';
      tableData.textContent = `${hours}:${String(minutes).padEnd(2, '0')} ${suffix}`;
      row.appendChild(tableData);
    }
    tableBody.appendChild(row);
  });
}

async function renderSchedule() {
  let scheduleData = await getScheduleData();

  renderDays(scheduleData.days);
  renderTimes(scheduleData.hour_samples, scheduleData.days);
}

renderSchedule();