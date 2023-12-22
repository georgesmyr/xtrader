from yieldcurve.helpers import p2xdate, interp1_flat_extrapolation, nelson_siegel
from yieldcurve.tree_helpers import x2r_mapping_rgp, x2r_mapping_bk, x2r_mapping_hw
from yieldcurve.tree_helpers import ih_mapping_rgp, ih_mapping_bk, ih_mapping_hw
from scipy.sparse import csr_matrix
import math
import numpy as np
import copy
import cal


class MyTree:
    def __init__(self, today, currency, mrs0, sigma0, time, rg, displpara, prunetol,
                 m_data, model, method, rstar, deltar, first_qrm, n_sigmas, ns_mrs, ns_sigma,
                 swap_crv_id=0, discount_crv_id=1):

        self.new_negative_rates_approach = True
        self.m_data = m_data
        self.ns_sigma = ns_sigma  # Nelson-Siegels-Svensson parameterization for volatility (Boolean)
        self.ns_mrs = ns_mrs  # Nelson-Siegels-Svensson parameterization for mean reversion speed (Boolean)
        self.model = model  # Type of model, e['g[' Extended Regime Switch, Hull-White, Black-Karasinski
        self.n_sigmas = n_sigmas  # Number of sigmas
        self.first_qrm = first_qrm  # First use the QRM curve (Boolean)
        self.prunetol = prunetol  # Pruning tolerance level, default 1e-12
        self.tol = max(self.prunetol, 1e-12)  # If pruning tolerance level below 1e-12 use 1e-12
        self.max_iter = 50  # Maximum number of iterations, hardcoded as 50
        self.today = today  # Date of today
        self.currency = currency  # Quoted currency
        self.displpara = displpara  # Displacement parameter (or servicing fee)
        self.rg = rg - math.log(1 - self.displpara + 2e-6)  # Regime switch thresholds
        self.displpara = -math.log(1 - self.displpara)  # Transformed displacement parameter
        self.mrs0 = mrs0  # Calibrated MRS pararmeters of yesterday
        self.sigma0 = sigma0  # Calibrated volatility parameters for NSS based on yesterday[' Note that the sigmas are the sigmas of the Ornstein-Uhlenback process['
        self.time0 = time  # Full time grid of dates of the calibration instruments
        self.time_e = np.array([x for x in self.time0], dtype=np.float64)  # Copy of the full time grid of dates
        self.time = np.zeros(len(self.time_e))  # Time vector of equal length of the
        self.swap_crv_id = swap_crv_id
        self.discount_crv_id = discount_crv_id

        self.currency = currency
        self.m_data = m_data

        for k in range(len(self.time0)):
            if p2xdate(cal.calEndOfMonth(self.time0[k])) == self.time0[k]:
                self.time[k] = cal.calYearFraction('30/360 ISDA', self.today + 1, self.time0[k] + 1)
            else:
                self.time[k] = cal.calYearFraction('30/360 ISDA', self.today, self.time0[k] + 1)

        self.time_steps = np.diff(self.time, n=1).astype(np.float64)  # time between time fractions
        self.n_steps = len(self.time_steps)
        self.grid = np.empty(self.n_steps + 1, dtype=object)
        self.transition_probs = np.empty(self.n_steps, dtype=object)
        self.probs = np.empty(self.n_steps + 1, dtype=object)

        self.n_crvs = len(m_data.curves['CurveNames'])
        self.q = np.empty((self.n_steps + 1, self.n_crvs), dtype=object)
        self.g = np.zeros((self.n_steps + 1, self.n_crvs))
        self.zerorates = np.empty((self.n_steps + 1, self.n_crvs), dtype=object)
        self.discountfactors = np.empty((self.n_steps + 1, self.n_crvs), dtype=object)

        self.zerorates_actact = np.empty((self.n_steps + 1, self.n_crvs), dtype=object)
        self.discountfactors0 = np.empty(self.n_crvs, dtype=object)  # market discount factors
        self.forward_crv0 = np.empty(self.n_steps, dtype=object)
        self.set_market_data()

        if 'HW96' in method:
            self.HW96 = True
        else:
            self.HW96 = False

        self.crv = np.empty(self.n_steps + 1, dtype=object)
        self.rstar = np.log(1 + rstar) + self.displpara
        self.deltar = np.log(1 + rstar) - np.log(1 + rstar - deltar)

        if model == 'BK':
            self.h = lambda x, x_rg, r_star=self.rstar, delta_r=self.deltar, displ_para=self.displpara: x2r_mapping_bk(
                x, x_rg, r_star, delta_r, displ_para)
            self.h1 = lambda x, x_rg, r_star=self.rstar, delta_r=self.deltar, displ_para=self.displpara: ih_mapping_bk(
                x, x_rg, r_star, delta_r, displ_para)
        elif model == 'HW':
            self.h = lambda x, x_rg, r_star=self.rstar, delta_r=self.deltar, displ_para=self.displpara: x2r_mapping_hw(
                x, x_rg, r_star, delta_r, displ_para)
            self.h1 = lambda x, x_rg, r_star=self.rstar, delta_r=self.deltar, displ_para=self.displpara: ih_mapping_hw(
                x, x_rg, r_star, delta_r, displ_para)
        elif model == 'ERS':
            self.h = lambda x, x_rg, r_star=self.rstar, delta_r=self.deltar, displ_para=self.displpara: x2r_mapping_rgp(
                x, x_rg, r_star, delta_r, displ_para)
            self.h1 = lambda x, x_rg, r_star=self.rstar, delta_r=self.deltar, displ_para=self.displpara: ih_mapping_rgp(
                x, x_rg, r_star, delta_r, displ_para)

        self.mrs = np.zeros(self.n_steps, dtype=np.float64)
        self.sigma = np.zeros(self.n_steps, dtype=np.float64)
        self.qrm_scalefactor = np.ones(self.n_steps)

        self.set_sde_paras(self.mrs0, self.sigma0)
        self.dx = np.zeros(self.n_steps + 1)
        self.update_mytree(False)

        self.g1 = []
        self.discountfactors01 = []
        self.q1 = []
        self.zerorates1 = []
        self.discountfactors1 = []
        self.forward_crv01 = []

    def convert_rates(self, crv_id):
        for j in range(self.discountfactors.shape[0] - 1):
            year_fraction = cal.calYearFraction('ACT/ACT ISDA', self.time_e[j], self.time_e[j + 1])
            self.zerorates_actact[j, crv_id] = \
                self.discountfactors[j, crv_id] ** (-np.reciprocal(year_fraction)) - 1

    def calc_probs(self):
        self.probs[0] = 1
        for j in range(1, len(self.time_e)):
            self.probs[j] = self.probs[j - 1] * self.transition_probs[j - 1]

    def pull_back(self, n0, n1, cf):
        df1 = cf.copy()
        for j in range(n1 - 1, n0 - 1, -1):
            df1 = self.discountfactors[j, self.discount_crv_id] * (self.transition_probs[j] * df1)
        return df1

    def set_market_data(self):
        for k in range(self.n_crvs):
            self.discountfactors0[k] = self.m_data.curves['Crvs'][k](self.time_e)

        self.forward_crv0 = -12 * np.log(self.discountfactors0[self.swap_crv_id][1:]
                                         / self.discountfactors0[self.swap_crv_id][0:-1]) + self.displpara
        self.forward_crv0[self.forward_crv0 < 2e-6] = 2e-6
        self.forward_crv0 -= self.displpara

    def set_sde_paras(self, mrs0, sigma0):
        if self.ns_mrs:
            self.mrs = nelson_siegel(mrs0['value'], self.time[:-1])
        else:
            if len(mrs0['time']) > 1:
                self.mrs = interp1_flat_extrapolation(self.time[:-1], mrs0['time'], mrs0['value'])
            else:
                if np.isscalar(mrs0['value']):
                    self.mrs.fill(mrs0['value'])
                else:
                    self.mrs.fill(mrs0['value'][0])

        if self.ns_sigma:
            self.sigma = nelson_siegel(sigma0['value'], self.time[:-1])
        else:
            if len(sigma0['time']) > 1:
                self.sigma = interp1_flat_extrapolation(self.time[:-1], sigma0['time'], sigma0['value'])
            else:
                if np.isscalar(sigma0['value']):
                    self.sigma.fill(sigma0['value'])
                else:
                    self.sigma.fill(sigma0['value'][0])

        self.sigma = np.maximum(self.sigma, 1e-2)
        self.sigma *= (self.forward_crv0 + self.displpara) / self.h1(self.forward_crv0, self.rg)
        if self.new_negative_rates_approach:
            self.calc_qrm_scalefactor()
            self.sigma *= self.qrm_scalefactor

    def calc_qrm_scalefactor(self):
        displpara = -np.log(np.exp(-self.displpara) + 2e-6)
        if self.model == 'ERS':
            ind_BK = self.forward_crv0 + displpara < self.rg[0]
            if sum(ind_BK) > 0:
                self.qrm_scalefactor[ind_BK] = (self.rg[0] - displpara) / self.rg[0]
            if sum(np.invert(ind_BK)) > 0:
                self.qrm_scalefactor[np.invert(ind_BK)] = self.forward_crv0[np.invert(ind_BK)] \
                                                   / (self.forward_crv0[np.invert(ind_BK)] + displpara)

    def update_mytree(self, allcurves=False):

        if allcurves:  # construct trees for all curves provided
            q_in = self.q
            z_in = self.zerorates
            df_in = self.discountfactors
            g_in = self.g
            df0_in = self.discountfactors0
        else:  # construct trees only for discount and forecast curves
            q_in = self.q[:, [self.discount_crv_id, self.swap_crv_id]]
            z_in = self.zerorates[:, [self.discount_crv_id, self.swap_crv_id]]
            df_in = self.discountfactors[:, [self.discount_crv_id, self.swap_crv_id]]
            g_in = self.g[:, [self.discount_crv_id, self.swap_crv_id]]
            df0_in = self.discountfactors0[[self.discount_crv_id, self.swap_crv_id]]

        (q_out, z_out, df_out, g_out) = self.update_mytree_multi(q_in, z_in, df_in, g_in, df0_in)

        if allcurves:
            self.q = q_out
            self.zerorates = z_out
            self.discountfactors = df_out
            self.g = g_out
        else:
            self.q[:, [self.discount_crv_id, self.swap_crv_id]] = q_out
            self.zerorates[:, [self.discount_crv_id, self.swap_crv_id]] = z_out
            self.discountfactors[:, [self.discount_crv_id, self.swap_crv_id]] = df_out
            self.g[:, [self.discount_crv_id, self.swap_crv_id]] = g_out

    def update_mytree_multi(self, q, zerorates, discountfactors, g, discountfactors0):

        n_steps = self.time_steps.shape[0]
        if self.HW96:
            m0 = np.exp(-self.mrs * self.time_steps) - 1
            s0 = self.sigma * np.sqrt((1 - np.exp(-2 * self.mrs * self.time_steps)) / (2 * self.mrs))
        else:
            m0 = -self.mrs * self.time_steps
            s0 = self.sigma * np.sqrt(self.time_steps)

        beta2 = np.exp(-2 * self.mrs * self.time_steps)
        # std at t>0 of the x process see section 5.3.1. of the YCM documentation
        vt = np.zeros(len(beta2) + 1)

        for j in range(len(beta2)):
            vt[j + 1] = vt[j] * beta2[j] + s0[j] ** 2

        s23 = math.sqrt(2 / 3)  # Upper-bound probability to assume positive probabilities
        self.grid[0] = np.array([0.0])  # Startvalue grid
        self.probs[0] = np.array([1.0])  # Startvalue probability
        q[0] = np.array([1.0])  # Startvalue Arrow-Debreu price

        if self.first_qrm:
            self.dx = np.concatenate([[s0[0], s0[0]], math.sqrt(3) * s0[1:]])  # Deltas of the x process, dx
            pd = 0.5  # Down movement probability of the binomial lattice
            pu = 0.5  # Up movement probability of the binomial lattice
            self.grid[1] = np.array([-self.dx[1], self.dx[1]])
            s = np.array([pd, pu])
            i = np.array([0, 0])
            j = np.array([0, 1])
        else:
            self.dx = math.sqrt(3) * np.concatenate([[s0[0]], s0])  # Deltas of the x process, dx
            pd = 1 / 6
            pm = 2 / 3
            pu = 1 / 6
            self.grid[1] = np.array([-self.dx[1], 0, self.dx[1]])
            s = np.array([pd, pm, pu])
            i = np.array([0, 0, 0])
            j = np.array([0, 1, 2])

        self.transition_probs[0] = csr_matrix((s, (i, j)), shape=(1, len(j)))
        self.probs[1] = self.probs[0] * self.transition_probs[0]

        if self.prunetol > 0:
            not_pruned = self.probs[1] >= self.prunetol
            self.grid[1] = self.grid[1][not_pruned]
            self.transition_probs[0] = self.transition_probs[0][:, not_pruned]
            self.probs[1] = self.probs[1][not_pruned]

        df0 = np.stack(discountfactors0).transpose()
        (q[1], zerorates[0], discountfactors[0], g[0]) = self.mycalibrate_update_F2_multi(q[0], g[0], 0, df0[1])

        for N in range(1, n_steps):
            M = (m0[N] + 1) * self.grid[N]

            # lattice pruning
            k = np.rint(M / self.dx[N + 1])
            k = np.minimum(k, np.floor(self.n_sigmas * np.sqrt(vt[N + 1]) / self.dx[N + 1]))
            k = np.maximum(k, -np.floor(self.n_sigmas * np.sqrt(vt[N + 1]) / self.dx[N + 1]))

            # probabilities of trinomial tree
            alpha = M / self.dx[N + 1] - k
            pu = 1 / 6 + alpha * (alpha + 1) / 2
            pd = 1 / 6 + alpha * (alpha - 1) / 2
            pm = 1 - pu - pd

            # adjustment applied if necessary to prevent negative probabilities
            index = np.absolute(alpha) > s23
            pu[index] = (alpha[index] + 1) / 2
            pd[index] = (1 - alpha[index]) / 2
            pm[index] = 0

            index = alpha > 1
            pu[index] = 1
            pm[index] = 0
            pd[index] = 0

            index = alpha < -1
            pu[index] = 0
            pm[index] = 0
            pd[index] = 1

            i = np.concatenate([range(len(self.grid[N])), range(len(self.grid[N])),
                                range(len(self.grid[N]))])  # Each node has three branches
            jmin = np.amin(k) - 1
            k = k - jmin
            j = (np.concatenate([k, k + 1, k + 2])).astype(int)  # -1 is there to match Python indexing
            s = np.concatenate([pd, pm, pu])  # The set of transition probabilities
            mj = np.amax(j)
            self.grid[N + 1] = jmin * self.dx[N + 1] + (self.dx[N + 1]) * np.arange(mj)  # Determine the next grid one step ahead in time
            self.transition_probs[N] = csr_matrix((s, (i, j - 1)), shape=(len(self.grid[N]), mj))  # Store the transition probabilties in a cell array. -1 is there to match Python indexing
            self.probs[N + 1] = self.probs[N] * self.transition_probs[N]

            (q[N + 1], zerorates[N], discountfactors[N], g[N]) = self.mycalibrate_update_F2_multi(q[N], g[N], N, df0[N + 1])

        return q, zerorates, discountfactors, g

    def mycalibrate_update_F2_multi(self, q_all, g_all, grid_num, discountfactors0_all):
        # Calibrate the lattice using the discount rates.
        # The discountfactors0 are the market discount rates.
        # Given the initial set-up of the lattice, the nodes are adjusted in a vertical manner by adding the
        # g(.) terms as long as the difference between the observed and model discount rates has an error
        # larger than the tolerance level (tol).
        # The output Qnext contains the Arrow-Debreu prices.

        n_crvs = len(q_all)
        g = np.zeros(n_crvs)
        zerorates = np.empty(n_crvs, dtype=object)
        discountfactors = np.empty(n_crvs, dtype=object)
        q_next = np.empty(n_crvs, dtype=object)
        for crv_id in range(n_crvs):

            # # this is an adjustment only if we calibrate for the tree displacement as well
            # if (1 - self.displpara) ** (-self.time_steps[grid_num]) * np.sum(q_all[crv_id]) \
            #         - discountfactors0_all[crv_id] < 0:
            #     zrs = self.h(self.grid[grid_num] - 12, self.rg)[0]
            #     dfs = np.exp(-self.time_steps[grid_num] * zrs)
            #     self.displpara += np.log(discountfactors0_all[crv_id] / (dfs * q_all[crv_id])) / self.time_steps[grid_num]

            (g[crv_id], zerorates[crv_id], discountfactors[crv_id], q_next[crv_id]) = \
                self.find_opt_g(g_all[crv_id], discountfactors0_all[crv_id], q_all[crv_id], grid_num)

        return q_next, zerorates, discountfactors, g

    def find_opt_g(self, g, discountfactors0, q, grid_num):
        zerorates, dr = self.h(self.grid[grid_num] + g, self.rg)
        discountfactors = np.exp(-self.time_steps[grid_num] * zerorates)
        err = np.dot(discountfactors, q) - discountfactors0
        deriv = (-self.time_steps[grid_num]) * np.dot((discountfactors * q), dr)
        dg = np.absolute(err / deriv)
        dg = np.minimum(dg, np.maximum(math.fabs(g) / 50, 0.5))

        erra = -1
        errb = 1
        twosqrt = math.sqrt(2)

        # First a bisection approach is applied to determine two points on the optimization function erra and errb.
        # These points bound the optimum; given these points one can enclose the optimum in a faster.
        # Start with negative value for lower bound (erra) and positive value for upper bound.

        while ((erra < 0) or (errb > 0)) and np.greater(np.absolute(err), self.tol).all():

            if np.greater(err, 0).all():
                # in case of a positive error add a value to g
                a = g
                erra = err
                deriva = deriv
                g1 = g + dg
            else:
                # in case of a non-positive error subtract a value from g
                b = g
                errb = err
                derivb = deriv
                g1 = g - dg

            if (erra < 0) or (errb > 0):
                g = g1
                zerorates, dr = self.h(self.grid[grid_num] + g, self.rg)
                discountfactors = np.exp(-self.time_steps[grid_num] * zerorates)
                err = np.dot(discountfactors, q) - discountfactors0
                deriv = (-self.time_steps[grid_num]) * np.dot((discountfactors * q), dr)

                if np.greater(np.absolute(deriv), 1e-6).all():
                    dg = np.absolute(err / deriv)
                else:
                    dg = twosqrt * dg

            # Whenever the error is larger than the tolerance level, adjust the g values and re-calculate the short
            # rates and discount factors corresponding to the lattice: grid + g.
            # Use the bisection approach for relative fast convergence.
        i = 1

        while (i < self.max_iter) and (np.greater(np.absolute(err), self.tol).all()):
            if np.less(np.absolute(erra / deriva), np.absolute(errb / derivb)).all():
                c0 = erra
                c1 = deriva * (b - a)
                c2 = errb - c1 - c0
                if np.greater(c2, 0).all():
                    x = (-c1 - math.sqrt(math.pow(c1, 2) - 4 * c0 * c2)) / (
                            2 * c2)
                else:
                    x = (-c1 - math.sqrt(math.pow(c1, 2) - 4 * c0 * c2)) / (2 * c2)
                g = a + x * (b - a)

            else:
                c0 = -errb
                c1 = derivb * (b - a)
                c2 = -erra - c1 - c0

                if np.greater(c2, 0).all():
                    x = (-c1 - math.sqrt(math.pow(c1, 2) - 4 * c0 * c2)) / (
                            2 * c2)
                else:
                    x = (-c1 - math.sqrt(math.pow(c1, 2) - 4 * c0 * c2)) / (2 * c2)

                g = b - x * (b - a)

            zerorates, dr = self.h(self.grid[grid_num] + g, self.rg)
            discountfactors = np.exp(-self.time_steps[grid_num] * zerorates)
            err = np.dot(discountfactors, q) - discountfactors0
            deriv = (-self.time_steps[grid_num]) * np.dot((discountfactors * q), dr)

            if np.greater(err, 0).all():
                a = g
                erra = err
                deriva = deriv
            else:
                b = g
                errb = err
                derivb = deriv

            i = i + 1

        q_next = (discountfactors * q) * (self.transition_probs[grid_num])

        return g.item(), zerorates, discountfactors, q_next

    def calc_df0(self, n0, xx, crv_id):
        n1 = np.digitize(xx, self.time_e).item()
        if np.greater(xx, self.time_e[n1 - 1]).all():
            dt1 = cal.calYearFraction('ACT/ACT ISDA', self.time_e[n1 - 1], xx)
            dt2 = cal.calYearFraction('ACT/ACT ISDA', self.time_e[n1 - 1], self.time_e[n1])
            df1 = self.discountfactors[n1 - 1][crv_id] ** (dt1 / dt2)

            dfh = interp1_flat_extrapolation([xx], self.m_data.curves['T'][crv_id],
                                             self.m_data.curves['R'][crv_id])
            dfh = (1 + dfh.copy()) ** (-(xx - self.m_data.today) / 365)

            df1 *= dfh / np.dot(self.q[n1 - 1, crv_id], df1)
        else:
            df1 = np.ones(len(self.grid[n1 - 1]))

        for j in range(n1 - 2, n0 - 1, -1):
            df1 = self.discountfactors[j][crv_id] * (self.transition_probs[j] * df1)
        return df1

    def calc_df(self, value_date, xx, crv_id):
        n = np.digitize(value_date, self.time_e)
        df = self.calc_df0(n - 1, xx, crv_id)
        if np.greater(value_date, self.time_e[n - 1]).all():
            df *= np.reciprocal(self.calc_df0(n - 1, value_date, crv_id))
        return df

    def get_q(self, value_date, crv_id):
        n = np.digitize(value_date, self.time_e)
        q = self.q[n - 1, crv_id].copy()
        if value_date > self.time_e[n - 1]:
            q *= self.calc_df0(n, value_date, crv_id)
        return q

    def copy_tree(self):
        self.g1 = copy.copy(self.g)
        self.q1 = copy.copy(self.q)
        self.zerorates1 = copy.copy(self.zerorates)
        self.discountfactors1 = copy.copy(self.discountfactors)
        self.discountfactors01 = copy.copy(self.discountfactors0)
        self.forward_crv01 = copy.copy(self.forward_crv0)
