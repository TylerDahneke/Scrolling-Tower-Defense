import tkinter as tk
import random as random

WIDTH = 1000
HEIGHT = 500

FLOOR_HEIGHT = int(.8 * HEIGHT)


class Shape_node:

    def __init__(self, shape=None, pos=None, vel=2, team=True, sight=None,
                 attack_rng=50):
        if sight is None:
            self.sight = []
        self.shape = shape
        self.pos = pos
        self.x, self.y = self.pos % WIDTH, self.pos // WIDTH
        self.team = team
        self.vel = vel
        self.a_r = attack_rng
        self.v_b_x, self.v_b_y, self.v_b_x2, self.v_b_y2 = self.x, self.y, self.x + 75, self.y + 50
        self
        if not team:
            self.vel = -self.vel
            self.vision_box[0], self.vision_box[2] = self.x - 50, self.x + 25

    def fill_vision(self, sight):
        if sight == []:
            pass
        self.sight = sight

    def change_vel(self):
        if type(Shape_node) in self.sight:
            print('passed')
            self.vel = 0
        else:
            print('failed')
            self.vel = 2
            if self.team is False:
                self.vel = -self.vel


class Map:

    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, height=HEIGHT, width=WIDTH)
        self.allies, self.enemies = {}, {}

        self.create_ally()
        self.create_enemy()
        self.movement()
        self.create_map()
        self.canvas.pack()

    def movement(self):
        for ph in self.allies:
            for ally_node in self.allies[ph]:
                ally_node.change_vel()
                self.canvas.move(ally_node.shape, ally_node.vel, 0)
                self.fill_node_vis(ally_node)

        for ph in self.enemies:
            for enemy_node in self.enemies[ph]:
                enemy_node.change_vel()
                self.canvas.move(enemy_node.shape, enemy_node.vel, 0)
                self.fill_node_vis(enemy_node)

        self.canvas.after(30, self.movement)

    def create_map(self):
        setting = {}
        ph = self.canvas.create_rectangle(0, FLOOR_HEIGHT, WIDTH + 1, HEIGHT, fill='green', outline='')
        setting['floor'] = [Shape_node(shape=ph, pos=FLOOR_HEIGHT * WIDTH)]

    def create_ally(self):
        ally_shape = self.canvas.create_rectangle(5, FLOOR_HEIGHT - 55, 30, FLOOR_HEIGHT - 5)
        if 'box' not in self.allies:
            self.allies['box'] = [Shape_node(shape=ally_shape, pos=(FLOOR_HEIGHT - 50) * WIDTH + 5)]
        else:
            self.allies['box'].append(Shape_node(shape=ally_shape, pos=(FLOOR_HEIGHT - 50) * WIDTH + 5))

    def create_enemy(self):
        enemy_shape = self.canvas.create_rectangle(WIDTH - 30, FLOOR_HEIGHT - 55, WIDTH - 5, FLOOR_HEIGHT - 5)
        if 'box' not in self.enemies:
            self.enemies['box'] = [Shape_node(shape=enemy_shape, pos=(FLOOR_HEIGHT - 50) * WIDTH + 5,
                                              team=False)]
        else:
            self.enemies['box'].append(Shape_node(shape=enemy_shape, pos=(FLOOR_HEIGHT - 50) * WIDTH + 5,
                                                  team=False))

    def fill_node_vis(self, node):
        vis_list = []
        if node in self.allies:
            for enemy_name in self.enemies:
                for enemy in self.enemies[enemy_name]:
                    if node.x <= enemy.x <= node.x + node.a_r:
                        print('added enemey')
                        vis_list.append(enemy)
        else:
            for ally_name in self.allies:
                for ally in self.allies[ally_name]:
                    if node.x - node.a_r >= ally.x >= node.x:
                        print('added enemey')
                        vis_list.append(ally)
        node.fill_vision(vis_list)

    def are_colliding(self, ob_1, ob_2):
        return (ob_1.x * 10 < ob_2.x * 10 + ob_2.width and
                ob_1.x * 10 + ob_1.width > ob_2.x * 10 and
                ob_1.y * 10 < ob_2.y * 10 + ob_2.width and
                ob_1.y * 10 + ob_1.width > ob_2.y * 10)


def get_pos_from_index(index):
    return index % WIDTH, index // HEIGHT


if __name__ == '__main__':
    root = tk.Tk()
    mast = Map(root)

    tk.mainloop()
