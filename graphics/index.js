const ROOT_URL = 'localhost:8888';
const MODEL_ID = 1;
const INPUT_STEP_SIZE = 0.01;
const RESET_STATE = {
  message: 'state',
  active: false,
  inputs: {
    R: 0,
    S: 0,
  },
};

let state = Object.assign({}, RESET_STATE);

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
    console.log('Clicked activateSim.');
    console.log(state);
  };
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
