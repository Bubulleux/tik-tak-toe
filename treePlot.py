import tkinter


class Tree:
    def __init__(self, main_node):
        self.nodes = {
            (): main_node
        }

    def add_node(self, pos: tuple, values):
        if len(pos) != 0 and pos[:-1] not in self.nodes.keys():
            print(pos, values)
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
        self.node_size = 50
        self.on_click_node = None
        self.node_pos = {}

    def show(self):
        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.root, width=1000, height=800)
        self.canvas.bind("<Button-1>", self.click_canvas)
        self.canvas.bind("<Button-3>", self.zoom_in)
        self.draw_plot()

        self.canvas.pack()
        self.root.mainloop()

    def draw_plot(self, root=()):
        self.canvas.delete("all")
        valid_key = []
        for key in self.tree.nodes.keys():
            if key[:len(root)] == root:
                valid_key.append(key[len(root):])

        stage_size = {}
        for key in valid_key:
            if len(key) in stage_size.keys():
                stage_size[len(key)] += 1
            else:
                stage_size[len(key)] = 1

        max_size = max(stage_size.values())
        width = 1000

        sorted_key = valid_key.copy()
        sorted_key.sort()

        stage_index = [0] * len(stage_size)
        self.node_pos.clear()
        for key in sorted_key:
            stage = len(key)
            if stage >= 4:
                continue
            x = (width / (stage_size[stage] + 1) * (stage_index[stage] + 1)) - self.node_size / 2
            y = stage * 2 * self.node_size + self.node_size / 2
            self.canvas.create_oval(x+0.1, y, x + self.node_size, y + self.node_size)
            if len(key) != 0:
                self.canvas.create_text(x, y, text=str(key[-1]))

            if stage != 0:
                p_x, p_y = self.node_pos[root + key[:-1]]
                self.canvas.create_line(p_x + self.node_size / 2, p_y + self.node_size, x + self.node_size / 2, y)

            self.node_pos[root + key] = (x, y)
            stage_index[stage] += 1
        self.canvas.update()

    def get_node(self, event):
        for key, (x, y) in self.node_pos.items():
            if x < event.x < (x + self.node_size) and y < event.y < (y + self.node_size):
                return key

    def click_canvas(self, event):
        if self.on_click_node is None:
            return
        key = self.get_node(event)
        if key is not None:
            self.on_click_node(key, self.tree.nodes[key])

    def zoom_in(self, event):
        key = self.get_node(event)
        if key is not None:
            self.draw_plot(root=key)
        else:
            self.draw_plot()


if __name__ == '__main__':
    nodes = {
        (): 0,
        (0,): 1,
        (0, 0): 2,
        (1,): 1,
        (1, (2, )): 2,
        (1, (1, )): 2,
    }

    tree = Tree(0)
    tree.nodes = nodes
    print(tree)
    plot = TreePlot(tree)
    plot.on_click_node = lambda key, node: print(key, node)
    plot.show()



