import pickle
from wood_berry import WoodBerry


f = open('models/wood_berry.pkl', 'wb')
f.write(pickle.dumps(WoodBerry(1)))
