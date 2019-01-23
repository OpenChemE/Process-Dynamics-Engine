const ROOT_URL = 'localhost:8888';
const MODEL_ID = 1;
const INPUT_STEP_SIZE = 0.01;
const TIME_STEP_SIZE_MS = 500;
const RESET_STATE = {
  message: 'state',
  active: false,
  inputs: {
    R: 0,
    S: 0,
  },
};

let state = Object.assign({}, RESET_STATE);

function timeoutP(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function send(ws, obj) {
  const message = JSON.stringify(obj);
  console.log(`Sent to backend: ${message}`);
  ws.send(message);
}

function receive(message) {
  console.log(`Received from backend: ${message}`);
  return JSON.parse(message);
}

async function createSim() {
  const response = await fetch(
      `http://${ROOT_URL}/models/${MODEL_ID}`, {method: 'POST'});
  const json = await response.json();
  document.getElementById('socket_id').value = json.socket_id;
}

async function activateSim() {
  const socket_id = document.getElementById('socket_id').value;
  const ws = new WebSocket(`ws://${ROOT_URL}/${socket_id}`);
  state = Object.assign({}, RESET_STATE);
  ws.onopen = async () => {
    while (true) {
      await timeoutP(TIME_STEP_SIZE_MS);
      if (state.active) {
        send(ws, state);
      }
    }
  };
  ws.onmessage = (e) => {
    const data = receive(e.data);
    switch (data.message) {
    case 'inactive':
      send(ws, {message: 'activate'});
      break;
    case 'active':
      state.active = true;
      break;
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('create').addEventListener('click', createSim);
  document.getElementById('activate').addEventListener('click', activateSim);
  document.getElementById('reflux_up').addEventListener('click', () => {
    state.inputs.R += INPUT_STEP_SIZE;
  });
  document.getElementById('reflux_down').addEventListener('click', () => {
    state.inputs.R -= INPUT_STEP_SIZE;
  });
  document.getElementById('steam_up').addEventListener('click', () => {
    state.inputs.S += INPUT_STEP_SIZE;
  });
  document.getElementById('steam_down').addEventListener('click', () => {
    state.inputs.S -= INPUT_STEP_SIZE;
  });
});
