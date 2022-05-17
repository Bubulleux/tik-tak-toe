import tkinter


class Tree:
    def __init__(self, main_node):
        self.nodes = {
            (): main_node
        }

    def add_node(self, pos: tuple, values):
        if len(pos) != 0 and pos[:-1] not in self.nodes.keys():
            raise IndexError

        self.nodes[pos] = values

    def remove_node(self, pos: tuple):
        to_delete = []
        for p, value in self.nodes.items():
            if pos == p[:len(pos)]:
                to_delete.append(p)

        for p in to_delete:
            self.nodes.pop(p)

    def __str__(self):
        keys = list(self.nodes.keys())
        keys.sort()
        output = ""
        for key in keys:
            output += f"{'   ' * len(key)}{key}: {self.nodes[key]}\n"
        return output


class TreePlot:
    def __init__(self, tree):
        self.tree = tree

    def show(self):
        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.root, width=500, height=500)
        self.canvas.create_oval(0, 0, 100, 100)
        self.canvas.pack()

        self.root.mainloop()


if __name__ == '__main__':
    nodes = {
        (): 0,
        (0,): 1,
        (0, 0): 2,
        (1,): 1,
        (1, 0): 2,
        (1, 1): 2,
    }

    tree = Tree(0)
    tree.nodes = nodes
    print(tree)
    plot = TreePlot(tree)
    plot.show()



