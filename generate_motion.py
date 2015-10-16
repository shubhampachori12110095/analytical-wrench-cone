#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Stephane Caron <caron@phare.normalesup.org>
#
# This file is part of surface-contacts-icra-2015.
#
# surface-contacts-icra-2015 is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# surface-contacts-icra-2015 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# surface-contacts-icra-2015. If not, see <http://www.gnu.org/licenses/>.

import pylab

from dmotions import Trajectory, HRP4
from dmotions.hrp4 import Stance
from dmotions.interpolation import active_bezier_interpolate
from dmotions.hrp4.topp import WrenchConstraint
from numpy import array, eye, dot, linalg, pi
from dmotions.vector import norm


hrp = HRP4(topp_npoints=1000, topp_constraint=WrenchConstraint)

ACTUATED_DOFS = hrp.get_dofs('CHEST', 'R_LEG', 'L_LEG', 'R_ARM', 'L_ARM',
                             'TRANS_Y', 'TRANS_X', 'TRANS_Z')


def project_foot_velocity(q, qd_ref):
    """Return qd s.t. J * qd = 0 and |qd - qd_ref| is minimized."""
    J = hrp.compute_foot_jacobian(hrp.left_foot_link, q)
    P = eye(56) - dot(linalg.pinv(J), J)
    return dot(dot(P, linalg.pinv(P)), qd_ref)


def connect(q0, q1, support):
    """Bezier curve with as-linear-as-possible velocity."""
    assert not hrp.self_collides(q0)
    assert not hrp.self_collides(q1)
    qd_ref = (q1 - q0) / norm(q1 - q0)
    qd0 = project_foot_velocity(q0, qd_ref)
    qd1 = project_foot_velocity(q1, qd_ref)
    traj = active_bezier_interpolate(
        q0, qd0, q1, qd1, ACTUATED_DOFS, support)
    return traj


q_start = pi / 180 * array(
    [0.,      0.,    0.,     0.,     0.,
     0.,      0.,    0.,     0.,     0.,
     0.,      0.,    0.,     0.,     0.,
     0.,      0.,   -0.76, -22.02,  41.29,
     -18.75, -0.45,  0.,     1.15, -21.89,
     41.21, -18.74, -1.10,   8.,     0.,
     0.,      0.,   -3.,   -10.,     0.,
     -30.,    0.,    0.,     0.,     0.,
     0.,     -3.,   10.,     0.,   -30.,
     0.,      0.,    0.,     0.,     0.,
     0. * (180 / pi),       # [m/rad] TRANS_X
     0. * (180 / pi),       # [m/rad] TRANS_Y
     -0.0387 * (180 / pi),  # [m/rad] TRANS_Z (feet touch the floor)
     0.,                    # [rad] ROT_R
     0.,                    # [rad] ROT_P
     0.])                   # [rad] ROT_Y

q_comleft = \
    array([0.00000000,  0.00000000,  0.00000000,  0.00000000,  0.00000000,
           0.00000000,  0.00000000,  0.00000000,  0.00000000,  0.00000000,
           0.00000000,  0.00000000,  0.00000000,  0.00000000,  0.00000000,
           0.00000000,  0.00118611, -0.14315774, -0.34923836,  0.73068834,
          -0.37228841,  0.12204464,  0.00131564, -0.10959855, -0.33846228,
           0.71184241, -0.36320601,  0.11047787,  0.15604690, -0.00292546,
           0.00000000,  0.00000000, -0.06132496, -0.14572702,  0.00442847,
          -0.52713123,  0.00000000,  0.00000000,  0.00000000,  0.00000000,
           0.00000000, -0.06132139,  0.20359890,  0.00443174, -0.52553889,
           0.00000000,  0.00000000,  0.00000000,  0.00000000,  0.00000000,
           0.02605553,  0.08471537, -0.04321228,  0.00000000,  0.00000000,
           0.0000000])

q_c3po = \
    array([0.00000000e+00,   0.00000000e+00,  -2.60046563e-16,
           0.00000000e+00,  -2.60046563e-16,   0.00000000e+00,
          -2.60046560e-16,   0.00000000e+00,   0.00000000e+00,
          -4.50930800e-15,   0.00000000e+00,  -4.50930807e-15,
           0.00000000e+00,  -4.50930807e-15,   0.00000000e+00,
          -4.50930800e-15,   9.45055790e-03,  -1.83551404e-01,
          -7.79022310e-01,   8.78871699e-01,  -4.81160707e-02,
           1.83791813e-01,   1.58375597e-03,  -1.35570684e-01,
          -1.28703450e-01,   2.48598574e-01,  -1.09680652e-01,
           1.36451361e-01,   2.18538123e-02,  -2.19932584e-02,
           0.00000000e+00,   0.00000000e+00,  -2.67218252e-01,
          -7.02197180e-01,   1.44640348e+00,  -1.01289066e+00,
           0.00000000e+00,  -3.39061720e-15,  -1.53554789e-15,
           1.00136913e-15,   0.00000000e+00,  -2.67124714e-01,
           7.69639186e-01,  -1.44639515e+00,  -9.87170259e-01,
           0.00000000e+00,  -3.33644647e-16,   0.00000000e+00,
          -3.33066900e-16,  -1.42289629e-16,   1.52893123e-02,
           1.06716976e-01,  -8.27889835e-03,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00])

q_equi1 = \
    array([0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   1.27570012e-16,
           0.00000000e+00,   1.27570012e-16,   0.00000000e+00,
           1.27570012e-16,   0.00000000e+00,   1.27570012e-16,
           0.00000000e+00,  -5.31697580e-01,  -1.37186676e-02,
          -1.05000000e+00,   6.72038247e-01,   6.91383507e-02,
           1.95835459e-02,   2.16317098e-03,  -1.91291785e-01,
          -3.61300248e-01,   6.75221914e-01,  -3.03612956e-01,
           1.92175266e-01,  -8.01118850e-02,  -3.98762220e-01,
           0.00000000e+00,   0.00000000e+00,  -1.18124922e+00,
          -5.04941626e-01,   1.44612245e+00,  -1.81210097e+00,
           0.00000000e+00,   3.18726237e-16,  -3.18726237e-16,
           5.49104856e-09,   0.00000000e+00,  -1.56818020e+00,
           4.63682676e-01,  -1.44673829e+00,  -1.71382162e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          -2.28751701e-07,   0.00000000e+00,  -8.83400882e-04,
           1.37974225e-01,  -4.92850237e-02,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00])

q_eagle = \
    array([0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          -2.38968325e-15,   0.00000000e+00,  -2.38968325e-15,
           0.00000000e+00,  -2.38968325e-15,   0.00000000e+00,
          -2.38968325e-15,  -5.31697573e-01,  -1.37186678e-02,
          -9.36266529e-01,   6.72038187e-01,   6.91384916e-02,
           1.95834886e-02,   2.16317105e-03,  -1.91291783e-01,
          -3.61300263e-01,   6.75221935e-01,  -3.03612962e-01,
           1.92175242e-01,  -8.01118845e-02,  -3.98762309e-01,
           0.00000000e+00,   0.00000000e+00,  -1.18124923e+00,
          -1.40862387e+00,   1.44612246e+00,   3.49065850e-02,
           0.00000000e+00,   1.63367867e-15,   4.80124714e-15,
           9.12758123e-08,  -2.94392336e-16,  -1.56818014e+00,
           1.27529159e+00,  -1.44673828e+00,   3.49065566e-02,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          -2.40600596e-07,   0.00000000e+00,  -8.83400906e-04,
           1.37974232e-01,  -4.92850244e-02,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00])

q_eagle2 = \
    array([0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          -1.13049189e-16,   0.00000000e+00,  -1.13049189e-16,
           0.00000000e+00,  -1.13049189e-16,   0.00000000e+00,
          -1.13049189e-16,  -5.31697573e-01,  -1.37186678e-02,
          -9.36266529e-01,   6.72038187e-01,   6.91384916e-02,
           1.95834512e-02,   2.16317105e-03,  -1.91291783e-01,
          -3.61300263e-01,   6.75221935e-01,  -3.03612962e-01,
           1.92175220e-01,  -8.01118845e-02,  -3.98762396e-01,
           0.00000000e+00,   0.00000000e+00,  -3.53177031e-02,
          -1.40862387e+00,   1.44612245e+00,   3.45066261e-02,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           6.50810699e-08,   0.00000000e+00,  -3.10400530e-02,
           1.27529167e+00,  -1.44673827e+00,   3.49065750e-02,
           0.00000000e+00,  -1.27570012e-16,  -1.66822324e-16,
          -2.69971583e-07,  -1.66822324e-16,  -8.83400906e-04,
           1.37974232e-01,  -4.92850244e-02,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00])

q_fly = \
    array([0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          -1.32675345e-16,   0.00000000e+00,  -1.32675345e-16,
           0.00000000e+00,  -1.32675345e-16,   0.00000000e+00,
          -1.32675345e-16,  -5.31697573e-01,  -1.37186678e-02,
          -9.36266529e-01,   6.72038187e-01,   6.91384916e-02,
           1.95833884e-02,   2.16317105e-03,  -1.91291783e-01,
          -3.61300263e-01,   6.75221935e-01,  -3.03612962e-01,
           1.92175191e-01,  -8.01118845e-02,  -1.98762396e-01,
           0.00000000e+00,   0.00000000e+00,  -3.53177031e-02,
          -6.90361512e-01,   1.44612235e+00,   3.45066060e-02,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           1.26461233e-07,   0.00000000e+00,  -3.10400530e-02,
           7.27553488e-01,  -1.44673825e+00,   3.49065657e-02,
           0.00000000e+00,   1.57009246e-16,   0.00000000e+00,
          -9.66028413e-08,   0.00000000e+00,  -8.83400906e-04,
           1.37974232e-01,  -4.92850244e-02,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00])

q_fly2 = \
    array([0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,  -5.31697573e-01,  -1.37186678e-02,
          -9.36266529e-01,   6.72038187e-01,   6.91384916e-02,
           1.95832459e-02,   2.16317105e-03,  -1.91291783e-01,
          -3.61300263e-01,   6.75221935e-01,  -3.03612962e-01,
           1.92175162e-01,  -8.01118845e-02,  -3.98762396e-01,
           0.00000000e+00,   0.00000000e+00,  -3.53177031e-02,
          -6.90361512e-01,   1.44612229e+00,  -6.74909954e-01,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           9.42456180e-08,   0.00000000e+00,  -3.10400530e-02,
           1.45783012e+00,  -1.44673820e+00,   3.49065671e-02,
           0.00000000e+00,  -1.27570012e-16,   0.00000000e+00,
          -1.58883364e-07,   0.00000000e+00,  -8.83400906e-04,
           1.37974232e-01,  -4.92850244e-02,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00])

q_eagle3 = \
    array([0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          -1.13049189e-16,   0.00000000e+00,  -1.13049189e-16,
           0.00000000e+00,  -1.13049189e-16,   0.00000000e+00,
          -1.13049189e-16,  -5.31697573e-01,  -1.37186678e-02,
          -9.36266529e-01,   6.72038187e-01,   6.91384916e-02,
           1.95834512e-02,   2.16317105e-03,  -1.91291783e-01,
          -3.61300263e-01,   6.75221935e-01,  -3.03612962e-01,
           1.92175220e-01,  -8.01118845e-02,  -1.98762396e-01,
           0.00000000e+00,   0.00000000e+00,  -3.53177031e-02,
          -1.40862387e+00,   1.44612245e+00,   3.45066261e-02,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           6.50810699e-08,   0.00000000e+00,  -3.10400530e-02,
           1.27529167e+00,  -1.44673827e+00,   3.49065750e-02,
           0.00000000e+00,  -1.27570012e-16,  -1.66822324e-16,
          -2.69971583e-07,  -1.66822324e-16,  -8.83400906e-04,
           1.37974232e-01,  -4.92850244e-02,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00])

q_equi2 =\
    array([0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,  -5.30426373e-01,  -1.66662360e-03,
          -8.81897608e-01,   6.91688450e-01,   8.51297350e-02,
           7.46465163e-03,   2.20596250e-03,  -1.95363994e-01,
          -4.24648707e-01,   7.55521166e-01,  -3.20555535e-01,
           1.96247692e-01,  -1.58804238e-01,  -4.08143387e-01,
           0.00000000e+00,   0.00000000e+00,  -1.15095983e+00,
          -5.11763808e-01,   1.44513465e+00,  -1.80611632e+00,
           0.00000000e+00,   2.40221614e-16,  -7.50501663e-16,
           5.49104862e-09,   0.00000000e+00,  -1.53484266e+00,
           4.55981690e-01,  -1.44514520e+00,  -1.71521827e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          -2.28751701e-07,   0.00000000e+00,  -1.63755803e-02,
           1.38534429e-01,  -6.01283466e-02,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00])

q_c3po2 = \
    array([0.00000000e+00,  -1.15303665e-16,  -1.15303665e-16,
          -1.15303665e-16,  -1.15303665e-16,  -1.15303665e-16,
          -1.15303665e-16,  -1.15303665e-16,  -7.19421271e-16,
          -5.05884043e-15,  -7.19421271e-16,  -5.05884043e-15,
          -7.19421271e-16,  -5.05884043e-15,  -7.19421271e-16,
          -5.05884043e-15,   9.83999747e-03,  -1.90936680e-01,
          -8.26779336e-01,   8.52418532e-01,   2.61665088e-02,
           1.91186996e-01,   1.63537987e-03,  -1.40574964e-01,
          -2.64750088e-01,   4.15885412e-01,  -1.40913757e-01,
           1.41455902e-01,  -1.02353201e-01,  -2.11336232e-02,
           0.00000000e+00,   0.00000000e+00,  -2.10305273e-01,
          -6.58760161e-01,   1.44468754e+00,  -6.84627665e-01,
           0.00000000e+00,  -2.00329331e-15,  -2.98788342e-15,
           3.36536354e-16,  -2.17114348e-16,  -2.11893350e-01,
           6.61302973e-01,  -1.44463764e+00,  -6.84649427e-01,
           0.00000000e+00,   1.15916982e-16,   0.00000000e+00,
          -6.73072709e-16,  -1.93194971e-16,  -2.69159294e-02,
           1.08592387e-01,  -1.93959479e-02,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00])

q_equi22 = \
    array([0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
           0.00000000e+00,   9.83999747e-03,  -1.90936680e-01,
          -8.26779336e-01,   8.52418532e-01,   2.61665088e-02,
           7.46465163e-03,   2.20596250e-03,  -1.95363994e-01,
          -4.24648707e-01,   7.55521166e-01,  -3.20555535e-01,
           1.96247692e-01,  -1.58804238e-01,  -4.08143387e-01,
           0.00000000e+00,   0.00000000e+00,  -1.15095983e+00,
          -5.11763808e-01,   1.44513465e+00,  -1.80611632e+00,
           0.00000000e+00,   2.40221614e-16,  -7.50501663e-16,
           5.49104862e-09,   0.00000000e+00,  -1.53484266e+00,
           4.55981690e-01,  -1.44514520e+00,  -1.71521827e+00,
           0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          -2.28751701e-07,   0.00000000e+00,  -1.63755803e-02,
           1.38534429e-01,  -6.01283466e-02,   0.00000000e+00,
           0.00000000e+00,   0.00000000e+00])

q_list = [
    q_start,
    q_comleft,
    q_c3po,
    q_equi1,
    q_eagle,
    q_eagle2,
    q_fly,
    q_fly2,
    q_eagle3,
    q_eagle,
    q_equi2,
    q_equi22,
    q_c3po2,
    q_comleft,
    # q_start,  # this segment is done separately in double support
]


def move_com(q, dcom):
    stance = Stance.from_q(hrp, q)
    stance.com = stance.com + array(dcom)
    stance.recompute_q()
    return stance.q


def export(version="v12"):  # petit clin d'oeil a la CA ;)
    global traj0, traj1
    last_chunk_open = connect(q_list[-1], q_list[0],
                              support=hrp.Support.DOUBLE)
    last_traj = hrp.maintain_foot_contact(last_chunk_open)
    retimed = Trajectory([retimed_traj] + last_traj.chunks,
                         active_dofs=retimed_traj.active_dofs)
    hrp.export_openhrp(retimed, "retimed-" + version)
    reacc10 = Trajectory([reacc10_traj] + last_traj.chunks,
                         active_dofs=reacc10_traj.active_dofs)
    hrp.export_openhrp(reacc10, "reacc10-" + version)
    reacc15 = Trajectory([reacc15_traj] + last_traj.chunks,
                         active_dofs=reacc15_traj.active_dofs)
    hrp.export_openhrp(reacc15, "reacc15-" + version)
    slowed10 = Trajectory([slowed10_traj] + last_traj.chunks,
                          active_dofs=slowed10_traj.active_dofs)
    hrp.export_openhrp(slowed10, "slowed10-" + version)
    slowed15 = Trajectory([slowed15_traj] + last_traj.chunks,
                          active_dofs=slowed15_traj.active_dofs)
    hrp.export_openhrp(slowed15, "slowed15-" + version)
    slowed20 = Trajectory([slowed20_traj] + last_traj.chunks,
                          active_dofs=slowed20_traj.active_dofs)
    hrp.export_openhrp(slowed20, "slowed20-" + version)
    scaled = Trajectory(scaled_traj.chunks + last_traj.chunks,
                        active_dofs=scaled_traj.active_dofs)
    hrp.export_openhrp(scaled, "scaled-" + version)
    original = Trajectory(original_traj.chunks + last_traj.chunks,
                          active_dofs=original_traj.active_dofs)
    hrp.export_openhrp(original, "original-" + version)


if __name__ == '__main__':
    pylab.ion()
    hrp.display()

    q_pairs = [(q_list[i], q_list[i + 1]) for i in xrange(len(q_list) - 1)]
    open_chunks = [connect(q[0], q[1], support=hrp.Support.LEFT) for q in
                   q_pairs]
    closed_trajs = map(hrp.maintain_foot_contact, open_chunks)
    original_traj = Trajectory.merge(*closed_trajs)

    retimed_traj = hrp.topp.retime_trajectory(original_traj, 0., 0.)
    tscale = retimed_traj.duration / original_traj.duration
    scaled_traj = original_traj.timescale(tscale)
    reacc10_traj = retimed_traj.timescale(0.90)
    reacc15_traj = retimed_traj.timescale(0.85)
    slowed10_traj = retimed_traj.timescale(1.10)
    slowed15_traj = retimed_traj.timescale(1.15)
    slowed20_traj = retimed_traj.timescale(1.20)

    print "original duration:", original_traj.duration
    print "retimed duration: ", retimed_traj.duration
    print "scaled duration:  ", scaled_traj.duration

    # hrp.collision_handle = None  # for manipulation in OpenRAVE GUI
    export()

    if False:
        kron = hrp.topp.retime_trajectory(scaled_traj, 0., 0.)
        hrp.topp.plot_last_instance(ylim=(0, 2))

    if False:  # compare with discrete contact points
        w_cons = hrp.topp.get_constraint(original_traj)

        def wtest(s, sd):
            return w_cons.test_abc(
                original_traj.q_full(s), original_traj.qd_full(s),
                original_traj.qdd_full(s), sd)