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
        self.color = sns.color_palette(n_colors=2)
        self.plotting_args = {'linewidth': 2, 'markersize': 5}
        self.title = 'RTCF %d, DG %d (=%dx%d DOFS)\n quad_degree=(%d, %d)'

    def plot_per_order(self, name, orders, dofs, defo, results, knds, params, quad_degree_list, its_type, xlabel):
        # format the subplots
        len_x = int(len(orders)/2)
        len_y = len(orders) - int(len(orders)/2) - 1
        _, axlist = plt.subplots(len_x, len_y, figsize=(13, 8))

        # clean up the xlabels
        defo = self.round(defo)
        print(knds)

        c = 0
        for q in range(len_x):
            ax = axlist[q]
            for r in range(len_y):
                # sub-title
                self.set_sub_title(ax[r], c, quad_degree_list, orders, dofs)

                # iteration counts
                ax[r].plot(defo, self.pandas_to_list(results, c),
                           "-D", color=self.color[0], **self.plotting_args)
                ax[r].set_xlabel(xlabel)
                self.set_ax_ylabel(ax[r], its_type)

                # condition numbers
                ax2 = ax[r].twinx()
                ax2.plot(defo, self.pandas_to_list(knds, c),
                         '-o', color=self.color[1], **self.plotting_args)
                ax2.set_ylabel('condition numbers', color=self.color[1])

                c += 1

        plt.tight_layout()

        self.save_plot(name + "_" + its_type + ".pdf")

    def set_sub_title(self, ax, c, quad_degree_list, orders, dofs):
        degrees = self.pandas_to_list(quad_degree_list, 0, ",")
        ax.set_title(self.title % (int(orders[c])+1, int(orders[c]),
                                   float(dofs[c]), float(dofs[c]),
                                   int(degrees[c]), int(degrees[c])))

    def set_ax_ylabel(self, ax, its_type):
        if its_type == "total":
            # outer_its*(fsp1_its+fsp1_its*fsp0_its)
            ax.set_ylabel('total ksp iterations', color=self.color[0]) 
        else:
            ax.set_ylabel('outer ksp iterations', color=self.color[0])
        return ax

    def save_plot(self, name):
        plt.savefig(name)

    def pandas_to_list(self, results, order, delim=","):
        # Pandas saves data as string and really doesn't like arrays in cells
        return list(int(float(list(res.strip('[').strip(']').split(delim))[order]))
                    for res in results)

    def round(self, defo):
        return list(round(float(d), 1) for d in defo)
