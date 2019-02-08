const ROOT_URL = 'process-dynamics-engine.herokuapp.com';
const MODEL_ID = 1;
const BASE_PURITY = 0.5;
const PURITY_RANGE = [0, 1];
const ACTION_RANGE = [-0.1, 0.1];
const ACTION_STEP_SIZE = 0.01;
const TIME_STEP_SIZE_MS = 500;
const RESET_STATE = {
  message: 'state',
  active: false,
  inputs: {
    R: 0,
    S: 0,
  },
};
const RESET_CHARTS = {
  x_D: null,
  x_B: null,
  R: null,
  S: null,
};
const RESET_HISTORY = {
  x_D: [{label: 'Distillate purity', values: []}],
  x_B: [{label: 'Bottoms purity', values: []}],
  R: [{label: 'Reflux flow rate', values: []}],
  S: [{label: 'Steam flow rate', values: []}],
};

let state;
let charts;
let history;

function resetGlobalVariables() {
  state = Object.assign({}, RESET_STATE);
  charts = Object.assign({}, RESET_CHARTS);
  history = Object.assign({}, RESET_HISTORY);
  const time = new Date().getTime() / 1000;
  for (let i = 60; i >= 0; i--) {
    history.x_D[0].values.push({time: time - i, y: BASE_PURITY});
    history.x_B[0].values.push({time: time - i, y: BASE_PURITY});
    history.R[0].values.push({time: time - i, y: 0});
    history.S[0].values.push({time: time - i, y: 0});
  }
  charts.x_D = new Epoch.Time.Line({
    el: '#distillate_chart',
    data: history.x_D,
    range: PURITY_RANGE,
    axes: ['left', 'right', 'top', 'bottom'],
  });
  charts.x_B = new Epoch.Time.Line({
    el: '#bottoms_chart',
    data: history.x_B,
    range: PURITY_RANGE,
    axes: ['left', 'right', 'top', 'bottom'],
  });
  charts.R = new Epoch.Time.Line({
    el: '#reflux_chart',
    data: history.R,
    range: ACTION_RANGE,
    axes: ['left', 'right', 'bottom'],
  });
  charts.S = new Epoch.Time.Line({
    el: '#steam_chart',
    data: history.S,
    range: ACTION_RANGE,
    axes: ['left', 'right', 'bottom'],
  });
}

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
  resetGlobalVariables();
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
    const time = new Date().getTime() / 1000;
    switch (data.message) {
    case 'inactive':
      send(ws, {message: 'activate'});
      break;
    case 'active':
      state.active = true;
      if (data.outputs) {
        charts.x_D.push([{time, y: BASE_PURITY + data.outputs.x_D}]);
        charts.x_B.push([{time, y: BASE_PURITY + data.outputs.x_B}]);
        charts.R.push([{time, y: state.inputs.R}]);
        charts.S.push([{time, y: state.inputs.S}]);
      }
      break;
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('create').addEventListener('click', createSim);
  document.getElementById('activate').addEventListener('click', activateSim);
  document.getElementById('reflux_up').addEventListener('click', () => {
    state.inputs.R += ACTION_STEP_SIZE;
  });
  document.getElementById('reflux_down').addEventListener('click', () => {
    state.inputs.R -= ACTION_STEP_SIZE;
  });
  document.getElementById('steam_up').addEventListener('click', () => {
    state.inputs.S += ACTION_STEP_SIZE;
  });
  document.getElementById('steam_down').addEventListener('click', () => {
    state.inputs.S -= ACTION_STEP_SIZE;
  });
});
