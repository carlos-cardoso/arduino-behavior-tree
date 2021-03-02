#undef min
#undef max

#include "TREE.h"
#include <beehive.hpp>

using namespace beehive;

  Data tree_data{13};
  Context tree_state{tree_data};
  Tree<Context> behavior_tree;
void setup() {

  const uint32_t start = millis();
  tree_state.data.initialize(start);
  behavior_tree = build_tree_BehaviorTree();

};

void loop() {

  behavior_tree.process(tree_state);

};
