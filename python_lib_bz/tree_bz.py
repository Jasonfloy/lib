#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
生成树状结构
'''
from public_bz import storage


def makeTree(nodes):
    '''
    node.id = 0
    node.parent_id = 0
    node.children = []

    根据 node.id 和 node.parent_id 将铺平的数据组织成树状
    放到 children 节点
    '''
    tree = []
    for node in nodes:
        if node.parent_id == 0:
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
    加入子节点
    '''
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


if __name__ == '__main__':
    nodes = []

    node = storage()
    node.id = 1
    node.parent_id = 0
    nodes.append(node)

    node = storage()
    node.id = 2
    node.parent_id = 1
    nodes.append(node)

    node = storage()
    node.id = 4
    node.parent_id = 2
    nodes.append(node)

    node = storage()
    node.id = 5
    node.parent_id = 1
    nodes.append(node)

    print makeTree(nodes)
