import control
from collections import OrderedDict
from pde import Model, Tag, TagType


def WoodBerry(model_id):

    g11 = control.tf([12.8], [16.7, 1]) * control.tf(*control.pade(1, 1))
    g12 = control.tf([-18.9], [21.0, 1]) * control.tf(*control.pade(3, 1))
    g21 = control.tf([6.6], [10.9, 1]) * control.tf(*control.pade(7, 1))
    g22 = control.tf([-19.4], [14.4, 1]) * control.tf(*control.pade(3, 1))
    g1f = control.tf([3.8], [14.9, 1]) * control.tf(*control.pade(8, 1))
    g2f = control.tf([4.9], [13.2, 1]) * control.tf(*control.pade(3, 1))

    row_1_num = [x[0][0] for x in (g11.num, g12.num, g1f.num)]
    row_2_num = [x[0][0] for x in (g21.num, g22.num, g2f.num)]
    row_1_den = [x[0][0] for x in (g11.den, g12.den, g1f.den)]
    row_2_den = [x[0][0] for x in (g21.den, g22.den, g2f.den)]

    sys = control.tf([row_1_num, row_2_num], [row_1_den, row_2_den])

    R = Tag(1, 'Reflux', 'Reflux flow rate', TagType.INPUT)
    S = Tag(2, 'Steam', 'Steam flow rate', TagType.INPUT)
    F = Tag(3, 'Feed', 'Feed flow rate', TagType.INPUT)
    x_D = Tag(4, 'x_D', 'Distillate purity', TagType.OUTPUT)
    x_B = Tag(5, 'x_B', 'Bottoms purity', TagType.OUTPUT)

    return Model(
        model_id,
        'Wood-Berry Distillation Model',
        sys,
        OrderedDict([('R', R), ('S', S), ('F', F)]),
        OrderedDict([('x_D', x_D), ('x_B', x_B)]),
    )
