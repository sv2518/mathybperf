from firedrake import *
from mathybperf import *
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=1.5)


def plot_mat(a):
    a_assembled = assemble(a, mat_type='aij')
    plt.figure()
    A = a_assembled.M.handle
    A_np = petsc_to_py(A)
    plt.imshow(A_np, cmap='RdBu', vmin=-1, vmax=1)
    plt.axis('off')
    plt.colorbar()
    plt.show()


class ResultPlotter(object):

    def __init__(self):
        self.color = sns.color_palette(n_colors=3)
        self.plotting_args = {'linewidth': 2, 'markersize': 5}
        self.title = 'RTCF %d, DG %d (=%dx%d DOFS)\n quad_degree=(%d, %d)'

    def plot_knds(self, name, orders, dofs, defo, knds_mixed, knds_Schur, knds_A00, params, quad_degree_list, xlabel, type):
        # format the subplots
        len_x = int(len(orders)/2)
        len_y = len(orders) - int(len(orders)/2) - 1
        fig, axlist = plt.subplots(len_x, len_y, figsize=(13, 8))

        # add labels to outer frame not per subplot
        fig.add_subplot(111, frameon=False)
        plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
        plt.ylabel('condition numbers', weight='bold', labelpad=10)
        plt.xlabel(xlabel, weight='bold', labelpad=10)

        # clean up the xlabels
        defo = self.round(defo)

        c = 0
        for q in range(len_x):
            ax = axlist[q]
            for r in range(len_y):
                # sub-title
                self.set_sub_title(ax[r], c, quad_degree_list, orders, dofs)

                # condition numbers
                label = lambda name: name if q == 0 and r == 0 else None
                ax[r].plot(defo, self.pandas_to_list(knds_mixed, c),
                           '-o', color=self.color[1],
                           label=label("Mixed"),
                           **self.plotting_args)
                ax[r].plot(defo, self.pandas_to_list(knds_Schur, c),
                           '-x', color=self.color[0],
                           label=label("Schur complement"),
                           **self.plotting_args)
                ax[r].plot(defo, self.pandas_to_list(knds_A00, c),
                           '-D', color=self.color[2],
                           label=label("Velocity mass"),
                           **self.plotting_args)
                c += 1

        # add legend
        plt.figlegend(ncol=3, loc="center", bbox_to_anchor=[0.5, 0.04], frameon=True)
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.17)

        self.save_plot(name + "_knds_" + type + ".pdf")

    def plot_per_order(self, name, orders, dofs, defo, results, knds, params, quad_degree_list, its_type, xlabel, ylabel):
        # format the subplots
        len_x = int(len(orders)/2)
        len_y = len(orders) - int(len(orders)/2) - 1
        fig, axlist = plt.subplots(len_x, len_y, figsize=(13, 8))

        # add labels to outer frame not per subplot
        # iterations on left and condition numbers on the right
        ax_outer = fig.add_subplot(111, frameon=False)
        plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
        ax_outer.set_xlabel(xlabel, weight='bold', labelpad=10)
        self.set_ax_ylabel(ax_outer, ylabel)
        ax_outer.set_yticks([])
        ax2_outer = ax_outer.twinx()
        ax2_outer.set_ylabel('condition numbers', color=self.color[1], weight='bold', labelpad=50)
        ax2_outer.set_yticks([])

        # clean up the xlabels
        defo = self.round(defo)

        c = 0
        for q in range(len_x):
            ax = axlist[q]
            for r in range(len_y):
                # sub-title
                self.set_sub_title(ax[r], c, quad_degree_list, orders, dofs)

                # iteration counts
                ax[r].plot(defo, self.pandas_to_list(results, c),
                           "-D", color=self.color[0], **self.plotting_args)

                # condition numbers
                ax2 = ax[r].twinx()
                ax2.plot(defo, self.pandas_to_list(knds, c),
                         '-o', color=self.color[1], **self.plotting_args)

                c += 1

        plt.tight_layout()

        self.save_plot(name + "_" + its_type + ".pdf")

    def set_sub_title(self, ax, c, quad_degree_list, orders, dofs):
        degrees = self.pandas_to_list(quad_degree_list, 0, ",")
        ax.set_title(self.title % (int(orders[c])+1, int(orders[c]),
                                   float(dofs[c]), float(dofs[c]),
                                   int(degrees[c]), int(degrees[c])))

    def set_ax_ylabel(self, ax, its_type):
        ax.set_ylabel(f'{its_type} ksp iterations', color=self.color[0], weight='bold', labelpad=40)
        return ax

    def save_plot(self, name):
        plt.savefig(name)

    def pandas_to_list(self, results, order, delim=","):
        # Pandas saves data as string and really doesn't like arrays in cells
        return list(int(float(list(res.strip('[').strip(']').split(delim))[order]))
                    for res in results)

    def round(self, defo):
        return list(round(float(d), 1) for d in defo)
