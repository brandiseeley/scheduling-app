/* eslint-disable max-lines-per-function */
class Slot {
  constructor(ISOString) {
    this.ISOString = ISOString;
    this.id = ISOString;
    this.date = new Date(ISOString);
  }

  timeDisplay() {
    let hours = this.date.getHours();
    let minutes = this.date.getMinutes();
    let suffix = hours >= 12 ? 'pm' : 'am';
    let hoursDisplay = hours > 12 ? ((hours % 12) + 1) : hours;
    return `${hoursDisplay}:${String(minutes).padEnd(2, '0')} ${suffix}`;
  }

  dateDisplay() {
    const MONTHS = ['JAN', 'FEB', 'MAR', 'APR',
      'MAY', 'JUN', 'JUL', 'AUG',
      'SEP', 'OCT', 'NOV', 'DEC'];

    return `${MONTHS[this.date.getMonth()]} ${this.date.getDate()}`;
  }
}

class SlotCluster {
  constructor(slots, isMain, owner) {
    this.slots = slots.map(ISOString => new Slot(ISOString));
    this.owner = owner;
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
  localDatesMap() {
    let datesMap = {};
    this.slots.forEach(slot => {
      let dateString = slot.dateDisplay();
      let timeString = slot.timeDisplay();
      if (datesMap.hasOwnProperty(dateString)) {
        datesMap[dateString].push(timeString);
      } else {
        datesMap[dateString] = [timeString];
      }
    });
    return datesMap;
  }

  // Returns an object with time strings in the local time
  // as keys and slots associated with that time of day
  // in an array value
  localTimesMap() {
    let timesMap = {};
    this.slots.forEach(slot => {
      let timeString = slot.timeDisplay();
      if (!(timeString in timesMap)) {
        timesMap[timeString] = [slot];
      } else {
        timesMap[timeString].push(slot);
      }
    });

    return timesMap;
  }
}

async function getScheduleData() {
  let response = await fetch('data/31');
  let data = await response.json();
  console.log(data);
  return data;
}

function renderMainSchedule(mainCluster) {
  let datesMap = mainCluster.localDatesMap();
  let timesMap = mainCluster.localTimesMap();

  let daysHeader = document.querySelector('#days');
  for (let dateString of Object.keys(datesMap)) {
    let head = document.createElement('TH');
    head.textContent = dateString;
    daysHeader.appendChild(head);
  }

  let tableBody = document.querySelector('tbody');
  for (let [timeString, timesArray] of Object.entries(timesMap)) {
    let row = document.createElement('TR');
    timesArray.forEach(slot => {
      let tableData = document.createElement('TD');
      tableData.textContent = timeString;
      tableData.dataset.timeslot = slot.id;
      row.appendChild(tableData);
    });
    tableBody.appendChild(row);
  }
}

function renderUserAvailability(userClusters) {
  userClusters.forEach(userCluster => {
    console.log('Working on user cluster for:, ', userCluster.owner);
    console.log(userCluster);

    userCluster.slots.forEach(slot => {
      let matchingTableData = document.querySelector(`[data-timeslot="${slot.id}"]`);
      if (matchingTableData) {
        matchingTableData.textContent += userCluster.owner;
      } else {
        throw new Error("User cluster contained time stamp not present in main schedule");
      }
    });
  });
}

async function renderSchedule() {
  let scheduleData = await getScheduleData();

  let mainCluster = new SlotCluster(scheduleData.base_cluster.slots, true);
  let userClusters = scheduleData.user_clusters.map(clusterObj => {
    return new SlotCluster(clusterObj.slots, false, clusterObj.owner);
  });

  renderMainSchedule(mainCluster);
  renderUserAvailability(userClusters);
}

renderSchedule();