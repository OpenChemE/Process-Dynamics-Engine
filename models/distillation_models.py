import control
from pde.model import Model
from pde.tag import Tag

def WoodBerry():
	g_tf = control.tf([12.8], [16.7,1])
	td = 1
	g_delay = control.tf(control.pade(td,1)[0],control.pade(td,1)[1])
	g11 = g_tf*g_delay

	g_tf = control.tf([-18.9], [21.0,1])
	td = 3
	g_delay = control.tf(control.pade(td,1)[0],control.pade(td,1)[1])
	g12 = g_tf*g_delay

	g_tf = control.tf([6.6], [10.9,1])
	td = 7
	g_delay = control.tf(control.pade(td,1)[0],control.pade(td,1)[1])
	g21 = g_tf*g_delay

	g_tf = control.tf([-19.4], [14.4,1])
	td = 3
	g_delay = control.tf(control.pade(td,1)[0],control.pade(td,1)[1])
	g22 = g_tf*g_delay

	g_tf = control.tf([3.8], [14.9,1])
	td = 8
	g_delay = control.tf(control.pade(td,1)[0],control.pade(td,1)[1])
	g1f = g_tf*g_delay

	g_tf = control.tf([4.9], [13.2,1])
	td = 3
	g_delay = control.tf(control.pade(td,1)[0],control.pade(td,1)[1])
	g2f = g_tf*g_delay

	row_1_num = [x[0][0] for x in (g11.num, g12.num, g1f.num)]
	row_2_num = [x[0][0] for x in (g21.num, g22.num, g2f.num)]

	row_1_den = [x[0][0] for x in (g11.den, g12.den, g1f.den)]
	row_2_den = [x[0][0] for x in (g21.den, g22.den, g2f.den)]

	sys = control.tf([row_1_num,row_2_num],[row_1_den,row_2_den])

	R = Tag('Reflux', 'Reflux flow rate', IOtype='INPUT')
	S = Tag('Steam', 'Steam flow rate', IOtype='INPUT')
	F = Tag('Feed', 'Feed flow rate', IOtype='INPUT')

	xD = Tag('x_D', 'Distillate purity', IOtype='OUTPUT')
	xB = Tag('x_B', 'Bottoms purity', IOtype='OUTPUT')

	inputs = {'R':R,'S':S,'F':F}
	outputs = {'xD':xD,'xB':xB}
	wood_berry = Model(sys, "Wood Berry Distillation Model", inputs, outputs)
	return wood_berry