#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
生成树状结构
'''
from public_bz import storage


def makeTree(nodes):
    '''
    modify by liuyong at 15/05/06 09:52:44
    node.id = 0
    node.parent_id = 0
    node.children = []

    node.level 节点所在层
    根据 node.id 和 node.parent_id 将铺平的数据组织成树状
    放到 children 节点
    '''
    tree = []
    # 为了确定节点所在层，使用parent_id进行排序
    nodes = sorted(nodes, key=lambda k: k.parent_id)
    for node in nodes:
        if node.parent_id == 0:
            node.level = 1
            tree.append(node)
        else:
            parent_node = findNode(tree, node.parent_id)
            if parent_node:
                addChilren(parent_node, node)
            # 父节点还没加入到 tree 中
            else:
                parent_node = findNode(nodes, node.parent_id)
                addChilren(parent_node, node)
    return tree


def addChilren(parent_node, child_node):
    '''
    modify by liuyong at 15/05/06 09:52:52
    加入子节点
    '''
    child_node.level = parent_node.level + 1
    if parent_node.get('children'):
        parent_node.children.append(child_node)
    else:
        parent_node.children = [child_node]


def findNode(nodes, id):
    '''
    在树里面查找节点
    '''
    for node in nodes:
        if node.id == id:
            return node
        # 递归查找其子节点
        if node.get('children'):
            target_node = findNode(node.children, id)
            if target_node:
                return target_node


def makeSelectTree(nodes):
    '''
    '''
    tree = []
    for node in nodes:
        if node.parent_id == 0:
            tree.append(node)
        else:
            parent_node = findSelectNode(tree, node.parent_id)
            if parent_node:
                addSelectChilren(parent_node, node)
            # 父节点还没加入到 tree 中
            else:
                parent_node = findSelectNode(nodes, node.parent_id)
                addSelectChilren(parent_node, node)
    return tree


def addSelectChilren(parent_node, child_node):
    '''
    加入子节点
    '''
    parent_id = str(parent_node.get('id'))
    if parent_node.get(parent_id):
        parent_node[parent_id].append(child_node)
    else:
        parent_node[parent_id] = [child_node]


def findSelectNode(nodes, id):
    '''
    在树里面查找节点
    '''
    for node in nodes:
        if node.id == id:
            return node
        # 递归查找其子节点
        if node.get(str(id)):
            target_node = findSelectNode(node[str(id)], id)
            if target_node:
                return target_node


if __name__ == '__main__':
    nodes = []

    node = storage()
    node.id = 3
    node.parent_id = 2
    nodes.append(node)

    node = storage()
    node.id = 2
    node.parent_id = 1
    nodes.append(node)

    node = storage()
    node.id = 5
    node.parent_id = 1
    nodes.append(node)

    node = storage()
    node.id = 1
    node.parent_id = 0
    nodes.append(node)

    node = storage()
    node.id = 8
    node.parent_id = 0
    nodes.append(node)

    node = storage()
    node.id = 9
    node.parent_id = 8
    nodes.append(node)
    print makeTree(nodes)
