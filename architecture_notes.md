# Design Requirements
1. Python control simulation server (Process Dynamics Engine, PDE)
2. Worker nodes for actual calculations. Started, stopped and controlled by the Engine
3. Front-End Graphics and real-time communication with the Engine (d3.js, Websockets, React)
4. Data Historian (Time series database, influx DB)

# Details
1. Server will contain multiple Models (Distillation, Ethylene Oxidation etc.). Each model shall be identified by a unique Model ID.
2. User should be able to spin up a Simulation and choose the desired Model using either the Graphics or directly from the API.
3. Each Simulation will have a unique Simulation ID and be independent from one another. Simulations will live in Worker nodes.
4. Users will be able to access Simulations from their unique ID. The Engine shall keep a record of all running simulations and their IDs.
5. Users will be able to interact with a Simulation from the Graphics or the API by talking to the Engine.
6. Simulation shall last a finite amount of time (i.e. 24 hours). The Worker node will terminate upon completion of Simulation and inform the Engine.
7. The Model shall define a list of Tags (inputs and outputs). The Simulation will take in Input Tags from the Server, U(t) = u_1(t), u_2(t), ..., u_n(t) and send out Output Tags to the Server, Y(t) = y_1(t), y_2(t), ..., y_n(t), whenever they are requested.
8. Each Model shall have its own corresponding Graphics page. There shall be a one-to-one relationship between Tags in the Graphics and Tags in the Model.
9. The Engine shall ping active Worker nodes for all process outputs, Y(t) and send it to all Users at a defined Sample Time.
10. The Engine shall send all user control Actions, U(t) to active Worker nodes whenever an Action is received from the Graphics.
11. The Engine shall also push all received Inputs and Outputs to the Data Historian at the defined Sample Time.

# Redis Queue Background Workers
Once a user spins up a simulation, the PDE will receive a request to perform a long-running calculation to simulate the transfer function (or state-space representation). This is best achieved by offloading the calculation to a background Worker using Redis Queue (RQ) to prevent blocking the main server.

This is scalable. More workers can be spawned if we have more background tasks accumulated.

The Engine shall talk to the active background workers periodically to get the latest process output y(t) and send control actions u(t) to the workers whenever they are received.

Read https://timber.io/blog/background-tasks-in-python-using-task-queues/

Also find out what's the difference between Threading and Multiprocessing https://timber.io/blog/multiprocessing-vs-multithreading-in-python-what-you-need-to-know/

# Process Dynamics Engine
Since the actual simulations have been offloaded to background workers, the job of the PDE is greatly simplified. The PDE will serve as a middleman between the Users, the Data Historian and the RQ Worker.

The PDE shall:

- Implement an API that sends out process outputs y(t) and takes in control inputs, u(t) for each simulation with an unique SimID. 
- Send all Tag data for all active simulations to the Data Historian at a defined sample time.


## The Engine APIs

The Engine shall implement these APIs

- Process manipulation
1. GET all tags in simulation SimID: 						GET /api/sims/{SimID}/all
Returns all tags in the simulation in JSON format

2. GET one tag in simulation SimID: 						GET /api/sims/{SimID}/{tag}
Returns one tag in the simulation in JSON format

3. POST a control action to a tag in simulation SimID:		POST /api/sims/{SimID}/{tag}
Returns new value of control action if successful 

- Simulation startup and management
1. GET all possible models: 								GET /api/models/
Returns a list of all possible models

2. GET a new simulation with ModelID: 						GET /api/models/{ModelID}/start
Returns a unique SimID if startup is successful

3. GET status of all simulations:							GET /api/sims/all
Returns all running simulations and their status



# Graphics
The Graphics shall be completely decoupled from the PDE. A Graphics page should talk to the PDE only via the API.
The Graphics shall correspond to a specific Model.
We should have the same number of Models and we have Graphics.
The Graphics should implement buttons for all input Tags defined in the model
The Graphics should implement visuals for all output Tags defined in the model
The Graphics should have a link to the time series stored in the Data Historian

Graphics loading steps
1. User navigates to a general Welcome page with a list of models
2. Clicking on a Model leads to the Model's corresponding Graphics page
3. The Graphics shall have a start button, which will call the START SIMULATION function, /api/models/{ModelID}/start in the PDE and receive and record the SimID returned.
4. The Graphics shall start updating the visuals for all process output Tags (decide whether the PDE pushes updates to Graphics or the Graphics requests updates from the server) by using the SimID.
5. The Graphics shall have buttons, sliders or other components to manipulate the process input Tags. Upon clicking on or manipulating the component, the Graphics shall send the control action to the server by using the SimID.
6. The Graphics shall have a link to the Process Data Historian or display a graph containing Historian data corresponding to this SimID.


