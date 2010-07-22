/*
 * crowdfilter.h
 *
 *  Created on: Jul 21, 2010
 *      Author: dan
 */

#ifndef CROWDFILTER_H_
#define CROWDFILTER_H_

#include "types.h"

#include <vector>

namespace lsd {

double compute_closeness (TweedUser &user1, TweedUser &user2);

}

#endif /* CROWDFILTER_H_ */
