const INPUT_STEP_SIZE = 0.01;
let state = {
  inputs: {
    R: 0,
    S: 0,
  },
};

function createSim() {
  console.log('Clicked createSim.');
}

function activateSim() {
  console.log('Clicked activateSim.');
  console.log(state);
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
