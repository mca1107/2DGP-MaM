world = [[], [], []]
collision_pairs = {} # key: 충돌 종류, value: [a], [b]
def add_object(o, depth = 0):
    world[depth].append(o)
def add_objects(ol, depth = 0):
    world[depth] += ol
def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f'새로운 그룹 추가: {group}')
        collision_pairs[group] = [[], []]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)
def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return
    raise ValueError('Cannot delete non existing object')
def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)
def update():
    for layer in world:
        for o in layer:
            o.update()
def render():
    for layer in world:
        for o in layer:
            o.draw()
def clear():
    global world
    for layer in world:
        layer.clear()
def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide_rect_to_rect(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
def collide_rect_to_rect(a, b): # 두 사각형 사이의 충돌 검사
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True
# 다른 종류의 충돌 검사