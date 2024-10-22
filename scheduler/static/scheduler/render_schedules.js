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

class SlotCluster {
  constructor(slots, isMain) {
    this.slots = slots.map(ISOString => new Date(ISOString));
  }

  earliest() {
    return this.slots[0];
  }

  latest() {
    return this.slots[this.slots.length - 1];
  }

  // Return an object with date strings in the local time
  // as keys and times that exist within that local date
  // in an array value
  localDatesAndTimes() {
    const MONTHS = ['JAN', 'FEB', 'MAR', 'APR',
      'MAY', 'JUN', 'JUL', 'AUG',
      'SEP', 'OCT', 'NOV', 'DEC'];
    let datesMap = {};
    this.slots.forEach(slot => {
      let dateString = `${MONTHS[slot.getMonth()]} ${slot.getDate()}`;
      let timeString = `${slot.getHours()}:${slot.getMinutes()}`;
      if (datesMap.hasOwnProperty(dateString)) {
        datesMap[dateString].push(timeString);
      } else {
        datesMap[dateString] = [timeString];
      }
    });
    return datesMap;
  }

  localTimes() {
    return this.slots.map(slot => {
      return `${slot.getHours()}:${slot.getMinutes()}`;
    });
  }
}

async function getScheduleData() {
  let response = await fetch('data/31');
  let data = await response.json();
  console.log(data);
  return data;
}

// Date String ID should always be in UTC
function dateStringId(date) {
  return date.toISOString();
}

function renderMainSchedule(datesMap) {
  let daysHeader = document.querySelector('#days');
  for (let [dateString, timesArray] of Object.entries(datesMap)) {
    let head = document.createElement('TH');
    head.textContent = dateString;
    daysHeader.appendChild(head);
  }
  // days.forEach(day => {
  //   let head = document.createElement('TH');
  //   head.textContent = day;
  //   daysHeader.appendChild(head);
  // });
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
      tableData.textContent = `${hours > 12 ? hours % 12 : hours}:${String(minutes).padEnd(2, '0')} ${suffix}`;

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
        matchingTableData.textContent += union.owner;
        console.log('Found matching Time: ', matchingTableData.dataset.timeslot, timeId);
      } else {
        console.log("No matching TD for this time: ", timeId);
      }
    });
  });
}


async function renderSchedule() {
  let scheduleData = await getScheduleData();

  let mainCluster = new SlotCluster(scheduleData.base_cluster.slots, true);
  console.log("Dates:");
  console.log(mainCluster.localDatesAndTimes());
  let userClusters = scheduleData.user_clusters.map(clusterObj => {
    return new SlotCluster(clusterObj.slots, false);
  });

  console.log(mainCluster);
  console.log(userClusters);

  renderMainSchedule(mainCluster.localDatesAndTimes());
  // renderTimes(scheduleData.hour_samples, scheduleData.days);
  // renderUserAvailability(scheduleData.user_unions);
}

renderSchedule();