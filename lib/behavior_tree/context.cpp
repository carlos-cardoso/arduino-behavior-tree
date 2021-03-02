#include "context.h"

using namespace beehive;


Status Context::Have5sPassed() {
  Status result{Status::FAILURE};
  if( millis() > this->data.start + 5000 ){
    result = Status::SUCCESS;
  }

  return result;
}

Status Context::TurnLedOn() {
  Status result{Status::SUCCESS};

  digitalWrite(this->data.led, HIGH);

  return result;
}
