const ROOT_URL = 'process-dynamics-engine.herokuapp.com';
const MODEL_ID = 1;
const BASE_PURITY = 0.5;
const FEED_RANGE = [-1, 1];
const PURITY_RANGE = [0, 1];
const ACTION_RANGE = [-0.1, 0.1];
const FEED_STEP_SIZE = 0.05;
const ACTION_STEP_SIZE = 0.01;
const TIME_STEP_SIZE_MS = 1000;
const RESET_STATE = {
  status: 'frontend',
  message: 'current state',
  active: false,
  inputs: {
    R: 0,
    S: 0,
    F: 0,
  },
};
const RESET_CHARTS = {
  x_D: null,
  x_B: null,
  R: null,
  S: null,
  F: null,
};
const RESET_HISTORY = {
  x_D: [{label: 'Distillate purity', values: []}],
  x_B: [{label: 'Bottoms purity', values: []}],
  R: [{label: 'Reflux flow rate', values: []}],
  S: [{label: 'Steam flow rate', values: []}],
  F: [{label: 'Feed flow rate', values: []}],
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
    history.F[0].values.push({time: time - i, y: 0});
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
  charts.F = new Epoch.Time.Line({
    el: '#feed_chart',
    data: history.F,
    range: FEED_RANGE,
    axes: ['left', 'right', 'bottom'],
  });
}

function timeoutP(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function send(ws, data) {
  const text = JSON.stringify(data);
  console.log(`to backend, ${data.status}: ${data.message}`);
  console.log(data);
  ws.send(text);
}

function receive(text) {
  const data = JSON.parse(text);
  console.log(`from backend, ${data.status}: ${data.message}`);
  console.log(data);
  return data;
}

async function createSim() {
  const response = await fetch(
      `http://${ROOT_URL}/models/${MODEL_ID}`, {method: 'POST'});
  let socket_id;
  try {
    const json = await response.json();
    receive(JSON.stringify({
      'status': 'success',
      'message': 'created new simulation',
      'sim_id': json.sim_id,
      'model_id': json.model_id,
      'socket_id': json.socket_id,
    }));
    socket_id = json.socket_id;
  } catch (e) {
    receive(JSON.stringify({
      'status': 'error',
      'message': e,
    }));
  }
  document.getElementById('socket_id').value = socket_id;
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
    switch (data.status) {
    case 'inactive':
      send(ws, {
        status: 'activate',
        message: `activate simulation with socket ${socket_id}`,
      });
      break;
    case 'active':
      state.active = true;
      if (data.outputs) {
        charts.x_D.push([{time, y: BASE_PURITY + data.outputs.x_D}]);
        charts.x_B.push([{time, y: BASE_PURITY + data.outputs.x_B}]);
        charts.R.push([{time, y: state.inputs.R}]);
        charts.S.push([{time, y: state.inputs.S}]);
        charts.F.push([{time, y: state.inputs.F}]);
      }
      break;
    }
  }
}

function incrementInput(element_id, input, step) {
  document.getElementById(element_id).addEventListener('click', () => {
    state.inputs[input] += step;
  });
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('create').addEventListener('click', createSim);
  document.getElementById('activate').addEventListener('click', activateSim);
  incrementInput('reflux_up', 'R', ACTION_STEP_SIZE);
  incrementInput('reflux_down', 'R', -ACTION_STEP_SIZE);
  incrementInput('steam_up', 'S', ACTION_STEP_SIZE);
  incrementInput('steam_down', 'S', -ACTION_STEP_SIZE);
  incrementInput('feed_up', 'F', FEED_STEP_SIZE);
  incrementInput('feed_down', 'F', -FEED_STEP_SIZE);
});
