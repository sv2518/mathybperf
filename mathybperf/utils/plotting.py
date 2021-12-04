from firedrake import *
from mathybperf import *
import matplotlib.pyplot as plt
import os


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
        self.color =  ['tab:red', "tab:blue"]

    def plot_its_vs_scaling_fororder(self, name, orders, dofs, scalings, results, params, its_type):
        # only for one ksp it
        results = results[0]

        len_x = int(len(orders)/2)
        len_y = len(orders) - int(len(orders)/2) - 1
        fig, axlist = plt.subplots(len_x, len_y, figsize=(16, 8))

        title = ""
        for i, v in params.items():
            title += "%s: %s \n" % (i,v)
        fig.suptitle(title, fontsize=10)

        c = 0
        for q in range(len_x):
            ax = axlist[q]
            for r in range(len_y):
                ax[r].plot(scalings, results[c], '-x')

                ax[r].set_title('RTCF %d, DG %d (=%dx%d DOFS)' % (orders[c]+1,orders[c], dofs[c], dofs[c]), fontsize=10)
                ax[r].set_xlabel('cell scalings', fontsize=10)
                self.set_ax_ylabel(ax, its_type)

                c+=1

        plt.subplots_adjust(hspace=0.5)
        plt.subplots_adjust(wspace=1.5)
        
        self.save_plot(name)


    def plot_deformation_vs_its_fororder(self, name, orders, dofs, defo, results, knds, params, quad_degree_list, its_type):
        len_x = int(len(orders)/2)
        len_y = len(orders) - int(len(orders)/2) - 1
        fig, axlist = plt.subplots(len_x, len_y, figsize=(16, 8))

        title = ""
        for i, v in params.items():
            title += "%s: %s \n" % (i,v)
        fig.suptitle(title, fontsize=10)

        c = 0
        for q in range(len_x):
            ax = axlist[q]
            for r in range(len_y):
                ax[r].plot(defo, list(res[c] for res in results), '-x', color=self.color[0])
    
                title = 'RTCF %d, DG %d (=%dx%d DOFS)\n, quad_degree=(%d, %d)'
                ax[r].set_title(title % (orders[c]+1,orders[c], dofs[c], dofs[c],
                                         quad_degree_list[c][0], quad_degree_list[c][1]), fontsize=10)
                ax[r].set_xlabel('deformations', fontsize=10)
                
                ax2 = ax[r].twinx() 
                ax2.plot(defo, list(res[c] for res in knds),'-o', color=self.color[1])
                ax2.set_ylabel('kondition numbers', color=self.color[1])

                c+=1

        plt.subplots_adjust(hspace=0.5)
        plt.subplots_adjust(wspace=1.5)

        self.save_plot(name)

    def set_ax_ylabel(self, ax, its_type):
        if its_type == "total":
            ax[r].set_ylabel('total ksp iterations \n [outer_its* \n(fsp0_its+fsp1_its*fsp0_its)]', fontsize=10, color=self.color[0])
        else:
            ax[r].set_ylabel('outer ksp iterations', fontsize=10, color=self.color[0])
        return ax



    def save_plot(self, name):
        # Figures out the absolute path for you in case your working directory moves around.
        path = os.path.dirname(__file__)
        plt.savefig(path+name)
