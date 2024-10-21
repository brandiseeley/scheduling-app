/* eslint-disable max-statements */
/* eslint-disable max-lines-per-function */
/*
1. Create a basic skeleton to be sent as the original HTML file we get.

2. Write JS that renders the main schedule (for now just use one)
  - Fetch schedule data asynchronously from server
  - Render it into the table with proper dates and times

2. Write JS that renders each users availability
  - Fetch data asynchronously (Should already have it)
  - Iterate through each existing user and add their names
    to the appropriate schedule
*/

async function getScheduleData() {
  let response = await fetch('data/24');
  let data = await response.json();
  console.log(data);
  return data;
}

function dateStringId(date) {
  return date.toISOString();
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
    for (let i = 0; i < days.length; i++) {
      let jsTimeDay = new Date(days[i]);
      let jsTimeHours = new Date(time);
      let hours = jsTimeHours.getHours();
      let minutes = jsTimeHours.getMinutes();
      jsTimeDay.setHours(hours);
      jsTimeDay.setMinutes(minutes);
      let jsTime = jsTimeDay;

      let tableData = document.createElement('TD');

      console.log(tableData);
      let suffix = hours >= 12 ? 'pm' : 'am';
      tableData.textContent = `${hours}:${String(minutes).padEnd(2, '0')} ${suffix}`;

      tableData.dataset.timeslot = dateStringId(jsTime);
      row.appendChild(tableData);
    }
    tableBody.appendChild(row);
  });
}

function renderUserAvailability(userUnions) {
  userUnions.forEach(union => {
    union.slots.forEach(timeString => {
      let jsTime = new Date(timeString);
      let timeId = dateStringId(jsTime);
      let matchingTableData = document.querySelector(`[data-timeslot="${timeId}"]`);
      if (matchingTableData) {
        matchingTableData.textContent += 'Brandi';
      } else {
        console.log("No matching TD for this time: ", timeId);
      }
    });
  });
}


async function renderSchedule() {
  let scheduleData = await getScheduleData();

  renderDays(scheduleData.days);
  renderTimes(scheduleData.hour_samples, scheduleData.days);
  renderUserAvailability(scheduleData.user_unions);
}

renderSchedule();