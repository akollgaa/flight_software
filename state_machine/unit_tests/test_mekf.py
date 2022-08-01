import unittest
import sys
from numpy import testing, array, eye

sys.path.insert(0, './state_machine/applications/flight')

import lib.mekf as mekf

def col(arr):
    return array([arr]).transpose()

class PropogationTest(unittest.TestCase):

    def test(self):
        expect = array([[0.5931645151518956, 0.42554207999942495, 0.5398640677185691, 0.41906632470378713]]).transpose()
        testing.assert_almost_equal(
            expect,
            mekf.propagate_state(
                array([[0.5, 0.5, 0.5, 0.5]]).transpose(),
                array([[0.324, 0.24, 0.9]]).transpose(),
                array([[0.23, 0.12, 0.321]]).transpose(),
                0.5
            )
        )

        expect = array([[-0.5242460284827297, 0.7105953066479479, 0.250513925250434, -0.39681631146616725]]).transpose()
        testing.assert_almost_equal(
            expect,
            mekf.propagate_state(
                array([[-0.5244311817641283, 0.7083212680159963, 0.2543322132742208, -0.3982060297895143]]).transpose(),
                array([[0.0, 0.0, 0.0]]).transpose(),
                array([[-0.03134203276802751, 0.7690511428713179, 0.5255725869290838]]).transpose(),
                0.01
            )
        )
        expect = col([-0.663050880225187, -0.17257983473214392, 0.29532112903513086, -0.6658567125304409])
        testing.assert_almost_equal(
            expect,
            mekf.propagate_state(
                col([-0.6622297601736082, -0.1700235029765648, 0.2950029393932262, -0.6674706127803229]),
                col([0.0, 0.0, 0.0]),
                col([0.172956626815103, -0.3898324679463814, -0.4633751544967398]),
                0.01
            )
        )

class StepTest(unittest.TestCase):

    def test(self):
        mekf.q = col([-0.6622297601736082, -0.1700235029765648, 0.2950029393932262, -0.6674706127803229])
        mekf.β = col([0.0, 0.0, 0.0])
        mekf.P = eye(6)
        ω = col([0.172956626815103, -0.3898324679463814, -0.4633751544967398])
        δt = 0.01
        nr_mag = col([0.1742196121801597, -0.002369930036338437, 0.9847039708274856])
        nr_sun = col([-0.3682708598271492, -0.852992443674256, -0.36983843071913647])
        br_mag = col([0.5637063206387467, -0.3048018674964489, 0.7676789730366488])
        br_sun = col([-0.8447985439341171, 0.42909923888397816, 0.31967055440873193])

        mekf.step(ω, δt, nr_mag, nr_sun, br_mag, br_sun)

        nq = col([-0.642273864229494, -0.18501248983065613, 0.28128772511044003, -0.6885723474236881])
        nβ = col([-0.0005577008504866591, 2.378549540184056e-5, -0.00045610528914747793])
        nP = array([[1.2914081975964834e-6, -4.1121919391426914e-7, 1.9099329105176787e-7, -1.291277778540849e-8,
                     4.111776649701094e-9, -1.9097400267749725e-9],
                    [-4.1121919391426914e-7, 7.137595468241695e-7, -1.0394226300259473e-7,
                     4.1117766497011006e-9, -7.136874643902605e-9, 1.0393176589423933e-9],
                    [1.9099329105176784e-7, -1.0394226300259472e-7, 7.956831088134053e-7, -
                     1.9097400267749833e-9, 1.039317658942383e-9, -7.95602752935359e-9],
                    [-1.2912777785408491e-8, 4.1117766497011006e-9, -1.909740026774983e-9,
                     0.9999010102280946, -4.111361402185755e-11, 1.909547162528913e-11],
                    [4.111776649701094e-9, -7.1368746439026054e-9, 1.0393176589423828e-9, -
                     4.1113614021857556e-11, 0.9999010101703414, -1.0392126985075322e-11],
                    [-1.909740026774972e-9, 1.0393176589423935e-9, -7.956027529353588e-9, 1.9095471625289132e-11,
                     -1.0392126985075322e-11, 0.9999010101785322]])

        testing.assert_almost_equal(mekf.q, nq, err_msg="incorrect q value")
        testing.assert_almost_equal(mekf.β, nβ, err_msg="incorrect β value")
        testing.assert_almost_equal(mekf.P, nP, err_msg="incorrect P value")
