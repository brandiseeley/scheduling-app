function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function intToHour(intHour) {
  let suffix = intHour < 12 ? 'am' : 'pm';
  let hour = intHour <= 12 ? intHour : ((intHour % 12));
  hour = hour !== 0 ? hour : 12;
  return `${hour}:00 ${suffix}`;
}

// Render Options

let form = document.querySelector('form');
const HOURS = [
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
  13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
];

HOURS.forEach(hour => {
  let label = document.createElement('LABEL');
  let text = document.createElement('SPAN');
  text.textContent = intToHour(hour);

  let input = document.createElement('INPUT');
  input.setAttribute('type', 'checkbox');

  label.appendChild(input);
  label.appendChild(text);

  form.appendChild(label);
});

// Event Listeners

form.addEventListener('submit', event => {
  event.preventDefault();
  let formData = new FormData(event.target);
  let dateFrom = formData.get('date-from');
  let dateTo = formData.get('date-to');

  createSchedule(dateFrom, dateTo);
});

async function createSchedule(dateFrom, dateTo) {
  console.log('getting csrf token');
  const csrftoken = getCookie('csrftoken');

  try {
    let response = await fetch('', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ dateFrom, dateTo })
    });
  } catch (error) {
    console.log("Error when adding availability");
    throw error;
  }
}