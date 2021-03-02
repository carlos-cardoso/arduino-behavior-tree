#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
//EXAMPLE
    auto tree = Builder<Context>{}
        .leaf([](Context &context) {
            auto success = DoSomething();
            return success ? Status::SUCCESS : Status::FAILURE;
        })
        .build();
"""

import xml.etree.ElementTree as ET
import sys

TREE_HEADER = """
#ifndef TREE__H 
#define TREE__H

#include <beehive.hpp> 
#include "context.h"
#undef min 
#undef max 

using namespace beehive;
"""

TREE_FOOTER = """
#endif //TREE_H
"""


CONTEXT_HEADER = """
#ifndef CONTEXT_H
#define CONTEXT_H
#include <beehive.hpp> 
#include "Data.h"

using namespace beehive;
struct Context
{
    Data &data;
    Context(Data &_data):data(_data){}
"""
CONTEXT_FOOTER = """};
#endif //CONTEXT_H
"""


fname = 'meta_tree.xml'
ddest = "lib/behavior_tree/"
if len(sys.argv) > 1:
    fname = sys.argv[1]
if len(sys.argv) > 2:
    ddest = sys.argv[2]

tree = ET.parse(fname)
root = tree.getroot()


TREE_PATH = ddest+"TREE.h"
CONTEXT_PATH = ddest+"context.h"

print("Available trees:\n")
trees = {}
for ind, child in enumerate(root):
    print(child.tag, child.attrib)
    try:
        trees[child.attrib['ID']] = ind
    except KeyError:
        print(child.tag)

actions = {}


def process_node(child, to_write, depends):
    requires_end = 0
    subtree = None
    print("enter:")
    print(child.tag, child.attrib)
    if child.tag == "Sequence":
        to_write += (".sequence()\n")
        requires_end = 1
    elif child.tag == "Fallback":
        to_write += (".selector()\n")
        requires_end = 1
    elif child.tag == "Action" or child.tag == "Condition":
        to_write += (".leaf(&Context::{})\n".format(child.attrib['ID']))
        if child.attrib['ID'] not in actions:
            f_context.write("  Status {}();\n".format(child.attrib['ID']))
            actions[child.attrib['ID']] = 1
    elif child.tag == "ForceFailure":
        to_write += (".inverter().succeeder()\n")
        requires_end = 2
    elif child.tag == "ForceSuccess":
        to_write += (".succeeder()\n")
        requires_end = 1
    elif child.tag == "Inverter":
        to_write += (".inverter()\n")
        requires_end = 1
    elif child.tag == "AlwaysFailure":
        to_write += (".leaf([](Context _) { return false; })\n")
    elif child.tag == "AlwaysSuccess":
        to_write += (".leaf([](Context _) { return true; })\n")
    elif child.tag == "SubTree":
        #subtree = root[trees[child.attrib['ID']]]
        depends.append(child.attrib['ID'])
        to_write += (".tree({})\n".format(child.attrib['ID']))
    else:
        print("UNKNOWN")
        print(child.tag, child.attrib)
        exit()
    return requires_end, subtree, depends, to_write


print("START:")


def traverse(root, level=0, to_write="", depends=[]):
    for child in root:
        for i in range(level):
            to_write += ("  ")
        N_ENDS, subtree, depends, to_write = process_node(
            child, to_write, depends)
        if subtree != None:
            to_write, depends = traverse(subtree, level, to_write, depends)

        if N_ENDS > 0:
            to_write, depends = traverse(child, level + 1, to_write, depends)
            for i in range(level):
                to_write += ("  ")
            for i in range(N_ENDS):
                to_write += (".end()")
            to_write += ("\n")
    return to_write, depends


f_tree = open(TREE_PATH, 'w')
f_tree.write(TREE_HEADER)
f_context = open(CONTEXT_PATH, 'w')
f_context.write(CONTEXT_HEADER)

for tree in reversed(root):
    try:
        f_tree.write(
            "\ntemplate <typename T = Context> //template to avoid multiple declaration, default type to fix deduction error\nTree<T> build_tree_{}(){{\n"
            .format(tree.attrib['ID']))
        to_write, depends = traverse(tree, 0, "", [])
        for depend in depends:
            f_tree.write("  Tree<T> {} = build_tree_{}();\n".format(
                depend, depend))
        f_tree.write("\n  return Builder<T>{{}}".format(tree.attrib['ID']))
        f_tree.write(to_write)
        f_tree.write(".build();}\n\n")
    except KeyError:
        pass

f_tree.write(TREE_FOOTER)
f_context.write(CONTEXT_FOOTER)

f_tree.close()
f_context.close()
