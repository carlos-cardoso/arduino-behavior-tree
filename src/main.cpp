#undef min
#undef max

#include <beehive.hpp>
#include "TREE.h"

using namespace beehive;

const uint32_t led_pin{13};
Data tree_data{led_pin}; //initialize the data structure with example data led_pin
Context tree_state{tree_data}; //use the struct as context for the tree
Tree<Context> behavior_tree;  //create behavior tree

void setup() {

  const uint32_t start = millis();
  tree_state.data.initialize(start); //initialize tree data with the start time
  behavior_tree = build_tree_BehaviorTree(); //build the behavior tree

};

void loop() {

  behavior_tree.process(tree_state); //run the tree

};
